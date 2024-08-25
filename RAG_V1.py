import openai
from sentence_transformers import SentenceTransformer, util
import torch
import pickle
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

openai.api_key = api_key

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


def extract_translation_info(json_string):
    data = json.loads(json_string)

    origin_language = data.get("origin_language", "")
    translation = data.get("translation", "")

    return origin_language, translation


def correct_prompt(prompt):
    # Use OpenAI API with the new interface
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """Correct this prompt without adding any new information.
            It will be directed to a chatbot, so provide the corrected prompt directly.
            If the prompt contains "casa" or "casablanca" without specifying "Voyageurs" or "port," replace it with "casa port" only if neither "port" nor "Voyageurs" is specified.
            You must translate from any of these languages: English, French, or arabic to English. If the language is not one of these, say that you cannot answer. Always provide and only provide a JSON file with:
                - "origin_language": The language of the original text (e.g., French, English)
                - "translation": The translation to English
            """},

            {"role": "user", "content": prompt}
        ],
    )
    return extract_translation_info(response.choices[0].message['content'].strip())


# Function to load or compute embeddings
def load_or_compute_embeddings(file_path, embedding_file):
    if os.path.exists(embedding_file):
        with open(embedding_file, 'rb') as f:
            lines, line_embeddings = pickle.load(f)
    else:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        line_embeddings = model.encode(lines, convert_to_tensor=True)
        with open(embedding_file, 'wb') as f:
            pickle.dump((lines, line_embeddings), f)
    return lines, line_embeddings


def get_most_valuable_sentences(lines, line_embeddings, query):
    # Encode the query
    query_embedding = model.encode([query], convert_to_tensor=True)

    # Compute cosine similarities
    similarities = util.pytorch_cos_sim(query_embedding, line_embeddings)[0]

    # Find the most similar sentences using torch.topk
    top_k_values, top_k_indices = torch.topk(similarities, k=2, largest=True)
    most_valuable_sentences = [lines[i] for i in top_k_indices.tolist()]

    return most_valuable_sentences


def generate_answer(query, sentence):
    # Use OpenAI API with the new interface
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """
            You are a transportation assistant chatbot.
            You will be asked about train schedules between cities.
            You must provide all available information about the schedules.
            """},
            {"role": "user", "content": sentence},
            {"role": "user", "content": query}
        ],
    )
    return response.choices[0].message['content'].strip()


def ask_question(question, file_path='data_text_v2.txt', embedding_file='embeddings.pkl'):
    language, q = correct_prompt(question)
    # print(q) # todo:
    # print(language) # todo:
    lines, line_embeddings = load_or_compute_embeddings(file_path, embedding_file)
    most_valuable_sentence = get_most_valuable_sentences(lines, line_embeddings, question)
    # print(f"most_valuable_sentence------>{most_valuable_sentence}")
    answer = generate_answer("You must answer the following question about transportation: '" + q + "provide your answer in :" + language + ".", "".join(most_valuable_sentence))
    return answer


questions = [
    "What are the train schedules from Settat to Casablanca?",
    "3etini ga3 les trains mn settat l tanger",
    "donnez moi tous les trains allant de rabat a kenitra"
]

for Q in questions:
    print(f"Q : {Q} \n A : {ask_question(Q)}", end="\n" + "_" * 100 + "\n")
