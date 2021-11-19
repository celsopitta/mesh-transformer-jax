import os
import argparse
import random

import pandas  




parser = argparse.ArgumentParser("prepara texto")
parser.add_argument("-i","--input",type=str, default='/mnt/datasets/Squad_2.0/SQuAD_csv.csv' )
parser.add_argument("-o","--output",type=str, default='/mnt/datasets/Squad_2.0/SQuAD_csv.txt' )


args = parser.parse_args()
input_file = args.input
output_file = args.output


colnames = ['index', 'context', 'question','id','answer_start','text']
data = pandas.read_csv(input_file, names=colnames)

context=data.context.tolist()
questions=data.question.tolist()
answers=data.text.tolist()

ofile = open(output_file, 'w')

countt = 0
countv = 0
countd = 0

index = 1
max_len = 0

random.seed(42)

while(index<len(context)):

    tupla = '<|endoftext|>context: '+str(context[index]).replace("“","\'").replace("\"","\'").replace("”","\'").strip() + \
            '\nquestion: ' +        str(questions[index]).replace("“","\'").replace("\"","\'").replace("”","\'").strip() + \
            '\nanswer: ' +          str(answers[index]).replace("“","\'").replace("\"","\'").replace("”","\'").strip()

    if len(tupla) < 2048:
        ofile.write(tupla)
        countv+=1

        if len(tupla)>max_len:

            max_len = len(tupla)
    else:
        countd +=1

    index +=1

ofile.write('<|endoftext|>')
print("max len:", max_len)
print("samples: {}\n".format(countv))
print("discarted: ", countd)
ofile.close()

