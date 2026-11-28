import string

punctuation = string.punctuation


class Tokenizer:
    def __init__(self) -> None:
        pass

    @staticmethod
    def tokenize(text: str) -> list[str]:
        # Lowercase
        text = text.lower()
        # Remove punctuation
        translation_table: dict[str, str | int | None] = {character: " " for character in string.punctuation}
        text = text.translate(str.maketrans(translation_table))
        # split by whitespace
        return text.split()
