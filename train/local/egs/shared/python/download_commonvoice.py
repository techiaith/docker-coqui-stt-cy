#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import tarfile
import shlex
import shutil
import subprocess
import glob

import download_manager 

from pathlib import Path
from argparse import ArgumentParser, RawTextHelpFormatter

from data_url import _DATA_URL

DESCRIPTION = """

"""

def move_clips(target_dir):

    # files may exist in levels of subdirectories. Need to move them
    # up to the target_dir
    extracted_clips_path = glob.glob(os.path.join(target_dir,"**","clips"), recursive=True)
    if len(extracted_clips_path) > 0:
        extracted_clips_parent_path = str(Path(extracted_clips_path[0]).parent)
        for file_path in glob.glob(extracted_clips_parent_path + "/*"):
            print ("Moving from %s to %s " % (file_path, target_dir)) 
            shutil.move(file_path, target_dir)


def main(cv_root_dir, **args):
    print ("Downloading and extracting CommonVoice to %s..." % cv_root_dir)
    if not Path(cv_root_dir).is_dir():
        tgz_file_path = download_manager.download(_DATA_URL, cv_root_dir)
        download_manager.extract(tgz_file_path)
        move_clips(cv_root_dir)
    
    #
    print ("Preparing with import_cv2.py")
    cmd = "python3 /code/bin/import_cv2.py %s --validate_label_locale /code/bin/bangor_welsh/egs/shared/python/validate_label_locale.py" % (cv_root_dir)

    import_process = subprocess.Popen(shlex.split(cmd))
    import_process.wait()



if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--target_dir", dest="cv_root_dir", required=True, help="target directory for extracted archive, also root directory for training data")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

