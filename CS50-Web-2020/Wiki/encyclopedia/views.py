from django import forms
from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.utils.safestring import mark_safe
from random import randint 
import markdown2

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="Search..", required=False)

class NewForm(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(label="Text", widget=forms.Textarea)

class EditForm(forms.Form):
    text = forms.CharField(label="New Text", widget=forms.Textarea, initial='')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

# return page of specific title
def title(request, title):
    if util.get_entry(title) is None:
        return HttpResponseNotFound('<h1>Error 404 Page not found</h1>')

    return render(request, "encyclopedia/title.html", {
        "title": title.capitalize(),
        "entry": markdown2.markdown(util.get_entry(title)),
        "form": SearchForm()
    })

# return links to all pages from search
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            # search for respective markdown entries
            entries = util.list_entries()
            upper_entries = [x.upper() for x in entries]
            indices = [i for i, s in enumerate(upper_entries) if search.upper() in s]
            results=[]
            for i in indices:
                results.append(entries[i])
            return render(request, "encyclopedia/search.html", {
                "results": results
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
        })

# Creates new page and return that specific page
def new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if title.upper() in [x.upper() for x in util.list_entries()]:
                return render(request, "encyclopedia/error.html", {
                    "errorMessage": "The title \"" + title + "\" already exists. Please use another title",
                    "form": SearchForm()
                })
            else:            
                util.save_entry(title, text)
                return render(request, "encyclopedia/title.html", {
                    "title": title.capitalize(),
                    "entry": markdown2.markdown(util.get_entry(title))
                })

        return render(request, "encyclopedia/new.html", {
            "form": SearchForm(),
            "newForm": NewForm()
        })
    else:     
        return render(request, "encyclopedia/new.html", {
            "form": SearchForm(),
            "newForm": NewForm()
        })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            newtext = form.cleaned_data["text"]      
            util.save_entry(title, newtext)
            return render(request, "encyclopedia/title.html", {
                "title": title.capitalize(),
                "entry": markdown2.markdown(util.get_entry(title)),
                "form": SearchForm()
            })

        return render(request, "encyclopedia/title.html", {
            "title": title.capitalize(),
            "entry": markdown2.markdown(util.get_entry(title)),
            "form": SearchForm()
        })
    else:     
        EditFormN = EditForm(initial={'text': util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            "form": SearchForm(),
            "editForm": EditFormN,
            "title": title,
            "text": util.get_entry(title)
        })

def random(request):
    entries = util.list_entries()
    index = randint(0, len(entries)-1)
    title = entries[index]
    return render(request, "encyclopedia/title.html", {
    "title": title.capitalize(),
    "entry": markdown2.markdown(util.get_entry(title)),
    "form": SearchForm()
    })