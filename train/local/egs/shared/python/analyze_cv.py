#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import pathlib
import librosa
import pandas
import wave

import numpy as np
import scipy.io.wavfile as wav

from python_speech_features import mfcc
from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

"""

N_CONTEXT=9

def panda_group(df, column, destination_file_path):

    df_grp_client = df.groupby(column).size().to_frame('count').reset_index()
    df_grp_client = df_grp_client.sort_values("count", ascending=False)
    df_grp_client.to_csv(destination_file_path, index=False)
    


def analyze_tsvs(cv_root_dir):
    #client_id	path	sentence	up_votes	down_votes	age	gender	accent	locale	segment
    tsv_files = pathlib.Path(cv_root_dir).glob("*.tsv")
    for tsv_file_path in tsv_files:
        
        print ("Analyzing %s " % tsv_file_path)

        if 'reported.tsv' in str(tsv_file_path):
            continue
        
        df = pandas.read_csv(tsv_file_path, encoding='utf-8', sep='\t', header=0, dtype={'gender':str})

        panda_group(df, 'client_id', str(tsv_file_path).replace(".tsv",".counts.client_id.txt"))
        panda_group(df, 'sentence', str(tsv_file_path).replace(".tsv",".counts.sentence.txt"))
        
        panda_group(df, 'age', str(tsv_file_path).replace(".tsv",".counts.age.txt"))
        panda_group(df, 'gender', str(tsv_file_path).replace(".tsv",".counts.gender.txt"))

        # analyze clients by age and gender.... 


def analyze_csvs(cv_root_dir):

    clips_dir = os.path.join(cv_root_dir, "clips")
    csv_files = pathlib.Path(clips_dir).glob("*.csv")

    # client_id	path	sentence	up_votes	down_votes	age	gender	accent	locale	segment
    for csv_file_path in csv_files:
        
        df = pandas.read_csv(csv_file_path, encoding='utf-8')        
        #
        df_grouped = df.groupby("transcript").size().to_frame('count').reset_index()
        df_grouped = df_grouped.sort_values("count", ascending=False)

        df_grouped.to_csv(str(csv_file_path).replace(".csv",".dups.txt"), index=False)

        #        
        total_duration = 0.0
        count = 0
        for index, row in df.iterrows():
            count += 1
            wav_file_path = os.path.join(cv_root_dir, "clips", row["wav_filename"])
            total_duration = total_duration + librosa.get_duration(filename=wav_file_path)

        print ("%s\t%s recordings\t\t%.2f hours\t(%.2f seconds)" % (csv_file_path, count, total_duration/60.0/60.0, total_duration))
        print (df_grouped.nlargest(n=5, columns='count'))
        print ('\n')


def audiofile_to_input_vector(audio_filename, numcep, numcontext):
    """
    Given a WAV audio file at ``audio_filename``, calculates ``numcep`` MFCC features
    at every 0.01s time step with a window length of 0.025s. Appends ``numcontext``
    context frames to the left and right of each time step, and returns this data
    in a numpy array.
    """
    # Load wav files
    fs, audio = wav.read(audio_filename)

    # Get mfcc coefficients
    features = mfcc(audio, samplerate=fs, numcep=numcep, winlen=0.032, winstep=0.02, winfunc=np.hamming)

    # Add empty initial and final contexts
    empty_context = np.zeros((numcontext, numcep), dtype=features.dtype)
    features = np.concatenate((empty_context, features, empty_context))

    return features

def is_feasible_transcription(wavfile, transcription):
    aftiv_length=audiofile_to_input_vector(wavfile, 26, N_CONTEXT).shape[0] - 2*N_CONTEXT
    return aftiv_length > len(transcription)


def verify_csvs(cv_root_dir):

    clips_dir = os.path.join(cv_root_dir, "clips")
    csv_files = pathlib.Path(clips_dir).glob("*.csv")

    for csv_file_path in csv_files:
        print ("Verifying CSV: {}".format(csv_file_path))
        df = pandas.read_csv(csv_file_path, encoding='utf-8')
        
        for index, row in df.iterrows():
            wav_file_path = os.path.join(cv_root_dir, "clips", row["wav_filename"])
            transcription = row["transcript"]
            if is_feasible_transcription(wav_file_path, transcription) == False:
                print (wav_file_path, '\t', transcription)

def main(cv_root_dir, **args):

    #verify_csvs(cv_root_dir) 
    #analyze_tsvs(cv_root_dir)
    analyze_csvs(cv_root_dir)

    

   
if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--cv_dir", dest="cv_root_dir", required=True, help="path to commonvoice files")    
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

