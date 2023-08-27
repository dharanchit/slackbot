from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import pickle
import os
from pathlib import Path
from app.constants.projects import PROJECTS_LIST
from app.constants.users import USER_NEW

current_dir = Path(__file__).parent

# Load the pre-trained model and tokenizer
def load_model_and_tokenizer(model_path, tokenizer_path):
    model = tf.keras.models.load_model(model_path)
    with open(tokenizer_path, 'rb') as tokenizer_file:
        tokenizer = pickle.load(tokenizer_file)
    return model, tokenizer

# Function to extract information from text
def extract_info_from_text(text):
    ticket_pattern = r'\b[A-Z]+-[A-Z0-9]+\b'
    name_pattern = r'\bto\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'

    extracted_tickets = re.findall(ticket_pattern, text, re.IGNORECASE)  # Make it case-insensitive
    ticketNumber = extracted_tickets[0] if extracted_tickets else ""

    match = re.search(name_pattern, text, re.IGNORECASE)  # Make it case-insensitive
    userName = match.group(1).title() if match else ""

    matching_projects = []
    for project in PROJECTS_LIST:
        project_name = project["project_name"].lower()
        project_key = project["key"].lower()
        if project_name in text.lower() or project_key in text.lower():
            matching_projects.append(project)

    return {"Assignee":userName, "TicketNo":ticketNumber, "MatchingProjects": matching_projects}

# Function to make predictions using the loaded model and tokenizer
def make_predictions(model, tokenizer, max_sequence_length, test_data):
    test_sequences = tokenizer.texts_to_sequences(test_data)
    padded_test_sequences = pad_sequences(test_sequences, maxlen=max_sequence_length, padding='post')
    predictions = model.predict(padded_test_sequences)

    result = []
    for i, prediction in enumerate(predictions):
        if prediction >= 0.5:
            label = "Update Ticket"
        else:
            label = "Create Ticket"
        
        info_dict = extract_info_from_text(test_data[i])
        info_dict["Text"] = test_data[i]
        info_dict["Task"] = label
        result.append(info_dict)
    
    return result

# Paths for the saved model and tokenizer
model_path = str(current_dir) + '/ticket_prediction_model.h5'
tokenizer_path = str(current_dir) + '/tokenizer.pkl'



# Load the model and tokenizer
loaded_model, loaded_tokenizer = load_model_and_tokenizer(model_path, tokenizer_path)

# # Maximum sequence length
max_sequence_length = loaded_model.layers[0].input_length

# # Make predictions
def generate_results(user_input):
    predictions = make_predictions(loaded_model, loaded_tokenizer, max_sequence_length, user_input)
    return predictions

def get_closest_match_by_name(reporter_name):
    texts = [entry['displayName'] for entry in USER_NEW]
    texts.append(reporter_name)  # Add the target_string to the list of texts
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    target_vector = tfidf_matrix[-1]  # The last vector corresponds to the target_string
    similarities = cosine_similarity(target_vector, tfidf_matrix[:-1])
    
    closest_index = similarities.argmax()
    closest_match = USER_NEW[closest_index]
    
    return closest_match
