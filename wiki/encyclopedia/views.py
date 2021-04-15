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

# runs a search function, found in util.py, and returns any results
def search(request):
    if request.method == "GET":
        form = NewSearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data["search"]

        if util.is_exact_match(search):
            markdowner = Markdown()
            return render(request, "encyclopedia/entry.html", {
                "entry": markdowner.convert(util.get_entry(search))
            })
        return render(request, "encyclopedia/search.html", {
            "results": util.search_entries(search)
        })

# returns main page when accessed
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

    # DO NOT DELETE: /wiki/{{result.md} this belongs in the search.html file.  like this. <li><a href=/wiki/{{result.md}}>{{ result }}</a></li>
    # {% for entry in entries %}
    # <li><a href=/wiki/{{entry.md}}>{{ entry }}</a></li>
    # {% endfor %}

# function to create a new entry 
def new(request):
    if request.method == "POST":
        form = CreateNewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        util.save_entry(title, content)
        return redirect('encyclopedia:entry', entry=title)
    else:
        return render(request, "encyclopedia/new.html", {
            "form": CreateNewForm(),
        })

# queries for the selecged entry
def entry(request, entry):
    entry_page = util.get_entry(entry)

    if entry_page is None:
        return render(request, "encyclopedia/error.html")
    else:
        markdowner = Markdown()
        e = util.get_entry(entry)
        return render(request, "encyclopedia/entry.html", {
            "e": e,
            "entry": markdowner.convert(e),
            "title": entry
            # maybe have an additional argument that displays content, while we have another that displays title
        })

# function that allows user to edit the entry page 
def edit_page(request, entry):
    if request.method == "GET":
        title = entry
        content = util.get_entry(title)
        form = CreateNewForm(
            {"title": title, "content": content})  # passing in
        return render(request, "encyclopedia/edit_page.html", {
            "form": form,
            "title": entry
        })
    form = CreateNewForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
    util.save_entry(title, content)
    return redirect('encyclopedia:entry', entry=title)

# def delete(request, entry):
#     if request.method == "GET":

# create edit template page
# get the entry, but not converted. just markdown
# utilize logic of new function to create a new form to POST to the server.
# redirect to new page
#
