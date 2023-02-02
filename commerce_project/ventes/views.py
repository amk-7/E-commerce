from django.shortcuts import render, redirect
from django.http import HttpResponse
from ventes.models import Article, Shopper, CommandeBasket,Categorie
from django.shortcuts import get_object_or_404
from django.urls import reverse
from . import otherViews as ov

def index(request):
    #return render(request, "welcome.html")
    data = {}
    shopper = ov.findShopper(request.user)
    if shopper:
        data['commandLine'] = shopper.getCurrentCommande()

    data["articles"] =  Article.objects.all()
    return render(request, 'store/index.html', context=data)

def details(request, id):
    article = get_object_or_404(Article, pk=id)
    return render(request, 'store/details.html', context={'article' : article})

def addToCart(request, id):
    user = request.user
    shopper = Shopper.objects.filter(user=user)[0]
    article = get_object_or_404(Article, pk=id)
    shopper.addLineToCommande(article)

    return redirect(reverse("ventes:article", kwargs={'id': id}))

def cart(request):
    shopper = ov.findShopper(request.user)
    commande = None
    if shopper:
        commande = shopper.getCurrentCommande()
        orders = commande.commandebasket_set.all()

    if request.method == "POST":
        if 'update' in request.POST:
            line_ids = request.POST.getlist('ids[]')
            quantitys = request.POST.getlist('quantity[]')
            for i in range(len(line_ids)):
                line = get_object_or_404(CommandeBasket, pk=int(line_ids[i]))
                if line:
                    quantity =int(quantitys[i])
                    if quantity > 0:
                        line.updateQuantity(quantity)
                    else:
                        raise ValueError
            orders = commande.commandebasket_set.all()
        else:
            pass    
    return render(request, 'store/cart.html', context={"orders" : orders })

def delete_cart(request):
    user = request.user
    shopper = Shopper.objects.filter(user=user)[0]
    shopper.deleteCommande()
    return redirect('ventes:index')

def note_article(request, id):
    shopper = ov.findShopper(request.user)
    if shopper:
        note = request.POST['note']
        article = get_object_or_404(Article, pk=id)
        shopper.setArticleNote(article, note)
    #return HttpResponse("Okay")
    return redirect(reverse('ventes:article', kwargs={"id": id}))

def categorie(request):
    if request.method == "POST":
        wording_str = request.POST.get('wording')
        categorie = Categorie(wording=wording_str)
        categorie.save()
        return redirect('ventes:index')
    return render(request, 'userAccount/formulaireCategorie.html')











