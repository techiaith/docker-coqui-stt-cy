#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from text_preprocess import cleanup

def validate_label(label):
    return cleanup(label)
