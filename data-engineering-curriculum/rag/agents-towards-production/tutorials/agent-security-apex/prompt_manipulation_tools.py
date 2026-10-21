def prompt_encoder(prompt, encoding=""):
    """
    Encode the prompt using the specified encoding.
    If no encoding is specified, a random encoding method will be chosen.
    """
    import random

    # List of all available encoding methods
    encoding_methods = [
        "atbash",
        "caesar",
        "vigenere",
        "braille",
        "morse",
        "pig_latin",
        "leet",
        "binary",
        "hex",
        "base64",
        "rot13",
        "reverse",
    ]

    # If no encoding specified, randomly choose one
    if encoding == "":
        encoding = random.choice(encoding_methods)
        print(f"Randomly selected encoding method: {encoding}")

    if encoding == "atbash":
        return atbash_encode(prompt)
    elif encoding == "caesar":
        return caesar_encode(prompt, 3)  # Example shift value
    elif encoding == "vigenere":
        return vigenere_encode(prompt, "KEY")  # Example key
    elif encoding == "braille":
        return braille_encode(prompt)
    elif encoding == "morse":
        return morse_encode(prompt)
    elif encoding == "pig_latin":
        return pig_latin_encode(prompt)
    elif encoding == "leet":
        return leet_encode(prompt)
    elif encoding == "binary":
        return binary_encode(prompt)
    elif encoding == "hex":
        return hex_encode(prompt)
    elif encoding == "base64":
        return base64_encode(prompt)
    elif encoding == "rot13":
        return rot13_encode(prompt)
    elif encoding == "reverse":
        return reverse_encode(prompt)
    else:
        raise ValueError("Unsupported encoding type.")


def atbash_encode(text):
    """
    Encode the text using the Atbash cipher.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    reversed_alphabet = alphabet[::-1]
    translation_table = str.maketrans(alphabet, reversed_alphabet)
    return text.translate(translation_table)


def caesar_encode(text, shift):
    """
    Encode the text using the Caesar cipher.
    """

    def shift_alphabet(alphabet, shift):
        return alphabet[shift:] + alphabet[:shift]

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    shifted_alphabet = shift_alphabet(alphabet, shift)
    translation_table = str.maketrans(alphabet, shifted_alphabet)
    return text.translate(translation_table)


def vigenere_encode(text, key):
    """
    Encode the text using the Vigenère cipher.
    """

    def generate_vigenere_table():
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        table = []
        for i in range(len(alphabet)):
            row = alphabet[i:] + alphabet[:i]
            table.append(row)
        return table

    def vigenere_encrypt(text, key):
        table = generate_vigenere_table()
        encrypted_text = []
        key_length = len(key)
        for i, char in enumerate(text):
            if char.isalpha():
                row = ord(key[i % key_length]) - ord("a")
                col = ord(char) - ord("a")
                encrypted_char = table[row][col]
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(char)
        return "".join(encrypted_text)

    return vigenere_encrypt(text.lower(), key.lower())


def braille_encode(text):
    """
    Encode the text using Braille.
    """
    braille_dict = {
        "a": "⠁",
        "b": "⠃",
        "c": "⠉",
        "d": "⠙",
        "e": "⠑",
        "f": "⠋",
        "g": "⠛",
        "h": "⠓",
        "i": "⠊",
        "j": "⠚",
        "k": "⠅",
        "l": "⠇",
        "m": "⠍",
        "n": "⠝",
        "o": "⠕",
        "p": "⠏",
        "q": "⠟",
        "r": "⠗",
        "s": "⠎",
        "t": "⠞",
        "u": "⠥",
        "v": "⠧",
        "w": "⠺",
        "x": "⠭",
        "y": "⠽",
        "z": "⠵",
    }
    return "".join(braille_dict.get(char, char) for char in text.lower())


def morse_encode(text):
    """
    Encode the text using Morse code.
    """
    morse_dict = {
        "a": ".-",
        "b": "-...",
        "c": "-.-.",
        "d": "-..",
        "e": ".",
        "f": "..-.",
        "g": "--.",
        "h": "....",
        "i": "..",
        "j": ".---",
        "k": "-.-",
        "l": ".-..",
        "m": "--",
        "n": "-.",
        "o": "---",
        "p": ".--.",
        "q": "--.-",
        "r": ".-.",
        "s": "...",
        "t": "-",
        "u": "..-",
        "v": "...-",
        "w": ".--",
        "x": "-..-",
        "y": "-.--",
        "z": "--..",
    }
    return "".join(morse_dict.get(char, char) for char in text.lower())


def pig_latin_encode(text):
    """
    Encode the text using Pig Latin.
    """

    def pig_latin_word(word):
        if word[0] in "aeiou":
            return word + "yay"
        else:
            return word[1:] + word[0] + "ay"

    words = text.split()
    pig_latin_words = [pig_latin_word(word) for word in words]
    return " ".join(pig_latin_words)


def leet_encode(text):
    """
    Encode the text using Leet Speak.
    """
    leet_dict = {
        "a": "4",
        "b": "8",
        "c": "<",
        "d": "|)",
        "e": "3",
        "f": "|=",
        "g": "9",
        "h": "#",
        "i": "1",
        "j": "_|",
        "k": "|<",
        "l": "|_",
        "m": "/\\/\\",
        "n": "^/",
        "o": "0",
        "p": "|*",
        "q": "(,)",
        "r": "|2",
        "s": "5",
        "t": "+",
        "u": "|_|",
        "v": "\\/",
        "w": "\\^/",
        "x": "%",
        "y": "`/",
        "z": "2",
    }
    return "".join(leet_dict.get(char, char) for char in text.lower())


def binary_encode(text):
    """
    Encode the text using binary.
    """
    return " ".join(format(ord(char), "08b") for char in text)


def hex_encode(text):
    """
    Encode the text using hexadecimal.
    """
    return " ".join(format(ord(char), "02x") for char in text)


def base64_encode(text):
    """
    Encode the text using Base64.
    """
    import base64

    return base64.b64encode(text.encode()).decode()


def rot13_encode(text):
    """
    Encode the text using ROT13.
    """
    import codecs

    return codecs.encode(text, "rot_13")


def reverse_encode(text):
    """
    Encode the text by reversing it.
    """
    return text[::-1]
