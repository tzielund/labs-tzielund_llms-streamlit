#Memorization Trick based on the shannon game
# To memorize a paragraph, you can use partial context to remember the paragraph.
# You start taking out partial context from the paragraph and try to remember the paragraph.
import random

import streamlit
import gutenberg_util
import re

import ui_util

session_state = streamlit.session_state
if "memorization_trick" not in session_state:
    session_state.memorization_trick = dict()
    session_state.memorization_trick["hidden_paragraph"] = ""
    session_state.memorization_trick["clean_paragraph"] = ""
    session_state.memorization_trick["source_book"] = ""
    session_state.memorization_trick["paragraph_num"] = 0

reset_button = streamlit.button("Reset")
if reset_button:
    session_state.memorization_trick = dict()
    session_state.memorization_trick["hidden_paragraph"] = ""
    session_state.memorization_trick["clean_paragraph"] = ""
    session_state.memorization_trick["guessed_letters"] = set()
    session_state.memorization_trick["source_book"] = ""
    session_state.memorization_trick["paragraph_num"] = 0
    streamlit.rerun()

streamlit.header("Memorization Trick")
streamlit.write("To memorize a paragraph, you can use partial context to remember the paragraph.")

if not session_state.memorization_trick["clean_paragraph"]:
    streamlit.write("This game requires a random paragraph for you to learn.")
    streamlit.write("To get started, we'll select a random passage from a book.")
    # First, select a random passage from one of the available books
    book_selector = gutenberg_util.get_book_selector()
    book_paragraphs = gutenberg_util.get_book_paragraphs(book_selector, include_start_end_tokens=False)
    # Create an index of paragraphs
    book_paragraph_index = {i: p for i, p in enumerate(book_paragraphs)}
    paragraph_picker = streamlit.selectbox("Pick a paragraph", book_paragraph_index)
    raw_paragraph = book_paragraph_index[paragraph_picker]
    # Remove extra whitespace
    clean_paragraph = " ".join(raw_paragraph.split())
    # shorten to 100 characters
    clean_paragraph = clean_paragraph[:350]

    streamlit.write(clean_paragraph)

    proceed = streamlit.button("Use these settings")
    if not proceed:
        streamlit.stop()

    session_state.memorization_trick["clean_paragraph"] = clean_paragraph
    session_state.memorization_trick["guessed_letters"] = set()
    session_state.memorization_trick["source_book"] = book_selector
    session_state.memorization_trick["paragraph_num"] = paragraph_picker
    acknowledge = streamlit.button("Acknowledge")
    if acknowledge:
        streamlit.rerun()
    else:
        streamlit.stop()

streamlit.write("Let's hide some of the message and you try to recite it!")
show_instructions = streamlit.checkbox("Show Instructions?")
if show_instructions:
    streamlit.write("Here's how the game works:")
    streamlit.write("1. We've selected a random passage from a book.")
    streamlit.write("2. We've hidden some of the letters in the passage.")
    streamlit.write("3. Try to recite the passage by guessing the hidden letters.")
    streamlit.write("4. Have fun!")

slider = streamlit.slider("What percent of message to hide?", 0, 100, 5)


def hide_message(param, percent_to_hide):
    # Replace random words with hyphens
    words = param.split()
    hidden_words = []
    hidden_word_id = 0
    for word in words:
        if random.randint(0, 100) < percent_to_hide:
            hidden_word = re.sub(r".", "-", word)
            hidden_hover_link = f"<a href='#{word}'>{hidden_word}</a>"
            hidden_words.append(hidden_hover_link)
            hidden_word_id += 1
        else:
            hidden_words.append(word)
    hidden_message = " ".join(hidden_words)
    return hidden_message


hidden_paragraph = hide_message(session_state.memorization_trick["clean_paragraph"], slider)
clean_paragraph = session_state.memorization_trick["clean_paragraph"]
source_book = session_state.memorization_trick["source_book"]
paragraph_num = session_state.memorization_trick["paragraph_num"]
guessed_letters = session_state.memorization_trick["guessed_letters"]
next_letter_to_guess = hidden_paragraph.find("_")

streamlit.header("The message so far:")


def display_hidden_message(hidden_paragraph):
    streamlit.markdown(hidden_paragraph, unsafe_allow_html=True)

streamlit.write("---")
display_hidden_message(hidden_paragraph)
streamlit.write("---")

streamlit.write("If you are able to recite the message, increase the percentage of the message to hide and try again.")
streamlit.write("If you are unable to recite the message, decrease the percentage of the message to hide and try again.")
