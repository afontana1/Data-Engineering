from googletrans import Translator


def g_translate(text, lang):

    translator = Translator()

    text_parts = text.split('. ')
    translated_text = []

    for parts in text_parts:
        translated_text.append(translator.translate(
            parts, src='en', dest=lang).text)

    return ' '.join(translated_text) + '.'
