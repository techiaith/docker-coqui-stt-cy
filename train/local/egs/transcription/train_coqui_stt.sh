#!/bin/bash
set -e

### Force UTF-8 output
export PYTHONIOENCODING=utf-8

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

commonvoice_data_dir=/data/commonvoice9
alphabet_cy_file=/code/bin/bangor_welsh/alphabet.txt

set +x
echo
echo "####################################################################################"
echo "#### Downloading CommonVoice training data  (from link in data_url.py)          ####"
echo "####################################################################################"
set -x
python3 ${SCRIPT_DIR}/../shared/python/download_commonvoice.py --target_dir ${commonvoice_data_dir}


set +x
echo
echo "####################################################################################"
echo "#### Preparing training data                                                    ####"
echo "####################################################################################"
set -x
test_files=${commonvoice_data_dir}/clips/test.csv
#train_files=${commonvoice_data_dir}/clips/validated.csv,${commonvoice_data_dir}/clips/other.csv
#train_files=${commonvoice_data_dir}/clips/train.csv,${commonvoice_data_dir}/clips/dev.csv
train_files=${commonvoice_data_dir}/clips/validated.csv
single_train_csv=${commonvoice_data_dir}/clips/training_transcription.csv
python3 ${SCRIPT_DIR}/../shared/python/combine_csvs.py --in_csvs ${train_files} --out_csv ${single_train_csv}


set +x
echo
echo "####################################################################################"
echo "#### Re-initialise checkpoint directories for transfer learning                 ####"
echo "####################################################################################"
set -x

checkpoint_dir=/checkpoints

checkpoint_en_dir="${checkpoint_dir}/en"
checkpoint_cy_dir="${checkpoint_dir}/cy-transcription"

rm -rf ${checkpoint_en_dir}
rm -rf ${checkpoint_cy_dir}

mkdir -p ${checkpoint_en_dir}
mkdir -p ${checkpoint_cy_dir}

cp -rv /checkpoints/coqui/coqui-en-checkpoint/* $checkpoint_en_dir

export CUDA_VISIBLE_DEVICES=0

###
set +x
echo
echo "####################################################################################"
echo "#### Transfer to WELSH model with --save_checkpoint_dir --load_checkpoint_dir   ####"
echo "####################################################################################"
set -x
python3 -m coqui_stt_training.train \
	--train_files "${single_train_csv}" \
	--train_batch_size 64 \
	--drop_source_layers 2 \
	--epochs 15 \
	--use_allow_growth true \
	--alphabet_config_path "${alphabet_cy_file}" \
	--load_checkpoint_dir "${checkpoint_en_dir}" \
	--save_checkpoint_dir "${checkpoint_cy_dir}"


