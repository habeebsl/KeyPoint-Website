import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
from nltk.tag import pos_tag

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



def wrap_consecutive_strong_tags(html):
    """
    Wrap consecutive <strong> tags with an <a> tag.

    Args:
        html (str): The HTML content.

    Returns:
        str: The HTML content with wrapped consecutive <strong> tags.
    """
    # Define a regex pattern to match consecutive <strong> tags
    pattern = r'(<strong>\s*.*?\s*<\/strong>\s*)+'

    # Define a function to replace matches with the wrapped version
    def replace_strong_tags(match):
        strong_tags_content = re.findall(r'<strong>\s*(.*?)\s*<\/strong>', match.group(0))
        search_query = '+'.join(strong_tags_content)
        return f'<a href="https://www.google.com/search?q={search_query}" target="_blank">{match.group(0)}</a>'

    # Use re.sub() to apply the replacement function to the HTML
    wrapped_html = re.sub(pattern, replace_strong_tags, html)

    return wrapped_html


def emphasize(block, threshold=4, sentences_per_paragraph=3):
    if not block:
        return ""

    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')

    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(block.lower())
    tagged_words = pos_tag(tokens)
    filtered_tokens = [word for word in tokens if re.match("^[a-zA-Z0-9-]+$", word)]

    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    word_count = Counter(lemmatized_tokens)

    for word, count in word_count.items():
        if count <= threshold and word not in stop_words:
            block = re.sub(r'\b' + re.escape(word) + r'(?=\W|$)', f"<strong>{word}</strong>", block, flags=re.IGNORECASE)

    wrapped_block = wrap_consecutive_strong_tags(block)
    block_with_paragraphs = add_paragraph_breaks(wrapped_block, sentences_per_paragraph)

    return block_with_paragraphs