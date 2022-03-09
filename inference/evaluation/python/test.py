import os
import csv
import librosa
import yaml
import datetime
import pandas
import wave
import glob

import text_preprocess

import re
import numpy as np

from stt import Model

from pathlib import Path
from datasets import load_metric

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

 Prifysgol Bangor University

"""


wer = load_metric("wer")
cer = load_metric("cer")

predictions = list()
references = list()

tags_regex = '\[.*?\]'

class TestStatistics:

    def __init__(self, name):
        self.name = name

        self.total_clips=0
        self.total_ignored_clips=0

        self.total_duration=0        
        
        self.average_wer=0
        self.average_cer=0

        self.dfResults=pandas.DataFrame(columns=['wav_filename', 'duration', 'prediction', 'reference', 'wer', 'cer'])
        self.dfIgnoredResults=pandas.DataFrame(columns=['wav_filename', 'duration', 'prediction', 'reference', 'wer', 'cer'])


    def calculate_error_rates(self, prediction, reference):        
        tmp_predictions=list()
        tmp_predictions.append(prediction)

        tmp_references=list()           
        tmp_references.append(reference)

        return 100*wer.compute(predictions=tmp_predictions, references=tmp_references), 100*cer.compute(predictions=tmp_predictions, references=tmp_references)
    

    def add(self, clip_file_path, prediction, reference):        
        audio, rate = librosa.load(clip_file_path, sr=16000)
        duration=librosa.get_duration(y=audio, sr=rate)

        current_wer, current_cer=self.calculate_error_rates(prediction, reference)
        
        # skip averaging if reference contains a (metadata) tag in square brackets
        if not re.findall(tags_regex, reference):
            self.total_clips+=1
            self.total_duration+=duration       

            self.dfResults.loc[self.total_clips] = [clip_file_path, duration, prediction, reference, current_wer, current_cer]
            self.average_wer=100 * wer.compute(predictions=self.dfResults['prediction'].tolist(), references=self.dfResults['reference'].tolist())
            self.average_cer=100 * cer.compute(predictions=self.dfResults['prediction'].tolist(), references=self.dfResults['reference'].tolist())

            print (clip_file_path)           
            print (reference)
            print (prediction)
            print ("WER: %s, CER: %s" % (current_wer, current_cer))    # Avg: %s, %s" % (current_wer, current_cer, self.average_wer, self.average_cer))
            print ("")

        else:
            self.total_ignored_clips+=1
            self.dfIgnoredResults.loc[self.total_clips] = [clip_file_path, duration, prediction, reference, current_wer, current_cer]
            

       
    def print(self):
        print ("Test Statistics: %s" % self.name)
        print ()
        print ("No of Clips: %s" % self.total_clips)        
        print ("Duration: {} hours ({} seconds).".format(datetime.timedelta(seconds=self.total_duration), self.total_duration))
        print ("WER: {:2f}".format(self.average_wer))
        print ("CER: {:2f}".format(self.average_cer))

        print ("No of ignored clips (because of tags etc.): %s" % self.total_ignored_clips)

        print ("")


    def save(self):
        file_name = "results_%s.csv" % self.name
        ignored_file_name = "results_%s_ignored.csv" % (self.name)

        print("Results saved to %s file" % file_name)

        self.dfResults.to_csv(file_name, encoding='utf-8', index=False)
        self.dfIgnoredResults.to_csv(ignored_file_name, encoding='utf-8', index=False)
        


#
def main(testset_csv_file_path, test_name, acoustic_model, language_model, **args):

    # iterate through each audio file and text. 
    test_stats = TestStatistics(test_name)
    
    ds = Model(acoustic_model)
    if len(language_model)>0:
        ds.enableExternalScorer(language_model)
    
    testset_csv_parent_dir=Path(testset_csv_file_path).parent.absolute()

    with open(testset_csv_file_path, 'r', encoding='utf-8') as testset_csv_file:
        testset = csv.DictReader(testset_csv_file)
        for testfile in testset:
            clip_file_path = os.path.join(testset_csv_parent_dir, "clips", testfile["wav_filename"])
            
            audio, rate = librosa.load(clip_file_path, sr=16000)
            duration = librosa.get_duration(y=audio, sr=rate)

            fin = wave.open(clip_file_path, 'rb')
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
            fin.close()

            prediction = ds.stt(audio)
    
            reference=text_preprocess.cleanup(testfile["transcript"])

            test_stats.add(clip_file_path, prediction, reference)                        
    
    test_stats.print()
    test_stats.save()


if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("--test_csv", dest="testset_csv_file_path", required=True)
    parser.add_argument("--test_name", dest="test_name", required=True)
    parser.add_argument("--am", dest="acoustic_model", required=True)
    parser.add_argument("--lm", dest="language_model", default='')
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

