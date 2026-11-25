
import string

punctuation = string.punctuation

class Tokenizer:
    def __init__(self):
        pass

    @staticmethod
    def tokenize(text: str) -> list[str]:
        #Lowercase
        text = text.lower()
        #Remove punctuation
        text = text.translate(
           str.maketrans({character: " " for character in string.punctuation})
        )
        #split by whitespace
        return text.split()