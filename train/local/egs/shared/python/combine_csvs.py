#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas as pd

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

© Prifysgol Bangor University

"""


def main(csv_files, out_csv_file, **args):
    csv_file_list = csv_files.split(",")
    combined_csv=pd.concat([pd.read_csv(f) for f in csv_file_list ])
    combined_csv.to_csv(out_csv_file, index=False, encoding='utf-8')


if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--in_csvs", dest="csv_files", required=True, help="commma seperated list of csv files for concatenating")
    parser.add_argument("--out_csv", dest="out_csv_file", required=True, help="result single csv file")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
