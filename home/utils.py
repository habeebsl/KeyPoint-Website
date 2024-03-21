import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re
import random

load_dotenv()


def retrieve_json(response):
    pattern = re.compile(r"\{([^{}]*)\}")
    finder = pattern.search(response.text)

    json_obj = finder.group()

    convert_json = json.loads(json_obj)
    return convert_json

def restructure_text(text):
    KEY=os.getenv("API_KEY2")

    genai.configure(api_key=KEY)

    prompt = f"""
    [{text}] --- read through the block of text which is delimited by [] and perform the following actions:
    1. Remove all newlines from the block of text
    2. Appropriately add paragraphs, bulletpoints and numbers when necessary
    3. Avoid using Markdown syntax, use "/n/n" to represent paragraphs 
    4. Go through the ***Guidelines*** for more instructions.

    ***Guidelines***
    1. Always respond with the modified text
    2. Return the modified text as a JSON object, with the key --- "modified_text".
    """


    model = genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt)
    converted_json = retrieve_json(response)
    return converted_json

def emphasize(question):

    text = restructure_text(question)
    print(text)
    new_t = text['modified_text']
    new_text = new_t.replace("**", "")
    
    GOOGLE_API_KEY=os.getenv("API_KEY")

    genai.configure(api_key=GOOGLE_API_KEY)

    prompt = f"""
    [{new_text}] --- read thoroughly the block of text delimited by [], and use the ***Step-by-step Instructions*** to determine how to respond.

    ***Step by step Instructions***
    1. Identify the subject of the block of text.
    2. Utilize this identified subject to pinpoint especially important words or sentences within the text.
    3. Place the important sentences found in a Python list.
    4. Place important words in a separate Python list.
    5. Construct a JSON object with the important sentences Python list and the important words Python list as the value to the dictionary.
    6. Proceed to the ***Guidelines*** before responding.

    ***Guidelines***
    1. Respond only with a JSON object, containing the stored important words and sentences.
    2. Name the key containing the important sentences --- "important_sentences".
    3. Name the key containing the important words --- "important_words".
    4. Create another key containing the identified subject and name it --- "subject".
    5. If the JSON object doesn't contain any enclosed content, respond with: "No Enclosed Content".
    6. Ensure that the important sentences include context and are not fragmented.
    7. Exclude common or trivial words from the important words list.
    8. Use the subject to filter out irrelevant content and focus on the main topic.
    9. Provide at least one important sentence and one important word in the JSON object.
    10. Ensure that the JSON object is well-formed with proper syntax (e.g., double quotes for keys and string values).
    11. Avoid including personal or sensitive information in the response.
    12. Double-check the response for accuracy and relevance before submitting.
    13. If unsure about the relevance of a sentence or word, err on the side of inclusivity rather than exclusivity.
    14. If the text contains multiple subjects, prioritize the most significant subject for the response.
    15. Consider the overall context of the text to provide a comprehensive and meaningful response.
    """


    model = genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt)
    print(response.text)

    if not response.text == "No Enclosed Content":
        converted_json = retrieve_json(response)


        important_sentences = converted_json['important_sentences']

        new_convert_json = new_text

        if important_sentences:

            for sent in important_sentences:
                if new_convert_json == new_text:
                    new_convert_json = new_convert_json.replace(sent, f"<strong>{sent}</strong>")
                else:
                    new_convert_json = new_convert_json.replace(sent, f"<strong>{sent}</strong>")


        important_words = converted_json['important_words']

        if important_words:
            for words in important_words:
                split_sent=words.split(" ")
                search_query="+".join(split_sent)
                find_words = re.compile(r"\b" + re.escape(words) + r"\b", re.IGNORECASE)
                replacement = f'<strong><a href="https://www.google.com/search?q={search_query}" target="_blank">{words}</a></strong>'
                new_convert_json = find_words.sub(replacement, new_convert_json)
        

        # block_with_paragraphs = add_paragraph_breaks(new_convert_json, sentences_per_paragraph)
        
        title = converted_json['subject']
        if not title:
            final_text = new_convert_json.replace("/n/n", "<p>")
            final_text = new_convert_json.replace("/n", "<br>")
            data = [final_text, None]
        else:
            final_text = new_convert_json.replace("/n/n", "<p>")
            final_text = new_convert_json.replace("/n", "<br>")
            data = [final_text, title]

        print(new_convert_json)
    else:
        data = [new_text, None]


    return data

def random_slug():
    numbers_and_letters = ['a', '1', 'b', '2', 'c', '3', 'd', '4', 'e', '5', 'f', '6', 'g', '7', 'h', '8', 'i', '9', 'j', '10', 'k', '11', 'l', '12', 'm', '13', 'n', '14', 'o']

    generated_slug = []

    for i in range(10):
        random_num = random.randint(0, len(numbers_and_letters) - 1)
        generated_slug.append(str(numbers_and_letters[random_num]))
    return "-"+"".join(generated_slug)
