#!/bin/bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

commonvoice_data_dir=/data/commonvoice

python3 ${SCRIPT_DIR}/../shared/python/download_commonvoice.py --target_dir ${commonvoice_data_dir}

alphabet_cy_file=/code/bin/bangor_welsh/alphabet.txt
export_dir=/export/coqui_${COQUI_RELEASE}_${TECHIAITH_RELEASE}/macsen/


set +x
echo
echo "####################################################################################"
echo "#### Preparing training data                                                    ####"
echo "####################################################################################"
set -x
train_files=${commonvoice_data_dir}/clips/validated.csv,${commonvoice_data_dir}/clips/other.csv
single_train_csv=${commonvoice_data_dir}/clips/training_macsen.csv
python3 ${SCRIPT_DIR}/../shared/python/combine_csvs.py --in_csvs ${train_files} --out_csv ${single_train_csv}


set +x
echo
echo "####################################################################################"
echo "#### Re-initialise checkpoint directories for transfer learning                 ####"
echo "####################################################################################"
set -x

checkpoint_dir=/checkpoints

checkpoint_cy_dir="${checkpoint_dir}/cy-macsen"
checkpoint_en_dir="${checkpoint_dir}/en"

rm -rf ${checkpoint_en_dir}
rm -rf ${checkpoint_cy_dir}

mkdir -p ${checkpoint_en_dir}
mkdir -p ${checkpoint_cy_dir}

cp -r /checkpoints/coqui/coqui-en-checkpoint/ $checkpoint_en_dir

set +x
echo
echo "####################################################################################"
echo "#### Reset exports folder                                                       ####"
echo "####################################################################################"
set -x
rm -rf ${export_dir}
mkdir -p ${export_dir}

###
set +x
echo
echo "####################################################################################"
echo "#### Transfer to WELSH model with --save_checkpoint_dir --load_checkpoint_dir   ####"
echo "####################################################################################"
set -x
python3 -m coqui_stt_training.train \
	--train_files "${single_train_csv}" \
	--train_batch_size 48 \
	--drop_source_layers 2 \
	--epochs 15 \
	--alphabet_config_path "${alphabet_cy_file}" \
	--load_checkpoint_dir "${checkpoint_en_dir}" \
	--save_checkpoint_dir "${checkpoint_cy_dir}"


set +x
echo
echo "####################################################################################"
echo "#### Export new Welsh checkpoint to frozen model                                ####"
echo "####################################################################################"
set -x
python3 -m coqui_stt_training.export \
	--checkpoint_dir "${checkpoint_cy_dir}" \
	--alphabet_config_path "${alphabet_cy_file}" \
	--export_dir "${export_dir}"


set +x
echo
echo "####################################################################################"
echo "#### Exported acoustic models can be found in ${export_dir} "
echo "####################################################################################"
set -x
