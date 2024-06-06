import streamlit
import nltk

streamlit.write("Select page from the left sidebar to view its content.")

nltk.download("punkt")

streamlit.write("To start with, find and download some books using the 'book downloader' page")
streamlit.write("You can view the text of a downloaded book in the 'ebook viewer' page")
streamlit.write("Finally, create a model using the 'build model from gutengerg file' page and generate some random text with it")
