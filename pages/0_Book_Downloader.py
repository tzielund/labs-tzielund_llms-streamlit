# Select a book to download

import streamlit
import os
import gutenberg_util

streamlit.write("Use this page to download books from the Gutenberg Project and save them to the cache.")
streamlit.write("You can then build a model from the downloaded books.")
streamlit.write("Go to https://www.gutenberg.org to find a book and then find it's ID in the URL.")
streamlit.write("Example: https://www.gutenberg.org/ebooks/2641 has an ID of 2641.")

book_id = streamlit.text_input("Enter a book ID to download")
do_id = streamlit.button("Download")
if not do_id:
    streamlit.write("Some example book ID's to get you started:")
    streamlit.markdown("11: Alice's Adventures in Wonderland by Lewis Carroll")
    streamlit.markdown("21: Aesop's Fables by Aesop")
    streamlit.markdown("84: Frankenstein by Mary Shelley")
    streamlit.markdown("1342: Pride and Prejudice by Jane Austen")
    streamlit.markdown("1513: Romeo and Juliet by William Shakespeare")
    streamlit.markdown("2701: Moby Dick by Herman Melville")
    streamlit.markdown("25717: The Decline and Fall of the Roman Empire by Edward Gibbon")

    # List books already downloaded
    book_list = gutenberg_util.get_book_list()
    if book_list:
        streamlit.write("Books already downloaded:")
        streamlit.json(book_list)
    else:
        streamlit.write("Nothing downloaded yet")

    streamlit.stop()
downloaded_text = gutenberg_util.download_book(book_id)
if downloaded_text:
    title_set, author_set = gutenberg_util.identify_book(downloaded_text)
    gutenberg_util.save_book_text(book_id, downloaded_text, title_set, author_set)
    streamlit.write(f"Downloaded {title_set} by {author_set}")
else:
    streamlit.write(f"Failed to download book {book_id}")


