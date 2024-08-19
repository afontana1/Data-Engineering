import pysbd
import os

documents = []
path_to_files = "Speech-to-Text-Converter\\transcripts\\"
for path, subdirs, files in os.walk(path_to_files):
    for name in files:
        filename = os.path.join(path, name)
        print(filename)
        with open(filename, "r") as f:
            documents.append(f.read())

seg = pysbd.Segmenter(language="en", clean=False)
print(seg.segment(documents[0]))
