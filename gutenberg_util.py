# Utilities for working with cached copies of project gutenberg books
import codecs
import os

import requests
import streamlit

GUTENBERG_CACHE_DIR = "gutenberg"
START_TOKEN = "START_TOKEN"
END_TOKEN = "END_TOKEN"

def get_book_list():
    # Get a list of books available in the cache
    list = os.listdir(GUTENBERG_CACHE_DIR)
    # Eliminate any that don't end with .txt
    list = [b for b in list if b.endswith(".txt")]
    return list

def get_book_selector():
    book_list = get_book_list()
    # Eliminate any that don't end with .txt
    book_list = [b for b in book_list if b.endswith(".txt")]
    return streamlit.selectbox("Select a book", book_list)

DOWNLOAD_URL_PATTERN = "https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
def download_book(book_id):
    # Given a book id, download the book from Project Gutenberg
    url = DOWNLOAD_URL_PATTERN.format(book_id=book_id)
    # Open the url and fetch the text
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return False

def identify_book(book_text):
    # Given a block of text, identify the book title and author
    # The title is on a line starting Title:
    # The author is on a line starting Author:
    title = "Unknown"
    author = "Unknown"
    for line in book_text.split("\n"):
        if line.startswith("Title: "):
            title = line[7:]
        if line.startswith("Author: "):
            author = line[8:]
    return title, author

def book_filename(book_id, title, author):
    filename = f"{GUTENBERG_CACHE_DIR}/{book_id}_{title}_by_{author}.txt"
    # make filename safe
    filename = filename.replace(" ", "_")
    filename = filename.replace(":", "")
    filename = filename.replace("//", "_SLASH_")
    return filename

def save_book_text(book_id, book_text, title, author):
    filename = book_filename(book_id, title, author)
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.write(book_text)

def get_book_text(filename):
    with codecs.open(f"{GUTENBERG_CACHE_DIR}/{filename}", 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
        # get rid of \r\n
        data = data.replace("\r\n", "\n")
    return data

def get_book_paragraphs(filename, include_start_end_tokens=True):
    text = get_book_text(filename)

    paragraphs = text.split("\n\n")
    print("Raw Paragraphs:", len(paragraphs))
    # Remove empty paragraphs
    paragraphs = [p for p in paragraphs if p.strip()]
    print("Non-empty Paragraphs:", len(paragraphs))
    # Strip whitespace from each paragraph
    paragraphs = [p.strip() for p in paragraphs]
    # Shorten multiple whitespace characters
    paragraphs = [" ".join(p.split()) for p in paragraphs]
    # Remove Gutenberg header-- all paragraphs preceding "*** START OF..."
    gutenberg_header_paragraph_index = None
    for i, paragraph in enumerate(paragraphs):
        if "*** START OF" in paragraph:
            gutenberg_header_paragraph_index = i
            break
    if gutenberg_header_paragraph_index is not None:
        paragraphs = paragraphs[gutenberg_header_paragraph_index + 1:]
    print("Header Removed Paragraphs:", len(paragraphs))
    # Remove Gutenberg footer-- all paragraphs following "*** END OF..."
    gutenberg_footer_paragraph_index = None
    for i, paragraph in enumerate(paragraphs):
        if "*** END OF" in paragraph:
            gutenberg_footer_paragraph_index = i
            break
    if gutenberg_footer_paragraph_index is not None:
        paragraphs = paragraphs[:gutenberg_footer_paragraph_index]
    print("Footer Removed Paragraphs:", len(paragraphs))
    # Get rid of paragraphs that start and end with brackets
    paragraphs = [p for p in paragraphs if not (p.startswith("[") and p.endswith("]"))]
    # Get rid of paragraphs that are all uppercase
    paragraphs = [p for p in paragraphs if not p.isupper()]
    print("Non-Uppercase Paragraphs:", len(paragraphs))
    # Get rid of very short paragraphs
    paragraphs = [p for p in paragraphs if len(p) > 32]
    print("Long Paragraphs:", len(paragraphs))
    if include_start_end_tokens:
        # Prefix every paragraph with a START and END token
        paragraphs = [f"{START_TOKEN} {p} {END_TOKEN}" for p in paragraphs]
    return paragraphs


def search_for_books(title_search):
    # Use Gutendex to search for the title
    pass