#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

checkpoint_dir=/checkpoints
checkpoint_cy_dir="${checkpoint_dir}/cy-transcription"

test_dir=/data/commonvoice11
test_file=${test_dir}/clips/test.csv

scorer_file_path=/export/coqui_${COQUI_RELEASE}_${TECHIAITH_RELEASE}/transcription/kenlm.transcription.scorer


set +x
echo "####################################################################################"
echo "####                                                                            ####"
echo "#### Optimizing                                                                 ####"
echo "####                                                                            ####"
echo "####################################################################################"
set -x
python /code/lm_optimizer.py \
  --test_files ${test_file} \
  --test_batch_size 64 \
  --checkpoint_dir ${checkpoint_cy_dir} \
  --n_trials 100 \
  --scorer ${scorer_file_path}
