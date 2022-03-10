#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

VOCAB_SIZE=1000

output_dir=/export/coqui_${COQUI_RELEASE}_${TECHIAITH_RELEASE}/macsen/kenlm   

alphabet_file_path=/code/bin/bangor_welsh/alphabet.txt

# From optimize_lm_scorer.sh and /data/corpws-profi-adnabod-lleferydd/data/macsen/clips/clips.csv
# Best params: lm_alpha=1.3569014286213879 and lm_beta=4.382943647381376 with WER=0.07770632368703108
default_alpha=1.3569014286213879
default_beta=4.382943647381376

set +x
echo "####################################################################################"
echo "####                                                                            ####"
echo "#### Fetching Macsen text corpus                                                ####"
echo "####                                                                            ####"
echo "####################################################################################"
set -x
python3 ${SCRIPT_DIR}/python/download_macsen_corpus.py 


set +x
echo "####################################################################################"
echo "####                                                                            ####"
echo "#### Generating language model package                                          ####"
echo "####                                                                            ####"
echo "####################################################################################"
set -x
mkdir -p ${output_dir}
python3 /code/data/lm/generate_lm.py \
    --input_txt /lm-data/macsen/corpus.txt \
    --output_dir ${output_dir} \
    --top_k ${VOCAB_SIZE} \
    --kenlm_bins /code/kenlm/build/bin \
    --arpa_order 5 \
    --discount_fallback \
    --max_arpa_memory "85%" \
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
	--alphabet ${alphabet_file_path} \
	--lm ${output_dir}/lm.binary \
	--vocab ${output_dir}/vocab-${VOCAB_SIZE}.txt \
	--package ${output_dir}/../kenlm.macsen.scorer \
 	--default_alpha ${default_alpha} \
	--default_beta ${default_beta}
