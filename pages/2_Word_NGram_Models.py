# User chooses a file from the Gutenberg Project and the program builds a model from it
import os
import random

import streamlit
import nltk
from nltk import ngrams
import gutenberg_util

import ngram_util

book_picker = gutenberg_util.get_book_selector()

model_type = "Words"

ngram_size = streamlit.slider("Pick an ngram size", 1, 10, 3)

build_model_button = streamlit.button("Build model")

model = ngram_util.WordNgramModel(book_picker, ngram_size, ignore_cache=build_model_button)
streamlit.write(f"Model built from {book_picker} with {model.ngram_count} ngrams")

sorted_ngrams = model.ngram_dict
print("Sorted NGrams type:", type(sorted_ngrams))

# Display the ngrams
show_ngrams = streamlit.checkbox("Show ngrams")
if show_ngrams:
    max_ngrams = 100
    for ngram, count in sorted_ngrams.items():
        streamlit.write(f"{ngram}: {count}")
        max_ngrams -= 1
        if max_ngrams == 0:
            break

#generate 30 sample paragraphs
generate_paragraph_button = streamlit.button("Generate paragraph")
if generate_paragraph_button:
    streamlit.write(model.generate_paragraph())