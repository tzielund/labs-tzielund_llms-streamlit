#Shannon Game allows user to guess letters in a hidden passage
#similar to the game first played by Claude and Betty Shannon in 1948
import time

import streamlit
import gutenberg_util
import re

import ui_util

def display_hidden_message(hidden_message):
    # Wrap the hidden message in a <pre> tag to preserve whitespace
    number_of_blanks = hidden_message.count("_")
    streamlit.markdown(f"<pre>{hidden_message} ({number_of_blanks} remaining)</pre>", unsafe_allow_html=True)


session_state = streamlit.session_state
if "shannon_game" not in session_state:
    session_state.memorization_trick = dict()
    session_state.memorization_trick["hidden_paragraph"] = ""
    session_state.memorization_trick["clean_paragraph"] = ""
    session_state.memorization_trick["guessed_letters"] = set()
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

streamlit.image("media/claude_and_betty.jpeg")
streamlit.header("Shannon Game")
# Show the image of cluade and betty shannon from media folder
streamlit.write("Claude and Betty Shannon challenge you to play their 'newlywed game'")

if not session_state.memorization_trick["hidden_paragraph"]:
    streamlit.write("This game requires a hidden message for you to guess.")
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
    # Remove everything that isn't a letter or a space or a period
    clean_paragraph = "".join([c for c in clean_paragraph if c.isalpha() or c.isspace() or c == "."])
    # Uppercase the paragraph
    clean_paragraph = clean_paragraph.upper()
    # shorten to 100 characters
    clean_paragraph = clean_paragraph[:50]

    # Hidden passage: replace every letter with an underscore
    hidden_paragraph = re.sub(r".", "_", clean_paragraph)
    display_hidden_message(hidden_paragraph)
    show_hidden = streamlit.checkbox("Show original message also?")
    if show_hidden:
        streamlit.write(f"Hidden message:")
        streamlit.write(clean_paragraph)

    proceed = streamlit.button("Use these settings")
    if not proceed:
        streamlit.stop()

    session_state.memorization_trick["hidden_paragraph"] = hidden_paragraph
    session_state.memorization_trick["clean_paragraph"] = clean_paragraph
    session_state.memorization_trick["guessed_letters"] = set()
    session_state.memorization_trick["source_book"] = book_selector
    session_state.memorization_trick["paragraph_num"] = paragraph_picker
    acknowledge = streamlit.button("Acknowledge")
    if acknowledge:
        streamlit.rerun()
    else:
        streamlit.stop()

streamlit.write("Let's play the game!")
show_instructions = streamlit.checkbox("Show Instructions?")
if show_instructions:
    streamlit.write("Here's how the game works:")
    streamlit.write("1. We've selected a random passage from a book.")
    streamlit.write("2. We've hidden all the letters in the passage.")
    streamlit.write("3. You are trying to guess only the first letter in the passage, one letter at a time.")
    streamlit.write("4. If you guess a letter correctly, we'll reveal it in the passage.")
    streamlit.write("5. If you guess a letter incorrectly, we'll keep track of it.")
    streamlit.write("6. You can guess until you've revealed all the letters in the passage.")
    streamlit.write("7. Have fun!")

hidden_paragraph = session_state.memorization_trick["hidden_paragraph"]
clean_paragraph = session_state.memorization_trick["clean_paragraph"]
source_book = session_state.memorization_trick["source_book"]
paragraph_num = session_state.memorization_trick["paragraph_num"]
guessed_letters = session_state.memorization_trick["guessed_letters"]
next_letter_to_guess = hidden_paragraph.find("_")

streamlit.header("The message so far:")
display_hidden_message(hidden_paragraph)

# Display the guessed letter
streamlit.write("Here are the letters you've guessed so far for the first available blank space:")
guessed_letters = session_state.memorization_trick["guessed_letters"]

# Ask the user to guess the next letter
streamlit.write("What letter would you like to guess next?")
next_letter = ui_util.qwerty_buttons(guessed_letters)

if next_letter == "hint":
    streamlit.header(f"Hint: try '{clean_paragraph[next_letter_to_guess]}'")
    time.sleep(2)
    streamlit.rerun()

if not next_letter:
    streamlit.stop()

if clean_paragraph[next_letter_to_guess] == next_letter:
    hidden_paragraph = hidden_paragraph[:next_letter_to_guess] + next_letter + hidden_paragraph[next_letter_to_guess + 1:]
    session_state.memorization_trick["hidden_paragraph"] = hidden_paragraph
    guessed_letters = set()
    session_state.memorization_trick["guessed_letters"] = guessed_letters
    streamlit.header(f"Yes!!! '{next_letter}' is correct!")
    time.sleep(1)
    streamlit.rerun()
else:
    guessed_letters.add(next_letter)
    session_state.memorization_trick["guessed_letters"] = guessed_letters
    streamlit.header(f"'Nope!  '{next_letter}' is not in the message.")
    time.sleep(1)
    streamlit.rerun()


