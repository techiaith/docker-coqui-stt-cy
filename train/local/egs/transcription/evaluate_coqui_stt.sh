#!/bin/bash
set -e

### Force UTF-8 output
export PYTHONIOENCODING=utf-8

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

commonvoice_data_dir=/data/commonvoice9
alphabet_cy_file=/code/bin/bangor_welsh/alphabet.txt
export_dir=/export/coqui_${COQUI_RELEASE}_${TECHIAITH_RELEASE}/transcription

set +x
echo
echo "####################################################################################"
echo "#### Preparing training data                                                    ####"
echo "####################################################################################"
set -x
test_files=${commonvoice_data_dir}/clips/test.csv


set +x
echo
echo "####################################################################################"
echo "#### Re-initialise checkpoint directories for transfer learning                 ####"
echo "####################################################################################"
set -x

checkpoint_dir=/checkpoints

checkpoint_en_dir="${checkpoint_dir}/en"
checkpoint_cy_dir="${checkpoint_dir}/cy-transcription"


###
set +x
echo
echo "####################################################################################"
echo "#### Test to see what WER and CER  (acoustic model)                             ####"
echo "####################################################################################"
set -x
python3 -m coqui_stt_training.evaluate \
	--test_files ${test_files} \
	--alphabet_config_path "${alphabet_cy_file}" \
	--checkpoint_dir ${checkpoint_cy_dir}


##
if [ -f ${export_dir}/kenlm.transcription.scorer ]
then
	set +x
	echo
	echo "####################################################################################"
	echo "#### Test to see what WER and CER  (with language model)                        ####"
	echo "####################################################################################"
	set -x
	python3 -m coqui_stt_training.evaluate \
		--test_files ${test_files} \
		--alphabet_config_path ${alphabet_cy_file} \
		--checkpoint_dir ${checkpoint_cy_dir} \
		--scorer_path ${export_dir}/kenlm.transcription.scorer
fi

