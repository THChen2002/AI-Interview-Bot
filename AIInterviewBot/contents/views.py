from django.shortcuts import render

def self_introduction(request):
    return render(request, 'contents/self_introduction.html')