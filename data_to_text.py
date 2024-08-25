import openai

# Set your OpenAI API key
openai.api_key = "xxxx"


def ask_question(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Based on the following information, answer the query:"},
            {"role": "user", "content": question}
        ],
    )
    return response.choices[0].message['content'].strip()

# read the file
with open("data_without_date.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()


# process the file to split traject
lines = lines[1:]
i, n = 1, len(lines)
start = 0
trajects = []
cities = lines[0].split("\t")[0:2]

while i < n:
    cities_now = lines[i].split("\t")[0:2]
    if cities_now != cities:
        cities = cities_now[:]
        if i - start > 1:
            trajects.append("".join(lines[start:i]))
        start = i
    i += 1

prompt = "I will provide train schedules for travel between two cities. Please consolidate this information into a single continuous paragraph, without lists or breaks."

# pip the traject to the chat to make it from row-data to human-text data
data_text = []
for i, traject in enumerate(trajects):
    traject_text_data = ask_question(prompt + "\n\n" + traject)
    data_text.append(traject_text_data)
    print(f"traject {i}/ {len(trajects)} --- {int((i/len(trajects))*100)}%\n")

with open('data_text_v2.txt', 'w', encoding='utf-8') as file:
    for item in data_text:
        file.write(item + "\n")






