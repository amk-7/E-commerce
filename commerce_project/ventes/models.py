from django.db import models
from accounts.models import Personne
from django.core.validators import MinValueValidator, MaxValueValidator
from .exception import ShopperNotFoundException, CommandeNoteFoundException, CommandeLineNoteFoundException
from postes.models import Post

class Manager(Personne):
    class Meta:
        verbose_name_plural = "Managers"
    def __str__(self):
        return super().__str__()

class Shopper(Personne):
    # Ajouter les attributs nécessaire au payements et à la livraison
    class Meta:
        verbose_name_plural = "Shoppers"
    
    def __str__(self):
        return super().__str__()
    
    def setArticleNote(self, article, note):
        shopperArticles, created = ShopperArticle.objects.get_or_create(article=article, shopper=self)
        shopperArticles.setNote(note)
        article.calculateNote()

    def likePost(self, post):
        shopper_poste, created = ShopperPost.objects.get_or_create(shopper=self, post=post)
        #print("Created::::: ", shopper_poste.liked)
        if created or shopper_poste.liked==False:
            shopper_poste.liked = True
            shopper_poste.post.incrementNbLike()
            shopper_poste.save()
        else:
            shopper_poste.liked = False
            shopper_poste.post.decrementNbLike()
            shopper_poste.save()
    
    def getCurrentCommande(self):
        commandes = Commande.objects.filter(shopper=self, state=-1)
        if commandes:
            return commandes[0]
        return []
    
    def deleteCommande(self):
        commandes = Commande.objects.filter(shopper=self, state=-1)
        if len(commandes) < 1:
            raise CommandeNoteFoundException
        commande = commandes[0]
        #Avant de supprimer on ramème ce qui avait avant.
        commande.delete()

    def addLineToCommande(self, _article):
        # _ (c'est une convension) signifie que la variable "_" ne sera jamais utilisé
        commande, _ = Commande.objects.get_or_create(shopper=self)
        line, created = CommandeBasket.objects.get_or_create(commande=commande, article=_article)

        if created:
            #print(created)
            line.save()
            line.article.updateQuantity(line.quantity*-1)
            
            
    def updateCommandeLine(self, line, _quantity):
        # _ (c'est une convension) signifie que la variable "_" ne sera jamais utilisé
        if line:
            line.updateQuantity(_quantity); 
        else:
            raise CommandeLineNoteFoundException

class Categorie(models.Model):
    wording = models.CharField(max_length=128)

    def __str__(self):
        return self.wording

class ShopperPost(models.Model):
    shopper = models.ForeignKey(Shopper, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)

class Article(models.Model):
    designation = models.CharField(max_length=128, unique=True)
    pricePurchase = models.FloatField(default=0.0)
    benefitPercentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stock = models.IntegerField(default=0)
    reduction = models.IntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    note = models.FloatField(default=0.0, blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    thumbnail = models.ImageField(upload_to="articles", blank=True, null=True)
    categorie = models.ForeignKey(Categorie, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.designation
    
    def getFakePrice(self):
        return self.price*0.3

    def getSalePrice(self):
        return self.pricePurchase + (self.pricePurchase*self.benefitPercentage/100)
    
    def updateQuantity(self, _quantity):
        print(_quantity)
        if _quantity >= 0 or _quantity < 0:
            self.stock += _quantity
        else:
            raise ValueError
        self.save()
    def calculateNote(self):
        shopperArticles = ShopperArticle.objects.filter(article=self)
        mean = 0
        for shopperArticle in shopperArticles:
            mean += shopperArticle.note
        self.note = mean/len(shopperArticles)
        self.save()

    

class Supply(models.Model):
    manager = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.manager.username}({self.date})"

class SupplyBasket(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.article.designation}({self.quantity})"


class ShopperArticle(models.Model):
    shopper = models.ForeignKey(Shopper, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    note = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def setNote(self, note):
        self.note = note
        self.save()

class Commande(models.Model):
    shopper = models.ForeignKey(Shopper, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, blank=True)
     # 1 : client reçoit cmd. 0 : cmd en cours de livraisons. -1 : cmd créer
    state = models.IntegerField(default=-1, validators=[MinValueValidator(-1), MaxValueValidator(1)]) 

    def __str__(self):
        return f"{self.shopper.user.username}({self.date})"
    
    def updateQuantity(self):
        self.save()
    
    def delete(self):
        commande_lines = CommandeBasket.objects.filter(commande=self)
        for line in commande_lines:
            line.article.updateQuantity(line.quantity)
        super().delete()

class CommandeBasket(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def delete(self):
        self.article.updateQuantity(self.quantity)
        super().delete()
   
    def __str__(self):
        return f"{self.article.designation}({self.quantity})"

    """def setQuantity(self, _quantity):
        self.quantity = _quantity
        self.save()
        setValue = _quantity*-1
        try:
            self.article.updateQuantity(setValue)
        except ValueError as ve:
            raise ve"""

    def updateQuantity(self,_quantity):
        setValue = _quantity - self.quantity
        self.quantity += setValue
        try:
            self.article.updateQuantity(setValue*-1)
        except ValueError as ve:
            print("##########################")
        self.save()
       
