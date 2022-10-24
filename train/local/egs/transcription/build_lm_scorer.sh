#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

VOCAB_SIZE=50000

output_dir=/export/coqui_${COQUI_RELEASE}_${TECHIAITH_RELEASE}/transcription/kenlm   

alphabet_file_path=/code/bin/bangor_welsh/alphabet.txt

checkpoint_dir=/checkpoints
checkpoint_cy_dir="${checkpoint_dir}/cy-transcription"

test_dir=/data/commonvoice11
test_file=${test_dir}/clips/test.csv


# From optimize_lm_scorer.sh and common voice test.csv
#Best params: lm_alpha=0.9654557488724579 and lm_beta=1.5250547174262943 with WER=0.3415967918337587
default_alpha=0.9654557488724579
default_beta=1.5250547174262943

set +x
echo "####################################################################################"
echo "####                                                                            ####"
echo "#### Fetching OSCAR  text corpus                                                ####"
echo "####                                                                            ####"
echo "####################################################################################"
set -x
python3 ${SCRIPT_DIR}/python/download_oscar.py 


set +x
echo "####################################################################################"
echo "####                                                                            ####"
echo "#### Generating language model package                                          ####"
echo "####                                                                            ####"
echo "####################################################################################"
set -x
mkdir -p ${output_dir}
python3 /code/data/lm/generate_lm.py \
    --input_txt /lm-data/transcription/corpus.txt \
    --output_dir ${output_dir} \
    --top_k ${VOCAB_SIZE} \
    --kenlm_bins /code/kenlm/build/bin \
    --arpa_order 5 \
    --discount_fallback \
    --max_arpa_memory "40%" \
    --arpa_prune "0|0|1" \
    --binary_a_bits 255 \
    --binary_q_bits 8 \
    --binary_type trie


set +x
echo "####################################################################################"
echo "#### Generating language model package                                          ####"
echo "####                                                                            ####"
echo "#### Default alpha and beta values are                                          ####"
echo "####                                                                            ####"
echo "####  alpha : ${default_alpha}                                                  ####"
echo "####  beta  : ${default_beta}                                                   ####"
echo "####                                                                            ####"
echo "####################################################################################"
set -x
/code/generate_scorer_package \
	--checkpoint ${checkpoint_cy_dir} \
	--lm ${output_dir}/lm.binary \
	--vocab ${output_dir}/vocab-${VOCAB_SIZE}.txt \
	--package ${output_dir}/../kenlm.transcription.scorer \
 	--default_alpha ${default_alpha} \
	--default_beta ${default_beta}


