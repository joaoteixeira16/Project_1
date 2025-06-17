from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages


import markdown2
from . import util

class NewSearchForm(forms.Form):
    search = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title of the Page")
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'style': 'max-width: 600px; height: 200px;',
        'placeholder': 'Enter Markdown content...',
    }))

def index(request): 
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            return entry(request, search)
    else:    
        return render(request, "encyclopedia/index.html", {
            "form":NewSearchForm(),
            "entries": util.list_entries()
        })
    
def new_entry(request):
    if request.method == "POST":
        form_new = NewPageForm(request.POST)
        if form_new.is_valid():
            title = form_new.cleaned_data["title"]
            content = form_new.cleaned_data["content"]
            
            if title.upper() in map(str.upper, util.list_entries()):
                messages.error(request,'Page Already Exists')
                return render(request, "encyclopedia/new_entry.html", {
                    "form":NewSearchForm(),
                    "form_new":form_new,
                })
            
            else:
                save = util.save_entry(title,content)
                return entry(request, title)
        else:    
            return render(request, "encyclopedia/new_entry.html", {
                "form":NewSearchForm(),
                "form_new":form_new,
            })
    else:    
        return render(request, "encyclopedia/new_entry.html", {
            "form":NewSearchForm(),
            "form_new":NewPageForm(),
        })
    

def entry(request, name):
    results = []
    for entry in util.list_entries():
        if entry.lower() == name.lower():
            if name != entry:
                return HttpResponseRedirect(reverse("wiki:entry", args=[entry]))

            entry_content = markdown2.markdown(util.get_entry(entry))
            return render(request, 'encyclopedia/entry.html', {
                "form":NewSearchForm(),
                "entry_content":entry_content,
                "entry_name": entry
            })
        elif name in entry:
            results.append(entry)
    
    if len(results) == 0:
        return render(request, 'encyclopedia/error.html', {
            "form":NewSearchForm(),
            "name":name,
        })
    
    return render(request, 'encyclopedia/search.html', {
                "form":NewSearchForm(),
                "entries":results,
                "entry_name": name
            }) 

