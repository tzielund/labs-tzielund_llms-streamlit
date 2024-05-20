# Build an n-gram language model from a text file
import json
import os
import random

import nltk
import streamlit
import gutenberg_util

MODEL_CACHE_DIR = "model_cache"
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)

class WordNgramModel:

    def __init__(self, filename, ngram_size, ignore_cache=False):
        self.ngram_size = ngram_size
        self.filename = filename
        self.model_filename = f"{MODEL_CACHE_DIR}/word_{ngram_size}_{filename}.model"
        if not ignore_cache and os.path.exists(self.model_filename):
            self.read_model()
            return

        # Read the file
        paragraphs = gutenberg_util.get_book_paragraphs(filename)
        print("Paragraphs:", len(paragraphs))
        # streamlit.json(paragraphs[:10])

        # Tokenize the text
        self.ngram_dict = dict()
        for paragraph in paragraphs:
            tokens = nltk.word_tokenize(paragraph)
            # prepend n-1 start tokens
            tokens = [gutenberg_util.START_TOKEN] * (ngram_size - 2) + tokens
            # streamlit.write(tokens) # A list of strings
            ngrams = nltk.ngrams(tokens, ngram_size)
            for ngram in ngrams:
                ngram_key = "|".join(ngram)
                # streamlit.markdown(f"* {ngram_key}")
                if ngram_key in self.ngram_dict:
                    self.ngram_dict[ngram_key] += 1
                else:
                    self.ngram_dict[ngram_key] = 1
            for ngram in ngrams:
                ngram_key = "|".join(ngram)
                if ngram_key in self.ngram_dict:
                    self.ngram_dict[ngram_key] += 1
                else:
                    self.ngram_dict[ngram_key] = 1
        print("Ngrams:", len(self.ngram_dict))

        # Sort the ngrams
        self.ngram_dict = dict(sorted(self.ngram_dict.items(), key=lambda x: x[1], reverse=True))

        # Count the number of ngrams
        self.ngram_count = len(self.ngram_dict)
        self.ngram_total = 0
        for key in self.ngram_dict:
            self.ngram_total += self.ngram_dict[key]

        self.write_model()

    def read_model(self):
        print(f"Reading model from {self.model_filename}")
        with open(self.model_filename) as f:
            data_struct = json.load(f)
            self.ngram_size = data_struct["ngram_size"]
            self.ngram_dict = data_struct["ngram_dict"]
            self.ngram_count = data_struct["ngram_count"]
            self.ngram_total = data_struct["ngram_total"]

    def write_model(self):
        print(f"Writing model to {self.model_filename}")
        with open(self.model_filename, "w") as f:
            data_struct = {
                "ngram_size": self.ngram_size,
                "ngram_dict": self.ngram_dict,
                "ngram_count": self.ngram_count,
                "ngram_total": self.ngram_total
            }
            json.dump(data_struct, f, indent=4)

    def string_to_context_key(self, contextString):
        # Pull out the last n-1 tokens and return them as a | delimited string
        if not contextString:
            # n-1 start tokens
            return "|".join([gutenberg_util.START_TOKEN] * (self.ngram_size - 1))
        tokens = nltk.word_tokenize(contextString)
        # if less than ngram_size tokens, add start token
        if len(tokens) < self.ngram_size:
            tokens = [gutenberg_util.START_TOKEN] * (self.ngram_size - len(tokens)) + tokens
        return "|".join(tokens[-(self.ngram_size - 1):]) + "|"

    def find_ngrams_matching_context(self, contextKey):
        matching_ngrams = dict()
        for ngram_key in self.ngram_dict.keys():
            if ngram_key[:len(contextKey)] == contextKey:
                matching_ngrams[ngram_key] = self.ngram_dict[ngram_key]
        return matching_ngrams

    def predict_next_word(self, contextKey):
        print(f"Predicting next word for {contextKey}")
        matching_ngrams = self.find_ngrams_matching_context(contextKey)
        print("Matching ngrams:", len(matching_ngrams))
        if not matching_ngrams:
            raise Exception(f"No matching ngrams for {contextKey}")
            # matching_ngrams = self.ngram_dict
        total = sum(matching_ngrams.values())
        choice = random.randint(0, total - 1)
        print(f"Total: {total}, Choice: {choice}")
        for key in matching_ngrams:
            choice -= matching_ngrams[key]
            if choice < 0:
                print(f"Choice: {choice}, Key: {key}")
                last_word = key.split("|")[-1]
                print(f"Last Word: {last_word}")
                return last_word
        return "BAR"

    def generate_paragraph(self):
        max_tokens = 1000
        paragraph = ""
        total_tokens = 0
        done = False
        while not done:
            contextKey = self.string_to_context_key(paragraph)
            next_word = self.predict_next_word(contextKey)
            if next_word == gutenberg_util.END_TOKEN:
                done = True
                break
            paragraph += next_word + " "
            total_tokens += 1
            if total_tokens > max_tokens:
                done = True # Prevent infinite loops
        return paragraph