from structure import *
import math, time
from nltk.tokenize.util import regexp_span_tokenize

""" Function declarations """

def tokenize(data, tokenizer_regex, query, normalize=True):

	""" Tokenizes query, returns as generator and updates frequency """

	for token in regexp_span_tokenize(data, tokenizer_regex):
		word = data[token[0] : token[1]]
		if normalize:
			word = word.lower()
		if word in query:
			query[word] += 1
		else:
			query[word] = 1
		yield word

def read_file(data_file, encoding, delimiters, inverted_index, query=None):

	""" Reads data for query and returns number of documents """
	""" Generates document vectors using lnc SMART notation """

	sizes = {}

	file = open(data_file, "r", encoding=encoding)
	number_of_docs = int(file.readline())
	for line in file:
		info = line[:-1].split(delimiters["index"])
		word = info[0]
		if query is None or word in query:
			inverted_index[word] = {}
			for pair in info[1].split(delimiters["term"])[:-1]:
				pair_info = pair.split(delimiters["id"])
				doc_id = int(pair_info[0])
				value = math.log10(1 + int(pair_info[1]))
				inverted_index[word][doc_id] = value
				if doc_id not in sizes:
					sizes[doc_id] = 0
				sizes[doc_id] += math.pow(value, 2)
	file.close()

	for word in inverted_index:
		for doc_id in inverted_index[word]:
			inverted_index[word][doc_id] /= math.sqrt(sizes[doc_id])

	return number_of_docs

def levenshtein_distance(word1, word2):

	""" Computes Levenshtein distance of word1 and word2 """

	matrix = [[0 for j in range(len(word2) + 1)] for i in range(len(word1) + 1)]

	for i in range(len(word1) + 1):
		for j in range(len(word2) + 1):
			if i == j == 0:
				continue
			top = (matrix[i - 1][j] + 1) if i > 0 else len(word2)
			left = (matrix[i][j - 1] + 1) if j > 0 else len(word1)
			diag = (matrix[i - 1][j - 1] + (0 if word1[i - 1] == word2[j - 1] else 1)) if i > 0 and j > 0 else (len(word1) + len(word2))
			matrix[i][j] = min(diag, top, left)

	return matrix[-1][-1]

def spell_correct(incorrect_word, inverted_index, max_edits):

	""" Tries to correct spelling of the word such that it is in inverted_index """

	for word in inverted_index:
		if word[0].lower() == incorrect_word[0].lower() and levenshtein_distance(incorrect_word, word) <= max_edits:
			yield word

def add_word(query, word, frequency, document_frequency, number_of_docs):

	""" Adds words to query vector """

	# only words with idf >= 0.75
	if document_frequency <= number_of_docs / math.pow(10, 0.75):
		if word in query:
			query[word] += frequency
		else:
			query[word] = frequency

	return query

def generate_vector(query, inverted_index, number_of_docs):

	""" Generates query vector using ltc SMART notation and returns vector """

	correct_query = {}

	for word in query:

		# correcting spelling of words in query
		if word in inverted_index:
			add_word(correct_query, word, query[word], len(inverted_index[word]), number_of_docs)
		else:
			print("Word not found: {}".format(word))
			for correct_word in spell_correct(word, inverted_index, 2):
				print("{} autocorrected to {}".format(word, correct_word))
				add_word(correct_query, correct_word, query[word], len(inverted_index[correct_word]), number_of_docs)

	query = correct_query
	size = 0

	for word in query:

		# logarithmic frequency * idf
		term = (1 + math.log10(query[word])) * math.log10(number_of_docs / len(inverted_index[word]))
		query[word] = term
		size += math.pow(term, 2)

	size = math.sqrt(size)

	for word in query:
		query[word] /= size

	return query

def index_elimination(query, inverted_index):

	""" Performs index elimination pruning """

	pruned_docs = []

	for word in query:
		if word in inverted_index:
			for doc_id in inverted_index[word]:
				pruned_docs.append(doc_id)
				yield doc_id

	return pruned_docs

def binary_search(list, element, index):

	""" Binary searches for element in list and returns its index, or the index where it should be inserted """

	start = 0
	end = len(list)
	mid = end
	while end > 0 and end >= start:
		mid = (int)((start + end) / 2)
		if element == list[mid][index]:
			return mid
		elif element > list[mid][index]:
			if end == mid:
				return mid
			end = mid
		else:
			if start == mid:
				return mid + 1
			start = mid

	return mid

def calculate_score(query, doc_id, inverted_index):

	""" Calculates score as angle between query vector and vector represented by doc_id """

	score = 0

	for word in query:
		if doc_id in inverted_index[word]:
			score += inverted_index[word][doc_id] * query[word]

	return score

def retrieve_documents(documents_file, encoding, delimiters, documents):

	""" Retreives documents present in documents list as generator """

	retreived = [{} for i in range(len(documents))]

	file = open(documents_file, "r", encoding=encoding)
	document_index = 0
	for line in file:
		try:
			index = documents.index(document_index)
			document = {}
			for word in line[:-1].split(delimiters["term"])[:-1]:
				info = word.split(delimiters["id"])
				document[info[0]] = info[1]
			retreived[index] = document
		except:
			pass
		document_index += 1

	file.close()

	return retreived

""" main """

if __name__ == "__main__":


	# Reading data

	t = time.time()

	inverted_index = {}
	number_of_docs = read_file(DATA_FILE, ENCODING, DELIMITERS, inverted_index)

	print("Data took {:.5f} seconds to read".format(time.time() - t))

	while True:

		# Input query
		data = input("Enter query: ")

		# Querying

		t = time.time()

		query = {}
		list(tokenize(data, TOKENIZER_REGEX, query))
		query = generate_vector(query, inverted_index, number_of_docs)

		scores = []
		for doc_id in index_elimination(query, inverted_index):
			score = calculate_score(query, doc_id, inverted_index)
			if score > 0:
				index = binary_search(scores, score, 1)
				if index == len(scores) or scores[index][1] != score:
					scores.insert(index, [doc_id, score])

		print("Query took {:.5f} seconds to process".format(time.time() - t))

		# Printing retreived documents

		print("Total documents retreived: {}".format(len(scores)))
		if len(scores) > 0:
			print("Top {} documents".format(min(len(scores), MAX_DOCS_TO_RETRIEVE)))
			index = 0
			for document in retrieve_documents(DOCUMENTS_FILE, ENCODING, DELIMITERS, [term[0] for term in scores[:MAX_DOCS_TO_RETRIEVE]]):
				print("Document: {}, Score: {:.4f}".format(document, scores[index][1]))
				index += 1

		print()

	exit(0)
