# utils/data_processor.py
import pandas as pd
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def read_file(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            return f"Unsupported file format: {file_path}"
        return f"\nData from {os.path.basename(file_path)}:\n{df.head(10).to_string(index=False)}\n"
    except Exception as e:
        return f"Error reading {file_path}: {e}"

def chunk_data(data, user_query, top_n=5):
    vectorizer = TfidfVectorizer(stop_words='english')
    all_texts = [user_query] + data
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    top_indices = cosine_sim[0].argsort()[-top_n:][::-1]
    return [data[i] for i in top_indices]

def prepare_data(file_paths, crawled_data=None):
    all_data = []
    for file_path in file_paths:
        content = read_file(file_path)
        all_data.append(content)
    if crawled_data:
        all_data.extend(crawled_data)
    return all_data

def load_crawled_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []