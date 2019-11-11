from django.shortcuts import render

# Create your views here.


def study_first(request):
    return render(request, 'study.html')