from django.shortcuts import render

# Create your views here.
def ml_block(request):
    return render(request,'ml_block.html',{})