import requests
import json
import os
import sys 

def get_api_key():
  api_key = os.getenv("S2_API_KEY")
  if not api_key:
    raise EnvironmentError("S2_API_KEY environment variable not set.")
  return api_key

def get_pubmed_ids(gene): 
  with open(f'docs/{gene}/PMIDs.txt') as f:
    pubmed_ids = f.readlines()
    pubmed_ids = [f'PMID:{pubmed_id.strip()}' for pubmed_id in pubmed_ids]
  return pubmed_ids
   
def download_pdf(url, destination, log):
  r = requests.get(url)
  if r.status_code == 200:
    with open(destination, 'wb') as f:
      f.write(r.content)
      if log: print(f"Downloaded {destination}")
  else:
    if log: print(f"Error: {r.status_code}\turl: {url}")

def get_papers(gene): 
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
      paper_id = paper['paperId']
      pubmed_id = paper['externalIds']['PubMed'] 
      corpus_id = paper['externalIds']['CorpusId'] 
      open_access_pdf_available = True if paper['openAccessPdf'] else False
      print(f"Corpus ID: {corpus_id}\tSS2 ID: {paper_id}\tPubMed ID: {pubmed_id}\tOpen Access PDF: {open_access_pdf_available}")
      if open_access_pdf_available:
        url = paper['openAccessPdf']['url']
        download_pdf(url, f'docs/AFF2/{pubmed_id}.pdf', log=False)
  else:
    print(f"Error: {r.status_code}")
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":  
  get_papers(gene=sys.argv[1])