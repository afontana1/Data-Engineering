# RAG (Retrieval-Augmented Generation) Prompt Generator

Introducing my RAG Prompt Generator! This project is my very own implementation of RAG (Retrieval-Augmented Generation) prompts, a fundamental aspect of natural language processing systems, especially in the realm of question answering. With this tool, you can generate prompts that enhance the accuracy and effectiveness of such systems by incorporating contextual information and user queries. It's a powerful way to improve the performance of question answering models and make them more robust in handling real-world scenarios.
## Features

- **Text Processing:** Tokenizes text into sentences and words using NLTK (Natural Language Toolkit).
- **Lemmatization:** Utilizes NLTK's WordNet Lemmatizer for lemmatization and normalization of text, ensuring consistency and accuracy in word forms.
- **TF-IDF Vectorization:** Employs TF-IDF (Term Frequency-Inverse Document Frequency) vectorization for feature extraction, capturing the importance of terms in a document corpus.
- **Cosine Similarity:** Computes cosine similarity between query text and context chunks, enabling the identification of relevant context for user queries.
- **RAG Prompt Generation:** Generates RAG prompts based on similar context chunks, facilitating effective question answering.

## Requirements

- Python 3.x
- NLTK (Natural Language Toolkit)
- Scikit-learn
- NumPy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ADIITJ/RAG-implementation.git


2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Before running the program, ensure that you have text files (.txt) containing the relevant data from which you want to generate answers. Follow these steps to use the program:
Run the program with the following command:

```
python program.py <uploaded_files> <sentences_per_chunk> <num_chunks>
```

- `<uploaded_files>`: Comma-separated string of filenames containing text data.
- `<sentences_per_chunk>`: Number of sentences to include in each context chunk.
- `<num_chunks>`: Number of context chunks to consider for generating RAG prompts.

## Example

```
python program.py data.txt,more_data.txt 5 3
```

This command will process `data.txt` and `more_data.txt`, considering 5 sentences per chunk and 3 chunks for generating RAG prompts.

## Contributing

Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests on [GitHub](https://github.com/ADIITJ/RAG-implementation).
