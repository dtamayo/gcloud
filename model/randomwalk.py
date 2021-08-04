#!/usr/bin/env python
# Copyright 2018 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import argparse
import csv
import math
import pickle
from os import path, makedirs
from random import randint
from sys import exit, stdout, stderr
from time import sleep

import numpy
import pandas


def _parse_args():
    parser = argparse.ArgumentParser('randomwalk', 
                                     description='Monte-Carlo simulation of stock prices '
                                                 'behavior based on data from quandl')
    parser.add_argument('-n', 
                        '--snum', 
                        type=int, 
                        default=1000, 
                        help='number of simulations (default:%(default)s)')
    parser.add_argument('-c', 
                        '--company', 
                        required=True, 
                        help='company symbol on stock (i. e. WDC)')
    parser.add_argument('--from-csv', 
                        help='path to wiki csv file')
    parser.add_argument('-s', 
                        '--start-date', 
                        default='2018-01-01', 
                        help='example: %(default)s')
    return parser.parse_args()


def main():
    args = _parse_args()
    data_model = DataModel(args.company, args.start_date)
    data_model.from_csv = args.from_csv
    data_model.run()


if __name__ == '__main__':
    main()
