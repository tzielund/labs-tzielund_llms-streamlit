# Displays the contents of a gutenberg ebook

import streamlit
import os
import gutenberg_util

book_selector = gutenberg_util.get_book_selector()

book_paragraphs = gutenberg_util.get_book_paragraphs(book_selector)

streamlit.json(book_paragraphs)
