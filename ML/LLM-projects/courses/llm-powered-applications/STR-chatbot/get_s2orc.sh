#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --account=quinlan-rw
#SBATCH --partition=quinlan-rw
#SBATCH --mem=50g # sacct -o reqmem,maxrss,averss,elapsed -j JOBID
#SBATCH --output=get_s2orc.log

set -o errexit
set -o pipefail
set -o nounset
# set -o noclobber
# set -o xtrace

python get_s2orc.py 

bash extract_s2orc_archive.sh
