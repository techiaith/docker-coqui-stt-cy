import os
import json
import requests

import text_preprocess

from datasets import load_dataset
from pathlib import Path

def get_textcorpus(lm_data_root_dir):

    target_dir = os.path.join(lm_data_root_dir, 'transcription')
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    corpus_file_path=os.path.join(target_dir, "corpus.txt")

    #
    oscar_dataset_name="unshuffled_deduplicated_cy"

    print ("\nLoading OSCAR {} dataset...".format(oscar_dataset_name))
    oscar_corpus = load_dataset("oscar", oscar_dataset_name)

    print ("\nExporting OSCAR to text file {}...".format(corpus_file_path))
    with open(corpus_file_path, 'w', encoding='utf-8') as corpus_file:
        for line in oscar_corpus["train"]:
            t = text_preprocess.cleanup(line["text"])
            corpus_file.write(t)

get_textcorpus("/lm-data")
