import requests
import json
import os
import sys 
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

def get_corpus_part(corpus_part_id):
  corpus_directory = '/scratch/ucgd/lustre-labs/quinlan/data-shared/s2orc'

  with open(f'{corpus_directory}/s2orc_part{corpus_part_id}', 'r') as f:
    # TESTING: 
    # json_list = [json.loads(next(f)) for _ in range(100)] 
    json_list = [json.loads(line) for line in f]
  df = pd.DataFrame(json_list)

  print(f'...done getting df for corpus part {corpus_part_id}')
  return df

def get_api_key():
  return os.getenv("S2_API_KEY")

def get_pubmed_ids(gene): 
  with open(f'docs/{gene}/PMIDs.txt') as f:
    pubmed_ids = f.readlines()
    pubmed_ids = [f'PMID:{pubmed_id.strip()}' for pubmed_id in pubmed_ids]
  return pubmed_ids 
   
def save_text(gene, pubmed_id, corpus_id, df):
  with open(f'docs/{gene}/{pubmed_id}.txt', 'w') as f:
    text = df[df['corpusid'] == corpus_id].iloc[0]['content']['text']
    print(f'...done getting text for PMID:{pubmed_id} from df')
    f.write(text)
    print(f'...done writing {pubmed_id}.txt') 

def save_texts(gene, corpus_part_id): 
  print(f'gene: {gene}, corpus_part_id: {corpus_part_id}')
  
  df = get_corpus_part(corpus_part_id)

  # https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers
  r = requests.post(
    'https://api.semanticscholar.org/graph/v1/paper/batch',
    headers={
      "x-api-key": get_api_key()
    },
    params={
      "fields": "url,isOpenAccess,openAccessPdf,externalIds"
    },
    json={
      "ids": get_pubmed_ids(gene),
    }
  )

  if r.status_code == 200:
    for paper in r.json():
      pubmed_id = paper['externalIds']['PubMed'] 
      corpus_id = paper['externalIds']['CorpusId'] 
      if corpus_id in df['corpusid'].values:
        print(f'...PMID:{pubmed_id} is in corpus part')
        save_text(gene, pubmed_id, corpus_id, df)
      else: 
        print(f'...PMID:{pubmed_id} is not in corpus part')

  else:
    print(f"Error: {r.status_code}")
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
  save_texts(gene=sys.argv[1], corpus_part_id=sys.argv[2])