# Vector space based ranked information retrieval system

## Description

The IR system built takes the corpus, reads it, tokenizes it based on a regex, and in the same pass also creates the inverted_index for all words. During tokenization, whitespaces are removed and all characters are converted to lower case (normalization). It then takes the query, reads the inverted_index, calculates cosine similarity score based on `lnc.ltc SMART notation` for all documents containing query words and then prints the **top K(=10)** documents according to this computed score.

Additionally, it performs spell correction on terms not present in inverted_index, by finding words starting with the same character as misspelled word and whose Levenshtein distance is <= 2. Then, it automatically replaces misspelled word with all these 'correct' words. Although, this spell correction has drawbacks (such as 'fllew' gets corrected to 'fellow') and needs to be improved.

The system also disregards words with idf (inverse document frequency) < **0.75** (this is equivalent to words present in more than roughly **17.78%** of documents), as they are considered common words, and have little impact on the overall query. This reduces total documents retrieved, which in turn improves the speed of the system.

### Corpus used: AH/wiki_25

## Installation and running

This program was written in `python 3.7` and it uses the nltk python library, which can be installed using `pip install nltk`.

Then, code can be run using `python index_creation.py` for creating the inverted_index for the corpus (**Note**: Corpus used should be placed at **../wiki_25**, although this can be changed in `structure.py`)
Then, use `python test_queries.py` for executing a query on this corpus (**Note**: this asks for user input)

### Some test queries

- american film the raven
- cancer victim
- american basketball player
- rock song

## Output

Both the programs output the time taken to run the code and separately for I/O operations.
`index_creation.py` also outputs the file sizes of corpus and data files.
`test_queries.py` also outputs total documents retrieved and list of top K(=10) documents with their computed score.

## Files

- **\__init\__.py** : to mark the folder and python files present in it as modules.
- **data (automatically created by `index_creation.py`)** : stores the inverted_index formed.
- **documents (automatically created by `index_creation.py`)** : stores document details dictionary.
- **index_creation.py** : read the corpus and creates inverted_index, stores it in data file and stores document details in documents file.
- **structure.py** : contains values for file paths, tokenizer regex, delimiters used while storing files, number of documents to retrieve, and also descriptions of the data structures used.
- **test_queries.py** : reads user input query, data and document files, and returns top K documents according to cosine similarity score computed.

## Limitations

- The tokenizer uses simple regex to tokenize, hence, it’s not very effective.
- Almost all non-alphanumeric characters are ignored.
- No lemmatization is done, which can improve scoring.
- data and document files are stored in human readable format (utf-8), instead of actual values of numbers. This way, no compression can be applied on these files and hence their sizes are not optimized.
- If any of the delimiters used in data and document files is present in any of the words in inverted_index, there might be some problems in reading those files.
- Documents' id present in id attribute of doc tag is ignored in code (it is stored in documents file) and `doc_id` used in code starts with 0 and increments by 1 each time a new doc tag is read. This is done to reduce the size of inverted_index stored on the disk.

## TO DO

- Correct information extraction from **<doc> tag**.
- Improve tokenization to take into account floating numbers, dates, currency, accents, foreign language words, etc.
- Lemmatization - it is the process of converting all words to their base form (like books and book should be considered same, etc.)
- Twin buffer for index contruction as currently, for large files, it may lead to `MemoryError`.
- Convert stored indices in binary form so that it can be compressed.
- Compress stored indices using gap encoding with gamma codes for all document ids.
- Improve spell correction by adding weights to steps taken in calculating Levenshtein distance corresponding to keyboard distance.
- Remove different document file and store all relevant data in a single file only.
