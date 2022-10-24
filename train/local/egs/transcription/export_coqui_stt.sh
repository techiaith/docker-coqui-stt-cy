#!/bin/bash
set -e

### Force UTF-8 output
export PYTHONIOENCODING=utf-8

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

alphabet_cy_file=/code/bin/bangor_welsh/alphabet.txt
export_dir=/export/coqui_${COQUI_RELEASE}_${TECHIAITH_RELEASE}/transcription/


set +x
echo
echo "####################################################################################"
echo "#### Re-initialise checkpoint directories for transfer learning                 ####"
echo "####################################################################################"
set -x

checkpoint_dir=/checkpoints

checkpoint_en_dir="${checkpoint_dir}/en"
checkpoint_cy_dir="${checkpoint_dir}/cy-transcription"

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
echo "#### Export new Welsh checkpoint to frozen model                                ####"
echo "####################################################################################"
set -x
/tflite-venv/bin/python -m coqui_stt_training.export \
	--checkpoint_dir "${checkpoint_cy_dir}" \
	--alphabet_config_path "${alphabet_cy_file}" \
	--export_dir "${export_dir}"


set +x
echo
echo "####################################################################################"
echo "#### Exported acoustic models can be found in ${export_dir} "
echo "####################################################################################"
set -x
