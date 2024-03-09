import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re
import random

load_dotenv()

def remove_redundant_new_lines(text):
    new = text.split(" ")
    for i in new:
        if "." in i and "\n" in i:
            if not i.index("\n") == i.index(".") + 1:
                new_line_index = i.index("\n")
                # containing_new_line = new.index(i)
                replaced = i[:new_line_index] + " " + i[new_line_index + 1:]
                new = " ".join(new)
                new = new.replace(i, replaced)
                new = new.split(" ")
        if "." not in i:
            if "\n" in i:
                new_line_index = i.index("\n")
                replaced = i[:new_line_index] + " " + i[new_line_index + 1:]
                new = " ".join(new)
                new = new.replace(i, replaced)
                new = new.split(" ")

    return " ".join(new)

def emphasize(question):

    new_text = remove_redundant_new_lines(question)
    
    GOOGLE_API_KEY=os.getenv("API_KEY")

    genai.configure(api_key=GOOGLE_API_KEY)

    prompt = f"""
        [{new_text}] --- read thoroughly the block of text delimited by [], and use the ***Step-by-step Instructions*** to determine how to respond. 

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
        5. If the json object doesn't contain any enclosed content, respond with: ***No Enclosed Content***
    """

    model = genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt)
    print(response.text)

    if not response.text == '***No Enclosed Content***':
        pattern = re.compile(r"\{([^{}]*)\}")
        finder = pattern.search(response.text)

        json_obj = finder.group()

        convert_json = json.loads(json_obj)



        important_sentences = convert_json['important_sentences']

        new_convert_json = new_text

        if important_sentences:

            for sent in important_sentences:
                if new_convert_json == new_text:
                    new_convert_json = new_convert_json.replace(sent, f"<strong>{sent}</strong>")
                else:
                    new_convert_json = new_convert_json.replace(sent, f"<strong>{sent}</strong>")


        important_words = convert_json['important_words']

        if important_words:
            for words in important_words:
                split_sent=words.split(" ")
                search_query="+".join(split_sent)
                find_words = re.compile(r"\b" + re.escape(words) + r"\b", re.IGNORECASE)
                replacement = f'<strong><a href="https://www.google.com/search?q={search_query}" target="_blank">{words}</a></strong>'
                new_convert_json = find_words.sub(replacement, new_convert_json)
        

        # block_with_paragraphs = add_paragraph_breaks(new_convert_json, sentences_per_paragraph)
        
        title = convert_json['subject']
        if not title:
            final_text = new_convert_json.replace("\n", "<br>")
            data = [final_text, None]
        else:
            final_text = new_convert_json.replace("\n", "<br>")
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
    return "".join(generated_slug)
