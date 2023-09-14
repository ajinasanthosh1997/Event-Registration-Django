from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm

# Create your views here.
def index(request):
    events = Event.objects.all()
    context = {
        'events': events
    }
    return render(request, 'index.html', context)


def details(request,pk):
    event = Event.objects.get(pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.event = event
            applicant.save()
            return redirect('/')
            
        else:
            print(form.errors)

    form = EventForm()
    context = {
        'event' : event,
        'form':form
    }
    return render(request,'details.html', context)
