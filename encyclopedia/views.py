from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms

import markdown2
from . import util

class NewTaskForm(forms.Form):
    search = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

def index(request): 
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            return entry(request, search)
    else:    
        return render(request, "encyclopedia/index.html", {
            "form":NewTaskForm(),
            "entries": util.list_entries()
        })

def entry(request, name):
    results = []
    for entry in util.list_entries():
        if entry.lower() == name.lower():
            if name != entry:
                return HttpResponseRedirect(reverse("wiki:entry", args=[entry]))

            entry_content = markdown2.markdown(util.get_entry(entry))
            return render(request, 'encyclopedia/entry.html', {
                "form":NewTaskForm(),
                "entry_content":entry_content,
                "entry_name": entry
            })
        elif name in entry:
            results.append(entry)
    
    if len(results) == 0:
        return render(request, 'encyclopedia/error.html', {
            "form":NewTaskForm(),
            "name":name,
        })
    
    return render(request, 'encyclopedia/search.html', {
                "form":NewTaskForm(),
                "entries":results,
                "entry_name": name
            }) 

