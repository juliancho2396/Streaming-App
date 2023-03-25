from django.shortcuts import render, redirect

# Create your views here.
def login_vue(request):
    if request.method == "POST":
        return redirect('home:principal')
    return render(request, 'login.html')

def principal_vue(request):

    return render(request, 'principal.html')

def creation_vue(request):

    if request.method == "POST":
        return redirect('home:principal')
    return render(request, 'creation.html')

def modification_vue(request):
    if request.method == "POST":
        return redirect('home:principal')
    return render(request, 'creation.html')




