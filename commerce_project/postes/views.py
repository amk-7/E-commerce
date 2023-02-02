from django.shortcuts import render, get_object_or_404, redirect
from postes.models import Post
from django.urls import reverse
from django.http import JsonResponse
from ventes import otherViews as ov

def index(request):
    postes = Post.objects.all()
    return render(request, 'postes/index.html', context={'postes':postes})
    #return render(request, 'postes/insta.html', context={})

def liker(request, id):
    post = get_object_or_404(Post, pk=id)
    shopper = ov.findShopper(request.user)
    if shopper:
        shopper.likePost(post)
        return JsonResponse({"result" : post.loveNumber==0})
    return JsonResponse({"result" : False})
