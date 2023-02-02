from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import get_object_or_404, HttpResponse
from ventes.models import Shopper
from ventes import otherViews as ov

User = get_user_model()

def signup(request):
    if request.method == "POST":
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        adresse = request.POST.getlist('adresse[]')
        contact = request.POST.get('contact')
        #Verifier si le username exist déjà.
        user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname, email=email)
        login(request, user)
        shopper, _ = Shopper.objects.get_or_create(contact=contact, adresse=adresse, user=user)
        #Vérifier si l'utilisateur à été bien créé.
        return redirect('ventes:index')
    return render(request, 'accounts/signup.html', context={})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('ventes:index')
    return render(request, 'accounts/login.html', context={})

def logout_user(request):
    logout(request)
    return redirect('ventes:index')

def edit_user(request, id):
    user = get_object_or_404(User, pk=id)
    shopper = ov.findShopper(request.user)

    return HttpResponse(user)