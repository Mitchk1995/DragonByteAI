import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def tokenize(text):
    return word_tokenize(text)

def pos_tagging(tokens):
    return pos_tag(tokens)

def named_entity_recognition(tagged_tokens):
    return ne_chunk(tagged_tokens)

def process_text(text):
    tokens = tokenize(text)
    tagged = pos_tagging(tokens)
    entities = named_entity_recognition(tagged)
    return entities
