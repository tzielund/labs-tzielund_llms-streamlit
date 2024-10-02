import streamlit
import nltk

import gutenberg_util

streamlit.write("Select page from the left sidebar to view its content.")

nltk.download("punkt")

streamlit.write("To start with, find and download some books using the 'book downloader' page")
streamlit.write("You can view the text of a downloaded book in the 'ebook viewer' page")
streamlit.write("Select a passage of text from your book and play the Shannon Game to guess it letter-by-letter")
streamlit.write("Create a model using the 'Word N-Gram Models' page and generate some random text with it")
streamlit.write("Use the 'memorization trick' page to memorize a paragraph of text using the power of context.")

# Ensure at least a couple books are downloaded
essentials = {
    "11": "Alice's Adventures in Wonderland by Lewis Carroll",
    "84": "Frankenstein by Mary Shelley",
    "1513": "Romeo and Juliet by William Shakespeare",
}

book_list = gutenberg_util.get_book_list()
if not book_list:
    streamlit.write("Downloading various well-known books to get you started")
    for book_id in essentials:
        downloaded_text = gutenberg_util.download_book(book_id)
        if downloaded_text:
            title_set, author_set = gutenberg_util.identify_book(downloaded_text)
            gutenberg_util.save_book_text(book_id, downloaded_text, title_set, author_set)
            streamlit.write(f"Downloaded {title_set} by {author_set}")
        else:
            streamlit.write(f"Failed to download book {book_id}")