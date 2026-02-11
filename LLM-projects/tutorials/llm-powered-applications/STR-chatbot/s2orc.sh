#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --account=quinlan-rw
#SBATCH --partition=quinlan-rw
#SBATCH --mem=50g # sacct -o reqmem,maxrss,averss,elapsed -j JOBID
#SBATCH --output=s2orc.log

set -o errexit
set -o pipefail
set -o nounset
# set -o noclobber
# set -o xtrace

number_of_corpus_parts=264

for gene in "AFF2"; do 
  mkdir -p "docs/${gene}"
  # https://github.com/laurelhiatt/STRchive/tree/lit/data
  curl "https://raw.githubusercontent.com/laurelhiatt/STRchive/lit/data/${gene}01.txt" \
    | grep "PMID-" \
    | awk '{ print $2 }' \
  > "docs/${gene}/PMIDs.txt"  
  for corpus_part_id in $(seq 1 $number_of_corpus_parts); do 
    python s2orc.py ${gene} ${corpus_part_id}
  done
done 
