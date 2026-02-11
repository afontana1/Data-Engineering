import os
import requests

DIR = '/scratch/ucgd/lustre-labs/quinlan/data-shared/s2orc' 

# https://api.semanticscholar.org/api-docs/datasets

def get_api_key():
  api_key = os.getenv("S2_API_KEY")
  if not api_key:
    raise EnvironmentError("S2_API_KEY environment variable not set.")
  return api_key

def get_latest_release_id(headers): 
  r = requests.get('https://api.semanticscholar.org/datasets/v1/release/latest', headers=headers)
  latest_release_id = r.json()['release_id']
  return latest_release_id

def get_download_links(headers, release_id, dataset_name):
  r = requests.get(f'https://api.semanticscholar.org/datasets/v1/release/{release_id}/dataset/{dataset_name}', headers=headers)
  download_links = r.json()['files']
  return download_links

def download_dataset(download_links, dataset_name, headers):
  for idx, download_link in enumerate(download_links, start=1):
    print(f'getting link {idx}/{len(download_links)}')
    r = requests.get(download_link, headers=headers)
    print(f'requests has returned ...')
    with open(f'{DIR}/{dataset_name}_part{idx}.zip', 'wb') as f:
      f.write(r.content)
    print(f"zip has been written to disk ...")
  print("Download completed!")

def download_s2orc():
  headers = {
      "x-api-key": get_api_key()
  }
  latest_release_id = get_latest_release_id(headers)
  dataset_name = "s2orc"
  download_links = get_download_links(headers, latest_release_id, dataset_name)
  download_dataset(download_links, dataset_name, headers)

if __name__ == "__main__":  
  download_s2orc()

  # Suggestions for working with downloaded dataset:
  # https://www.semanticscholar.org/product/api/tutorial#Suggestions-for-Working-with-Downloaded-Datasets