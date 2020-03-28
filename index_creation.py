from structure import *
import math, time, os
from nltk.tokenize.util import regexp_span_tokenize

""" Function declarations """

def tokenize(data, tokenizer_regex, inverted_index, documents, normalize=True):

	""" Tokenizes data according to regex given, returns as generator and fills inverted_index """

	state = 0

	doc_id = -1
	title = ""
	prev_index = 0

	for token in regexp_span_tokenize(data, tokenizer_regex):
		original_word = data[token[0] : token[1]]
		if normalize:
			word = original_word.lower()
		else:
			word = original_word

		if word == '':
			continue

		for char in data[prev_index : token[0]]:
			if title is not "":
				title += char

			if char is "'" or char is '"':
				# start and end of attribute values
				if state == 3:
					# word is a doc_id
					state = 4
				elif state == 5:
					# words are title
					state = 6
				elif state == 6:
					# title words have ended

					documents[doc_id]["title"] = title[:-1]

					# print("Title: {}".format(title[:-1]))
					title = ""
					state = 2
			elif char is "<":
				# this and following words are tagged
				if state == 0:
					state = 1
				if word == "doc":
					if state == 1:
						# doc tag used to extract document details
						state = 2
			elif char is ">":
				# this and following words are untagged
				state = 0
		prev_index = token[1]

		if word == "id":
			if state == 2:
				# doc tag's id attribute
				state = 3
		elif word == "title":
			if state == 2:
				# doc tag's title attribute
				state = 5
		elif word.isnumeric():
			if state == 4:

				# word is doc_id

				documents.append({
					"doc_id" : int(word), 
				})
				doc_id += 1

				# print("Current doc: {}".format(word))
				state = 2

		if state == 0:

			# untagged word

			# first encounter
			if word not in inverted_index:
				inverted_index[word] = {}

			# frequency
			if doc_id in inverted_index[word]:
				inverted_index[word][doc_id] += 1
			else:
				inverted_index[word][doc_id] = 1

		elif state == 6:
			title += original_word

		yield word

def read_corpus(corpus_file, encoding, tokenizer_regex, inverted_index, documents):

	""" Reads, tokenizes corpus and returns corpus size """

	file = open(corpus_file, "r", encoding=encoding)
	data = file.read()
	file.close()

	size = os.stat(corpus_file).st_size
	list(tokenize(data, tokenizer_regex, inverted_index, documents))

	return size

def write_data(data_file, encoding, delimiters, inverted_index):

	""" Writes extracted data and returns total size of data """

	file = open(data_file, "w", encoding=encoding)

	# number of documents
	file.write("{}\n".format(len(documents)))

	# inverted_index
	for word in inverted_index:
		file.write("{}{}".format(word, delimiters["index"]))
		for doc_id in inverted_index[word]:
			file.write("{}{}{}{}".format(
				doc_id, delimiters["id"], 
				inverted_index[word][doc_id], 
				delimiters["term"], 
			))
		file.write("\n")
	file.close()

	return os.stat(data_file).st_size

def write_document(documents_file, encoding, delimiters, documents):

	""" Writes document data and returns size of document data """

	# documents
	file = open(documents_file, "w", encoding=encoding)
	for doc in documents:
		for key in doc:
			file.write("{}{}{}{}".format(key, delimiters["id"], doc[key], delimiters["term"]))
		file.write("\n")
	file.close()

	return os.stat(documents_file).st_size

""" main """

if __name__ == "__main__":

	inverted_index = {}
	documents = []

	# Reading corpus

	t = time.time()
	size = 0
	for c in CORPUS_FILES:
		print(c[-2:])
		size += read_corpus(c, ENCODING, TOKENIZER_REGEX, inverted_index, documents)
	print("Data took {:.2f} seconds to process".format(time.time() - t))
	print("Corpus size: {:.2f}mb".format(size / (1024 * 1024)))

	# Writing data

	t = time.time()
	size = write_data(DATA_FILE, ENCODING, DELIMITERS, inverted_index)
	size += write_document(DOCUMENTS_FILE, ENCODING, DELIMITERS, documents)
	print("Data took {:.2f} seconds to write to file".format(time.time() - t))
	print("Total data size: {:.2f}mb".format(size / (1024 * 1024)))

	exit(0)
