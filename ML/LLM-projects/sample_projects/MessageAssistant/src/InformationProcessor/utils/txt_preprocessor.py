from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


class NERExtractor:
    def __init__(self, model_name="dslim/bert-large-NER"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.nlp = pipeline("ner", model=self.model, tokenizer=self.tokenizer)
        self.entity_mapping = {
            "O": "Outside of a named entity",
            "B-MISC": "Miscellaneous entity",
            "I-MISC": "Miscellaneous entity",
            "B-PER": "Person name",
            "I-PER": "Person name",
            "B-ORG": "Organization",
            "I-ORG": "Organization",
            "B-LOC": "Location",
            "I-LOC": "Location",
        }

    def extract_entities(self, text) -> str:
        ner_results = self.nlp(text.replace('\n', ' '))
        filtered_entities = []
        for entity in ner_results:
            entity['entity'] = self.entity_mapping.get(entity['entity'], "Unknown entity")

            if entity['score'] < 0.80 or not entity['word'].isalpha():
                continue

            if entity['word'].startswith('##') and filtered_entities:
                if filtered_entities[-1]['score'] > 0.80:
                    filtered_entities[-1]['word'] += entity['word'].replace('##', '')
                    filtered_entities[-1]['end'] = entity['end']
                continue

            if (filtered_entities and filtered_entities[-1]['end'] == entity['start'] - 1
                    and filtered_entities[-1]['score'] > 0.80):
                filtered_entities[-1]['word'] += ' ' + entity['word']
                filtered_entities[-1]['end'] = entity['end']
            else:
                filtered_entities.append(entity)

        unique_entities = set()
        distilled_entities = ''

        for entity in filtered_entities:
            identifier = (entity['word'], entity['entity'])
            if identifier not in unique_entities:
                unique_entities.add(identifier)
                distilled_entities = f"{distilled_entities} {entity['word']}: {entity['entity']}\n"

        return distilled_entities
