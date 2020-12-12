from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.files import File
from . import util
from markdown2 import Markdown
from django.http import Http404
import os
from django.views.generic.edit import UpdateView


class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search", required=False,
                             widget=forms.TextInput
                             (attrs={'placeholder': 'Search Encyclopedia'}))


class CreateNewForm(forms.Form):
    title = forms.CharField(label="Entry Title",
                            max_length=25)
    content = forms.CharField(widget=forms.Textarea)


def search(request):
    if request.method == "GET":
        form = NewSearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data["search"]
        return render(request, "encyclopedia/search.html", {
            "results": util.search_entries(search)
        })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

    # DO NOT DELETE: /wiki/{{result.md} this belongs in the search.html file.  like this. <li><a href=/wiki/{{result.md}}>{{ result }}</a></li>
    # {% for entry in entries %}
    # <li><a href=/wiki/{{entry.md}}>{{ entry }}</a></li>
    # {% endfor %}


def new(request):
    if request.method == "POST":
        form = CreateNewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        util.save_entry(title, content)
        # maybe provide this argument as context?
        return redirect('encyclopedia:entry', entry=title)
    else:
        return render(request, "encyclopedia/new.html", {
            "form": CreateNewForm(),
        })


def entry(request, entry):
    entry_page = util.get_entry(entry)

    if entry_page is None:
        return render(request, "encyclopedia/error.html")
    else:
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(entry))
            # maybe have an additional argument that displays content, while we have another that displays title
        })
