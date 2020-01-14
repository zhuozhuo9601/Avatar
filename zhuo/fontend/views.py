from django.shortcuts import render

# Create your views here.

def vue_text(request):
    return render(request, 'vue_text.html')