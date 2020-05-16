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
            myform = CommadForm(request.POST)
            if myform.is_valid():
                execute_command = myform.cleaned_data['command']
                try:
                    output = sp.check_output(execute_command, shell=True)
                except sp.CalledProcessError:
                    output = 'No such command'
            else:
                myform = CommadForm()
            return render(request, 'testPlot.html', {'output': output})
        else:
            return render(request, 'testPlot.html')