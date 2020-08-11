from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


class NewTaskForm(forms.Form):
    # character field with a label
    task = forms.CharField(label="New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        # looking in the session, if there is no list with key "tasks", make one
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        # pass that list of task to the html template
        "tasks": request.session["tasks"]
    })

def add(request):
    if request.method == "POST":
        # request.POST contains all the data of the form
        form = NewTaskForm(request.POST)
        if form.is_valid():
            # accessing data submitted by the user
            task = form.cleaned_data["task"]
            # adding to the list that already exists
            request.session["tasks"] += [task]
            # redirect user to another route. Reverse does -> Given the name of the url, what is the route
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            # return the page with the data to show user its data and what are the errors
            # qn is how will these errors be shown by django?
            return render(request, "tasks/add.html", {
                # input django form here
                "form": form
            })
    else:
        return render(request, "tasks/add.html", {
            "form": NewTaskForm()
        })
