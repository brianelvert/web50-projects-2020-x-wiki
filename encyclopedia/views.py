from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.core.exceptions import ValidationError

from . import util

from random import randint
from markdown2 import Markdown


class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    markdown = forms.CharField(widget=forms.Textarea(), label="Markdown Text")
    def clean_title(self):
        title = self.cleaned_data["title"]
        if title in util.list_entries():
            print('{title} already exists')
            raise ValidationError(
                'A wiki for %(title)s already exists.',
                code='already_exists'
            )
        return title

class EditForm(forms.Form):
    title = forms.CharField()
    markdown = forms.CharField()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if util.get_entry(title):
        converted = Markdown().convert(util.get_entry(title))
        return render(request, "wiki/title.html", {
            "content": converted,
            "title": title.capitalize()
        })
    return render(request, "wiki/not_found.html", {
            "title": title.capitalize()
        })

def search(request):
    query=request.GET["q"].lower()
    entries = []
    for entry in util.list_entries():
        entries.append(entry.lower())
    print(query)
    print(entries)
    print(query in entries)
    substring_matches = []
    no_results = True
    if query in entries:
        url = 'wiki/' + query
        return HttpResponseRedirect(url)
        '''
        return render(request, "wiki/title.html", {
            "content": util.get_entry(query),
            "title": query.capitalize()
        })
        '''
    for entry in entries:
        if query in entry:
            substring_matches.append(entry)
            no_results = False
    return render(request, "wiki/search_results.html", {
        "entries":substring_matches,
        "no_results":no_results
    })

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            # ADD THE PAGE (markdown file) to entries directory
            title = form.cleaned_data["title"]
            content = form.cleaned_data["markdown"]
            util.save_entry(title, content)
            # RENDER THE NEW PAGE
            return render(request, "wiki/title.html", {
                "content": util.get_entry(title),
                "title": title.capitalize()
            })
        else:
            invalid_title = form.data["title"]
            return render(request, "wiki/already_exists.html", {
                "title": invalid_title
            })
    else:
        form = CreateForm()
        return render(request, "wiki/create.html", {
            "form": form
        })

def edit(request, title):
    if request.method == "POST":
        # print(request.POST["markdown_editor"])
        # content = request.POST["markdown_editor"]
        print(request.POST.get("title"))
        print(request.POST.get("markdown"))
        form = EditForm(request.POST)
        if form.is_valid():
            util.save_entry(title, form.cleaned_data["markdown"])
            url = '/wiki/' + title
            return HttpResponseRedirect(url)
            '''
            return render(request, "wiki/title.html", {
                "content": util.get_entry(title),
                "title": title.capitalize()
            })
            '''
        else: # JUST PASTED THIS - no rhyme or reason yet
            invalid_title = request.POST.get("title")
            return render(request, "wiki/already_exists.html", {
                "title": invalid_title
            })
    # RENDER A PAGE THAT pre-populates the form
    else:
        return render(request, "wiki/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })

def testing(request):
    list = util.list_entries()
    end = len(list) - 1
    pick = randint(0,end)
    picked = list[pick]
    context = {'list':list, 'picked':picked}
    return render(request, "testing.html", context)

def random(request):
    list = util.list_entries()
    end = len(list) - 1
    pick = randint(0,end)
    picked = list[pick]
    url = "/wiki/" + picked
    return HttpResponseRedirect(url)