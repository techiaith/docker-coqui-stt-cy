#!/bin/bash
set -e

### Force UTF-8 output
export PYTHONIOENCODING=utf-8

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

checkpoint_dir=/checkpoints
checkpoint_cy_dir="${checkpoint_dir}/cy-macsen"

macsen_test_dir=/data/corpws-profi-adnabod-lleferydd/data/macsen
cp ${macsen_test_dir}/clips.csv ${macsen_test_dir}/clips/clips.csv
macsen_test_file=${macsen_test_dir}/clips/clips.csv

scorer_file_path=/export/coqui_${COQUI_RELEASE}_${TECHIAITH_RELEASE}/macsen/kenlm.macsen.scorer

alphabet_cy_file=/code/bin/bangor_welsh/alphabet.txt


##
set +x
echo "####################################################################################"
echo "####                                                                            ####"
echo "#### Preparing test set                                                         ####"
echo "####                                                                            ####"
echo "####################################################################################"
set -x
python3 ${SCRIPT_DIR}/../shared/python/preprocess_csv_dataset.py --csv ${macsen_test_file}


##
set +x
echo
echo "####################################################################################"
echo "#### Test to see what WER and CER  (acoustic model)                             ####"
echo "####################################################################################"
set -x
python3 -m coqui_stt_training.evaluate \
	--test_files ${macsen_test_file} \
	--alphabet_config_path "${alphabet_cy_file}" \
	--checkpoint_dir ${checkpoint_cy_dir}


##
set +x
echo
echo "####################################################################################"
echo "#### Test to see what WER and CER  (with language model)                        ####"
echo "####################################################################################"
set -x
python3 -m coqui_stt_training.evaluate \
	--test_files ${macsen_test_file} \
	--alphabet_config_path ${alphabet_cy_file} \
	--checkpoint_dir ${checkpoint_cy_dir} \
	--scorer_path ${scorer_file_path}

