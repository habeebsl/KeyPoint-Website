import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()


def add_paragraph_breaks(text, sentences_per_paragraph=3):
    if not text:
        return ""

    sentences = text.split('. ')
    paragraphs = []
    current_paragraph = ''

    for i, sentence in enumerate(sentences):
        current_paragraph += sentence + ('. ' if i < len(sentences) - 1 else '')  # Add period if not the last sentence
        if (i + 1) % sentences_per_paragraph == 0 or i == len(sentences) - 1:
            paragraphs.append(f"<p>{current_paragraph.strip()}</p>")
            current_paragraph = ''

    result = ''.join(paragraphs)

    return result


def emphasize(question, sentences_per_paragraph=3):
    GOOGLE_API_KEY=os.getenv("API_KEY")

    genai.configure(api_key=GOOGLE_API_KEY)

    prompt = f"""
        [{question}] --- read thoroughly the block of text delimited by [], and use the ***Step-by-step Instructions*** to determine how to respond. 

        ***Step by step Instructions***
        1. Identify the subject of the block of text.
        2. Utilize this identified subject to pinpoint especially important words or sentences within the text.
        3. Place the important sentences found in a python list
        4. Place important words in a seperate python list 
        5. Construct a json object with the important sentences python list and the important words python list as the value to the dictionary
        6. Proceed to the ***Guidelines*** before responding.

        ***Guidelines***
        1. Respond only with the json object, containing the stored important words and sentences.
        2. Name the key containing the important sentences --- important_sentences
        3. Name the key containing the important words --- important_words
        4. Create another key containing the identified subject and name it --- subject
        5. If the Python dictionary value doesn't contain any enclosed content, respond with: ***No Enclosed Content***
    """

    model = genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt)
    # print(response.text)

    pattern = re.compile(r"\{([^{}]*)\}")
    finder = pattern.search(response.text)

    json_obj = finder.group()

    convert_json = json.loads(json_obj)

    important_sentences = convert_json['important_sentences']

    new_convert_json = question

    for sent in important_sentences:
        if new_convert_json == question:
            new_convert_json = new_convert_json.replace(sent, f"<strong>{sent}</strong>")
        else:
            new_convert_json = new_convert_json.replace(sent, f"<strong>{sent}</strong>")


    important_words = convert_json['important_words']

    for words in important_words:
        split_sent=words.split(" ")
        search_query="+".join(split_sent)
        find_words = re.compile(r"\b" + re.escape(words) + r"\b")
        replacement = f'<strong><a href="https://www.google.com/search?q={search_query}" target="_blank">{words}</a></strong>'
        new_convert_json = find_words.sub(replacement, new_convert_json)
    

    # block_with_paragraphs = add_paragraph_breaks(new_convert_json, sentences_per_paragraph)

    title = convert_json['subject']
    final_text = new_convert_json.replace("\n", "<br>")
    data = [final_text, title]



    return data
