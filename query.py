import mysql.connector
from mysql.connector import Error
import os
import json
import torch
from embeding import get_bert_embeddings
import numpy as np


def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='youtube_comments_db',
            user='root',  # corrected from 'username' to 'user'
            password=os.getenv("PASSWORD")
        )
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = conn.cursor()
            return conn, cursor

    except Error as e:
        print(f"Error: {e}")
        return None, None


def fetch_embeddings(cursor):
    cursor.execute("SELECT comment, embedding FROM ytcomments")
    rows = cursor.fetchall()
    comments = [row[0] for row in rows]
    embeddings = []
    for row in rows:
        try:
            embedding = json.loads(row[1])
            if isinstance(embedding, list):
                embeddings.append(embedding)
            else:
                print(f"Warning: Skipping embedding that is not a list: {embedding}")
        except json.JSONDecodeError:
            print(f"Warning: Skipping embedding that could not be decoded from JSON: {row[1]}")
    return comments, embeddings


def compute_similarity(embedding1, embedding2):
    embedding1 = torch.tensor(embedding1, dtype=torch.float32)
    embedding2 = torch.tensor(embedding2, dtype=torch.float32)
    cosine_sim = torch.nn.functional.cosine_similarity(embedding1, embedding2, dim=0)
    return cosine_sim.item()


def find_closest_comment(user_input):
    user_embedding = get_bert_embeddings(user_input)
    conn, cursor = connect_to_db()
    if not conn or not cursor:
        return None
    comments, embeddings = fetch_embeddings(cursor)
    cursor.close()
    conn.close()
    similarities = [compute_similarity(user_embedding, emb) for emb in embeddings]
    max_sim_index = np.argmax(similarities)
    closest_comment = comments[max_sim_index]
    return closest_comment


if __name__ == "__main__":
    user_input = input("Enter your text: ")
    closest_comment = find_closest_comment(user_input)
    if closest_comment:
        print(f"The closest comment is: {closest_comment}")
    else:
        print("Could not find any closest comment.")
