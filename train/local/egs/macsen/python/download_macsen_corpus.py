import os
import json
import requests

import text_preprocess

from pathlib import Path

from data_url import _MACSEN_TEXT_CORPUS_URL



def get_macsen_textcorpus(lm_data_root_dir):

    target_dir = os.path.join(lm_data_root_dir, 'macsen')
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    
    json_data = json.loads(requests.get(_MACSEN_TEXT_CORPUS_URL).text)
    with open(os.path.join(target_dir, "corpus.txt"), 'w', encoding='utf-8') as macsen_file_out: 
        for s in json_data["result"]:
            macsen_file_out.write(text_preprocess.cleanup(s[0]).strip() + "\n")

get_macsen_textcorpus("/lm-data")
