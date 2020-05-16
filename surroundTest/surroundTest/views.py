from django.shortcuts import render
from django.shortcuts import redirect
from .forms import CommadForm
import subprocess as sp




def index(request):
    return render(request, 'index.html')
def example(request):
    return render(request,'example.html')
def aiconcepts(request):
    return render(request,'aiconcepts.html')
def testPlot(request):
    if request.method == "POST":
        form = Board_elementForm(request.POST)
        if form.is_valid():
            print("valid")
            form.save()
            return redirect('board_index')

    else:
        form = Board_elementForm(request.POST)
    context = {
        'form': form
    }
    return render(request, 'board_form.html', context)