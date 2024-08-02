import os
import json
import re
import random

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class KeyPoint:

    def __init__(self, question):
        self.gemini_key = os.getenv("API_KEY")
        self.restructure_key = os.getenv("API_KEY2")
        self.question = question

    @staticmethod
    def random_slug():
        numbers_and_letters = [
            'a', '1', 'b', '2', 'c', '3', 'd', '4',
            'e', '5', 'f', '6', 'g', '7', 'h', '8',
            'i', '9', 'j', '10', 'k', '11', 'l',
            '12', 'm', '13', 'n', '14', 'o'
        ]
        generated_slug = []
        for i in range(10):
            random_num = random.randint(0, len(numbers_and_letters) - 1)
            generated_slug.append(str(numbers_and_letters[random_num]))
        return "".join(generated_slug)

    def retrieve_json(self, response):
        pattern = re.compile(r"\{([^{}]*)\}")
        finder = pattern.search(response.text)
        json_obj = finder.group()
        convert_json = json.loads(json_obj)
        return convert_json
    
    def configure_gemini(self, api_key):
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')

    def restructure_text(self):
        model = self.configure_gemini(api_key=self.restructure_key)
        response=model.generate_content(self.__generate_restructuring_prompt())
        converted_json = self.retrieve_json(response)
        return converted_json
    
    def __highlight_important_words_and_sents(self, response):
        self.converted_json = self.retrieve_json(response)
        important_sentences = self.converted_json['important_sentences']
        bold_data = self.modified_text
        if important_sentences:
            for sent in important_sentences:
                bold_data = bold_data.replace(sent, f"<strong>{sent}</strong>")
                
        important_words = self.converted_json['important_words']
        if important_words:
            for words in important_words:
                split_sent = words.split(" ")
                search_query = "+".join(split_sent)
                find_words = re.compile(r"\b" + re.escape(words) + r"\b", re.IGNORECASE)
                replacement = f'<strong><a href="https://www.google.com/search?q={search_query}" target="_blank">{words}</a></strong>'
                bold_data = find_words.sub(replacement, bold_data)     
        self.bold_data = bold_data

    def __package_highlight_data(self):
        title = self.converted_json['subject']
        final_text = self.bold_data.replace("/n/n", "<p>").replace("/n", "<br>")
        if not title:
            highlight_data = [final_text, None]
        else:
            highlight_data = [final_text, title]
        return highlight_data

    def emphasizer(self):
        text = self.restructure_text()
        self.modified_text = text['modified_text'].replace("**", "")
        model = self.configure_gemini(api_key=self.gemini_key)
        response=model.generate_content(self.__generate_highlighting_prompt())
        if not response.text == "No Enclosed Content":
            self.__highlight_important_words_and_sents(response)
            data = self.__package_highlight_data()
        else:
            data = [self.modified_text, None]

        return data

    def __generate_highlighting_prompt(self):
        prompt = f"""
        [{self.modified_text}] --- read thoroughly the block of text delimited by [], and use the ***Step-by-step Instructions*** to determine how to respond.

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
        return prompt
    
    def __generate_restructuring_prompt(self):
        prompt = f"""
        [{self.question}] --- read through the block of text which is delimited by [] and perform the following actions:
        1. Remove all newlines from the block of text
        2. Appropriately add paragraphs, bulletpoints and numbers when necessary
        3. Avoid using Markdown syntax, use "/n/n" to represent paragraphs 
        4. Go through the ***Guidelines*** for more instructions.

        ***Guidelines***
        1. Always respond with the modified text
        2. Return the modified text as a JSON object, with the key --- "modified_text".
        """
        return prompt