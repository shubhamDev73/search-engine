import os

""" Files """

CORPUS_FILE = os.path.join(os.path.dirname(os.getcwd()), "wiki_25")
CORPUS_FILES = [os.path.join(os.path.join(os.path.dirname(os.getcwd()), "AH"), "wiki_{:02}".format(i)) for i in range(100)]
DATA_FILE = os.path.join(os.getcwd(), "data")
DOCUMENTS_FILE = os.path.join(os.getcwd(), "documents")
ENCODING = "utf-8"

""" Implementation data """

TOKENIZER_REGEX = r"\s|[“”’`~!@#$%^&_()\[\]{}|:;'\"<,>.?+-/*=]+"
DELIMITERS = {
	"index" : ":", 
	"term" : ";", 
	"id" : "~", 
}
""" Delimiter description

inverted_index = { word : { doc_id : frequency } } }

will be written in file as:
word{index}doc_id{id}frequency{term}doc_id{id}...
.
.
.

{} represents type of delimiter """

MAX_DOCS_TO_RETRIEVE = 10

""" Data structures """

# corpus
documents = [
	# {
	# 	"doc_id" : doc_id
	# 	"title" : title
	# }
]
inverted_index = {
	# word : {
	# 	doc_id : frequency
	# }
}

# query
query = {
	# word : frequency
}
scores = [
	# [doc_id, score_cos]
]
