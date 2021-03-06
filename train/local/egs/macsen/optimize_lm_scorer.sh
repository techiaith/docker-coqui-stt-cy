#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

checkpoint_dir=/checkpoints
checkpoint_cy_dir="${checkpoint_dir}/cy-macsen"

macsen_test_dir=/data/corpws-profi-adnabod-lleferydd/data/macsen
cp ${macsen_test_dir}/clips.csv ${macsen_test_dir}/clips/clips.csv
macsen_test_file=${macsen_test_dir}/clips/clips.csv

scorer_file_path=/export/coqui_${COQUI_RELEASE}_${TECHIAITH_RELEASE}/macsen/kenlm.macsen.scorer

set +x
echo "####################################################################################"
echo "####                                                                            ####"
echo "#### Preparing test set                                                         ####"
echo "####                                                                            ####"
echo "####################################################################################"
set -x
python3 ${SCRIPT_DIR}/../shared/python/preprocess_csv_dataset.py --csv ${macsen_test_file}


set +x
echo "####################################################################################"
echo "####                                                                            ####"
echo "#### Optimizing                                                                 ####"
echo "####                                                                            ####"
echo "####################################################################################"
set -x
python /code/lm_optimizer.py \
  --test_files ${macsen_test_file} \
  --checkpoint_dir ${checkpoint_cy_dir} \
  --n_trials 100 \
  --scorer ${scorer_file_path}
