from jinja2 import Template, Environment, FileSystemLoader
from typing import NewType
import os
import re

# using https://github.com/Animenosekai/translate
from translatepy import Translator

TranscriptComponent = NewType("TranscriptComponent", str)
Transcript = NewType("Transcript", list[TranscriptComponent])
ENVIRONMENT = Environment(loader=FileSystemLoader("templates/"))
TEMPLATE = ENVIRONMENT.get_template("template.md")
PATH_TO_TRANSCRIPTS = "#transcripts\\philosophy_engineered\\"

PATTERN = re.compile(r"^[0-9]\d{0,2}:[0-9]\d{0,2}:[0-9]\d{0,2}.[0-9]\d{0,3}$")


def process_file(lines: Transcript, paragraph_size: int = 250, translator=None) -> None:
    MAX_PARAGRAPH_SIZE = 500
    processed_paragraphs = []
    paragraph = ""
    for idx, line in enumerate(lines):
        # cant get the fucking regex to work
        if "-->" in line:
            for idx2, subline in enumerate(lines[idx + 1 :]):
                if not subline.strip():
                    break
                text_to_add = subline.strip("\n")
                if translator:
                    text_to_add = translator.translate(text_to_add, "English").result
                paragraph += text_to_add + " "
        if len(paragraph) > paragraph_size:
            if (
                not paragraph.strip().endswith(".")
                and len(paragraph) < MAX_PARAGRAPH_SIZE
            ):
                continue
            processed_paragraphs.append(paragraph)
            paragraph = ""

    if paragraph and len(paragraph) <= paragraph_size:
        processed_paragraphs.append(paragraph)
    return processed_paragraphs


def main(subdir):
    input_files = os.listdir(PATH_TO_TRANSCRIPTS)
    for idx, file in enumerate(input_files):
        title = file.split(".")[0]
        path_to_file = f"{PATH_TO_TRANSCRIPTS}\{file}"
        if path_to_file.endswith(".json"):
            continue

        with open(path_to_file, "r", encoding="utf8") as f:
            transcript: Transcript = f.readlines()
            language = transcript[2].split(":")[-1].strip()
            if language not in ["en", "en-GB"]:
                print(f"Translating {file}")
                TRANSLATOR = Translator()
                results = process_file(
                    lines=transcript, paragraph_size=400, translator=TRANSLATOR
                )
            else:
                print(f"No need to translate {file}")
                results = process_file(lines=transcript, paragraph_size=400)
        title = title.replace("__", " ").replace("_", " ")
        content = TEMPLATE.render(title=title, paragraphs=results)

        with open(
            f"markdown_transcripts\{subdir}\{title}.md", mode="w", encoding="utf-8"
        ) as document:
            document.write(content)


if __name__ == "__main__":
    main(subdir="philosophy_engineered")
