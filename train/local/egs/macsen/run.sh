#!/bin/bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo ${SCRIPT_DIR}

${SCRIPT_DIR}/train_coqui_stt.sh 
${SCRIPT_DIR}/export_coqui_stt.sh 
${SCRIPT_DIR}/build_lm_scorer.sh 
${SCRIPT_DIR}/optimize_lm_scorer.sh
#${SCRIPT_DIR}/evaluate_coqui_stt.sh
