set -o errexit
set -o pipefail
set -o nounset
# set -o noclobber
# set -o xtrace

number_of_parts=264
dir="/scratch/ucgd/lustre-labs/quinlan/data-shared/s2orc"

for i in $(seq 1 $number_of_parts); do 
  # Note that there is no space between the -o option and the directory path:
  7z x "${dir}/s2orc_part${i}.zip" -o${dir}
  rm "${dir}/s2orc_part${i}.zip"
done

