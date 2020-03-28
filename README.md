Corpus used: AH/wiki_25

This program uses the nltk python library, which can be installed using
pip install nltk

Then, code can be run using
python index_creation.py		For creating the inverted_index for the corpus
python test_queries.py			For executing a query on this corpus (Note: this asks for user input)

Both the codes output the time taken to run the code, and separately for I/O operations.
index_creation.py also outputs the file sizes of corpus and data files.
test_queries.py also outputs total documents retrieved and list of top K(=10) documents with their computed score.

File structure.py contains constants defining the implementation (such as file locations, number of documents to retrieve, tokenizer regex, etc.) and descriptions of various data structures used throughout.

Corpus used should be placed at ../wiki_25, although this can be changed in structure.py

TO DO

Tokenization
Normalization
Lemmatization?
Stop words?
Accents?

Index construction for large files
Support for arrays
Twin buffer

Storing compression
Gap encoding (gamma?)
Remove delimiters
Different document file?

Spell correction
Non-binary distance?
Keyboard distance?

Update report
