import streamlit
import nltk

streamlit.write("Select page from the left sidebar to view its content.")

nltk.download("punkt")

streamlit.write("To start with, find and download some books using the 'book downloader' page")
streamlit.write("You can view the text of a downloaded book in the 'ebook viewer' page")
streamlit.write("Select a passage of text from your book and play the Shannon Game to guess it letter-by-letter")
streamlit.write("Create a model using the 'build model from gutengerg file' page and generate some random text with it")
streamlit.write("Use the 'memorization trick' page to memorize a paragraph of text using the power of context.")
