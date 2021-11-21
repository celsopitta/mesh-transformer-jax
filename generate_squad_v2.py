import os
import argparse
import random

import json
from pathlib import Path

import datasets 


parser = argparse.ArgumentParser("prepara texto")
parser.add_argument("-project_name","--project_name",type=str, default='gptj-squad_v2' )

train_ds = datasets.load_dataset('squad_v2', split='train')
validation_ds = datasets.load_dataset('squad_v2', split='validation')

train_ds.shuffle(42)
validation_ds.shuffle(42)

args = parser.parse_args()
project_name = args.project_name

o_train = open(f"{project_name}_train_.txt", 'w')
o_validation = open(f"{project_name}_validation_.txt", 'w')

countv=0
countt=0

def write_file(file, tuples):
    countt=0
    for tuple in tuples:
        
        answer = '<No Answer>'
        if len(tuple['answers']['text']) > 0:
            answer = tuple['answers']['text'][0]
        
        train_tuple = '<|endoftext|>context: ' + tuple['context'].strip() + \
                    '\nquestion: ' + tuple['question'].strip() + \
                    '\nanswer: ' + answer.strip()

        if len(train_tuple) < 2030:
            file.write(train_tuple)
            countt+=1

    file.write('<|endoftext|>')
    return countt



countt = write_file(o_train, train_ds)
countv = write_file(o_validation, validation_ds)

o_train.close()
o_validation.close()

print("train samples: {}\n".format(countt))
print("validation samples: ", countv)
