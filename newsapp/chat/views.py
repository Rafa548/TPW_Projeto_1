from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

 
@login_required
def chatPage(request, *args, **kwargs):
    context = {}
    return render(request, "chatpage.html", context)

