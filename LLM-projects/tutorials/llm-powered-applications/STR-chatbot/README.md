## Semantic Scholar communication 

### Request 

In collaboration with Harriet Dashnow (https://harrietdashnow.com/), we are pursuing a method to automate the at-scale and real-time discovery of the loci, alleles, etc. associated with all known rare diseases, but in particular, those diseases associated with STR expansions. The idea is to use LLMs to ask questions of the literature, e.g., what are the loci associated with a given disease, what are the alleles associated with disease, etc. 

We currently have an LLM running locally on the University of Utah high-performance computing cluster, circumventing copyright issues that arise when using proprietary LLMs, e.g., those offered by OpenAI. And we are able to query a small set of research articles using the LLM. 

We now wish to download ~1000 specific research articles so that we can run the LLM on these articles. We can't do this using pubmed because most of the required articles are not open-access, and pubmed prohibits the bulk download of non-open-access articles. We hope that Semantic Scholar will allow us to download all these articles, or at least a significant majority of them. In fact, it would be great if I could send along the pubmed ids of the required articles, and Semantic Scholar could tell me how many of those it has the full text for. 

We will validate the method by comparing its predictions with the structured data Harriet has already manually curated from a small number of pdfs: 
https://github.com/hdashnow/STRchive/blob/main/data/STR-disease-loci.processed.json  

The methods Harriet and I will develop ought to have broad applicability to other projects in the Quinlan lab (http://quinlanlab.org/), e.g., the data-mining component of a graduate student's thesis where he proposes to pull down gene regulatory networks to inform variant interpretation, among other things. 

### Response

Thank you for requesting a Semantic Scholar API key! Your request has been approved. Here are the details:

S2 API Key: red-acted
Rate limit:
1 request per second for the following endpoints:
/paper/batch
/paper/search
/recommendations
10 requests / second for all other calls
Please set your rate limit to below this threshold to avoid rejected requests.

The API key needs to be sent in the header of the request as x-api-key directed at https://api.semanticscholar.org/ or via curl -Hx-api-key:$S2_API_KEY if coding in python.

 
