import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sys
import string
import re
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
lemmatizer = WordNetLemmatizer()

chunk_centroids = []
chunks = []

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def LemNormalize(text):
    tokens = word_tokenize(text.lower().translate(dict((ord(punct), None) for punct in string.punctuation)))
    return [lemmatizer.lemmatize(token) for token in tokens]

def break_into_chunks(tfidf_vectorizer, sentences, x):
    chunks = []
    for i in range(len(sentences)):
        chunk_start = max(0, i - x)
        chunk_end = min(len(sentences), i + x+1)
        base_sentence = sentences[i]
        similar_sentences = find_similar_sentence(base_sentence, sentences[chunk_start:chunk_end], tfidf_vectorizer, x)
        chunks.append(similar_sentences)
        i = i + x//2
    return chunks

def find_similar_sentence(base_sentence, candidate_sentences, tfidf_vectorizer, x):
    query_vector = tfidf_vectorizer.transform([base_sentence])
    distances = []
    for sentence in candidate_sentences:
        sentence_vector = tfidf_vectorizer.transform([sentence])
        distance = cosine_similarity(query_vector, sentence_vector)[0][0]
        distances.append((distance, sentence))
    distances.sort(key=lambda x: x[0], reverse=True)
    similar_sentences = [sentence for _, sentence in distances[:x]]  # Return top 2 similar sentences
    return similar_sentences

def get_file_contents(uploaded, x):
    global chunks
    global chunk_centroids
    sentences = []
    for filename in uploaded:
        print(f"Uploaded file: {filename}")
        with open(filename, 'r', errors='ignore') as file:
            raw_text = file.read()
            raw_sentences = sent_tokenize(raw_text)
            lemmatized_sentences = []
            for raw_sentence in raw_sentences:
                lemmatized_sentence = ' '.join(LemNormalize(raw_sentence))
                lemmatized_sentences.append(lemmatized_sentence)
            sentences += lemmatized_sentences

    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    chunks = break_into_chunks(tfidf_vectorizer, sentences, x)

    for chunk in chunks:
        chunk_vector = tfidf_vectorizer.transform(chunk)
        chunk_centroid = np.asarray(chunk_vector.mean(axis=0)).reshape(-1)
        chunk_centroids.append(chunk_centroid)


def find_similar_sentences(query_text, num_chunks):
    query_vector = tfidf_vectorizer.transform([query_text])
    distances = []
    for i in range(len(chunk_centroids)):
        distance = cosine_similarity(query_vector, chunk_centroids[i].reshape(1, -1))[0][0]
        distances.append((distance, i))
    distances.sort(key=lambda x: x[0], reverse=True)
    top_chunk_indices = [i for _, i in distances[:num_chunks]]  # Convert indices to integers
    similar_sentences = [chunks[index] for index in top_chunk_indices]
    return similar_sentences

def convert_data_to_list(data):
    unique_strings = set()
    for sublist in data:
        for string in sublist:
            unique_strings.add(string)
    return list(unique_strings)

def generate_rag_prompt(query_text, similar_sentences):
    prompt = f"Answer the question: '{query_text}' based on the following context:\n"
    for sentence in similar_sentences:
        prompt += f"{sentence}. "
    return prompt

def response(query_text, num_chunks):
    query_text = preprocess_text(query_text)
    similar_sentences = find_similar_sentences(query_text, num_chunks)
    similar_sentences = convert_data_to_list(similar_sentences)
    rag_prompt = generate_rag_prompt(query_text, similar_sentences)
    return rag_prompt

def main(uploaded, sentences_per_chunk, num_chunks):
    get_file_contents(uploaded, sentences_per_chunk)
    query_text = ""
    while True:
        query_text = input("You: ")
        if preprocess_text(query_text) == "bye":
            break
        prompt = response(query_text,num_chunks)
        print("Bot: RAG prompt-")
        print(prompt)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python program.py <uploaded_files> <sentences_per_chunk> <num_chunks>")
        sys.exit(1)
    
    uploaded_files = sys.argv[1].split(',')
    sentences_per_chunk = int(sys.argv[2])
    num_chunks = int(sys.argv[3])
    main(uploaded_files, sentences_per_chunk, num_chunks)
