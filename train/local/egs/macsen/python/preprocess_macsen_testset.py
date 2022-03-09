#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas as pd

import text_preprocess

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

© Prifysgol Bangor University

"""

def main(csv_file, **args):

    df = pd.read_csv(csv_file)
    df.reset_index()

    for index, row in df.iterrows():
        transcript=text_preprocess.cleanup(row['transcript'])
        df.at[index,'transcript']=transcript
    
    df.to_csv(csv_file, index=False, encoding='utf-8')

            


if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--csv", dest="csv_file", required=True, help="path to csv file")
       
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

