set -o errexit
set -o pipefail
# set -o noclobber
set -o xtrace
set -o nounset 

# while read id; do
#   curl \
#     "https://www.ncbi.nlm.nih.gov/books/${id}/pdf/Bookshelf_${id}.pdf" \
#     --output "docs/${id}.pdf"
# done < GeneReviewsIDs.txt

# # https://github.com/laurelhiatt/STRchive/tree/lit/data
# for gene in "AFF2"; do 
#   mkdir -p "docs/${gene}"
#   curl "https://raw.githubusercontent.com/laurelhiatt/STRchive/lit/data/${gene}01.txt" \
#     | grep "PMID-" \
#     | awk '{ print $2 }' \
#   > "docs/${gene}/PMIDs.txt"
#   while read id; do
#     curl \
#       "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/${id}/unicode" \
#       --output "docs/${gene}/${id}.xml"
#   done < "docs/${gene}/PMIDs.txt"
# done 

for gene in "AFF2"; do 
  mkdir -p "docs/${gene}"
  # https://github.com/laurelhiatt/STRchive/tree/lit/data
  curl "https://raw.githubusercontent.com/laurelhiatt/STRchive/lit/data/${gene}01.txt" \
    | grep "PMID-" \
    | awk '{ print $2 }' \
  > "docs/${gene}/PMIDs.txt"
  python get_papers_from_SS2.py ${gene}
done 
