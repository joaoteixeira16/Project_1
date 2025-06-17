from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

import markdown2
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    for entry in util.list_entries():
        if entry.lower() == name.lower():
            if name != entry:
                return HttpResponseRedirect(reverse("entry", args=[entry]))

            entry_content = markdown2.markdown(util.get_entry(entry))
            return render(request, 'encyclopedia/entry.html', {
                "entry_content":entry_content,
                "entry_name": entry
            })
    else:
        if name not in util.list_entries():
            return render(request, 'encyclopedia/error.html', {
                "name":name,
            })

