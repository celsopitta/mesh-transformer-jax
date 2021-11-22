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
    max_answer = 0
    for tuple in tuples:
        
        answer = '<No Answer>'
        if len(tuple['answers']['text']) > 0:
            answer = tuple['answers']['text'][0]

        if max_answer < len(answer):
            max_answer = len(answer)

        train_tuple = '<|endoftext|>context: ' + tuple['context'].strip() + \
                    '\nquestion: ' + tuple['question'].strip() + \
                    '\nanswer: ' + answer.strip()

        if len(train_tuple) < 2030:
            file.write(train_tuple)
            countt+=1

    file.write('<|endoftext|>')
    return countt, max_answer



def write_limpo(file, tuples):
    countt=0
    for key in tuples.keys():
        
        train_tuple = '<|endoftext|>context: ' + tuples[key]['context'].strip() + \
                    '\nquestion: ' + str(key).strip() + \
                    '\nanswer: ' + tuples[key]['answer'].strip()

        if len(train_tuple) < 2048 - 230:
            file.write(train_tuple)
            countt+=1

    file.write('<|endoftext|>')
    return countt



def clean_duplicates(tuples, include_impossible=False):

    train_limpo = {}
    for tuple in tuples:

        if tuple['question'] not in train_limpo:

            answer = '<No Answer>'
            if len(tuple['answers']['text']) > 0:
                answer = tuple['answers']['text'][0]
            
            if include_impossible or answer != '<No Answer>':

                train_limpo[tuple['question']] ={}
                train_limpo[tuple['question']]['context'] = tuple['context']
                train_limpo[tuple['question']]['answer'] = answer

    return train_limpo

train_limpo = clean_duplicates(train_ds)
validation_limpo = clean_duplicates(validation_ds)

countt = write_limpo(o_train, train_limpo)
countv = write_limpo(o_validation, validation_limpo)

o_train.close()
o_validation.close()

print("train samples: {}\n".format(countt))
print("validation samples: ", countv)
