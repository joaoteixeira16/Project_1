from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
import markdown2
from . import util
import random

class NewSearchForm(forms.Form):
    search = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title of the Page")
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'style': 'max-width: 600px; height: 200px;',
        'placeholder': 'Enter Markdown content...',
    }))

class EditPageFormHidden(forms.Form):
    title = forms.CharField().hidden_widget()
    content = forms.CharField(widget=forms.Textarea()).hidden_widget()

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'style': 'max-width: 600px; height: 200px;',
    }))



def index(request): 
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            request.method = ""
            return entry(request, search)
    else:    
        return render(request, "encyclopedia/index.html", {
            "form":NewSearchForm(),
            "entries": util.list_entries()
        })
    
def random_entry(request): 
    random_entry_name = random.choice(util.list_entries())
    random_entry_content = markdown2.markdown(util.get_entry(random_entry_name))
    return render(request, 'encyclopedia/entry.html', {
        "form":NewSearchForm(),
        "entry_content":random_entry_content,
        "entry_name": random_entry_name,
        "form_edit":EditPageFormHidden()
    })
    
def edit_page(request, name):
    if request.method == "POST":
        form_edit = EditPageForm(request.POST)
        if form_edit.is_valid():
            content = form_edit.cleaned_data["content"]
            save = util.save_entry(name,content)
            request.method = ""
            return entry(request, name)
        else:    
            return render(request, "encyclopedia/edit_page.html", {
                "form":NewSearchForm(),
                "form_edit":form_edit,
            })
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
                request.method = ""
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
    if request.method == "POST":
        entry_content = util.get_entry(name)
        
        form = EditPageForm(initial={'content': entry_content})
        return render(request, 'encyclopedia/edit_page.html', {
                "form":NewSearchForm(),
                "entry_content":entry_content,
                "entry_name": name,
                "form_new":form
            })

    results = []
    for entry in util.list_entries():
        if entry.lower() == name.lower():
            if name != entry:
                return HttpResponseRedirect(reverse("wiki:entry", args=[entry]))

            entry_content = markdown2.markdown(util.get_entry(entry))
            return render(request, 'encyclopedia/entry.html', {
                "form":NewSearchForm(),
                "entry_content":entry_content,
                "entry_name": name,
                "form_edit":EditPageFormHidden()
            })
        elif name.lower() in entry.lower():
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

