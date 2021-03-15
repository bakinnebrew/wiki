import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from . import views
import os


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                       for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def is_exact_match(title):
    result = list(filter(lambda entry: title == entry, list_entries()))
    # returnVal = len(result) == 1
    # return returnVal

    if len(result) == 1:
        return True
    else:
        return False

    # return len(result) == 1


def search_entries(title):
    """
    Retieves a list of entries by title as they compare to the user-entered search entry
    """
    # return list(filter(filter_entries, list_entries()))
    return list(filter(lambda entry: title in entry, list_entries()))

    # print('title: ' + title)
    # for res in result:
    #     print('result: ' + res)
    # for filename in default_storage.listdir("entries"):
    # if title == filename:
    #     return filename
    # return list(sorted(re.sub(r"\.md$", "", title)
    #              for title in filename))
    # compare search entry with current entry filenames
    # if none compare, display like terms
    # if no like terms, display, no results found
    # else, display the desired search item


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

# def delete_entry(title):
#     """
#     Deletes an entry
#     """
#     get_entry(title)
