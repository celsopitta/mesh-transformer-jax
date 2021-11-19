import os
import argparse
import random

import json
from pathlib import Path

def read_squad(path, include_impossible = True):
    path = Path(path)
    with open(path, 'rb') as f:
        squad_dict = json.load(f)

    contexts = []
    questions = []
    answers = []
    tuplas = []
    for group in squad_dict['data']:
        for passage in group['paragraphs']:
            context = passage['context']
            for qa in passage['qas']:
                question = qa['question']
                                
                if include_impossible and qa['is_impossible']:
                    contexts.append(context)
                    questions.append(question)
                    answers.append('<No Answer>')

                    tuplas.append('context: ' + context.strip() + \
                                  '\nquestion: ' + question.strip() + \
                                  '\nanswer: ' + '<No Answer>')
                else:
                    for answer in qa['answers']:
                        contexts.append(context)
                        questions.append(question)
                        answers.append(answer['text'])

                        tuplas.append('context: ' + context.strip() + \
                                    '\nquestion: ' + question.strip() + \
                                    '\nanswer: ' + answer['text'].strip())
                
    return contexts, questions, answers, tuplas

parser = argparse.ArgumentParser("prepara texto")
parser.add_argument("-train","--train",type=str, default='/datasets/Squad_2.0/train-v2.0.json' )
#parser.add_argument("-validation","--validation",type=str, default='//mnt/datasets/Squad_2.0/dev-v2.0.json' )

args = parser.parse_args()
train_file = args.train
#validation_file = args.validation

o_train = open(train_file.replace('.json','.txt'), 'w')
o_validation = open(train_file.replace('.json','_validation.txt'), 'w')

train_contexts, train_questions, train_answers, train_tuples = read_squad(train_file, True)
#val_contexts, val_questions, val_answers, val_tuples = read_squad(validation_file, False)

countv=0
countt=0

def write_tuples(file_train,file_validation, tuples):
    
    countt=0
    countv=0
    random.seed(42)

    for tupla in tuples:
        
        if len(tupla) < 2048 - 2*len('<|endoftext|>'):            
            
            if random.random() > 0.2:    

                file_train.write('<|endoftext|>' + tupla)
                countt+=1
            else:
            
                file_validation.write('<|endoftext|>' + tupla)
                countv+=1

    file_validation.write('<|endoftext|>')
    file_train.write('<|endoftext|>')

    return countt, countv

countt, countv = write_tuples(o_train, o_validation, train_tuples)
#countv = write_tuples(o_validation, val_tuples)

o_train.close()
o_validation.close()

print("train samples: {}\n".format(countt))
print("validation samples: ", countv)

