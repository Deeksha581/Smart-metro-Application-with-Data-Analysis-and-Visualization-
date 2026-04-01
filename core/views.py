from django.shortcuts import render

def home(request):
    return render(request, "common/home.html")  # ✅ FIXED
def about(request):
    return render(request, "accounts/about.html")

