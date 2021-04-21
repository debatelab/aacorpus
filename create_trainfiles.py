from aacorpus import *
import json
import jsonlines
import random
import itertools
import re
import os
from tqdm import tqdm
from string import Template
import pandas as pd
random.seed()

CORPUS_ID = "20200818-SYL01"
MIN_WORDS = 130 # minimum size of news splits

# Directories
root_path = "./corpora/"+CORPUS_ID 
jsonl_path = root_path+"/jsonlines" 
src_path = root_path+"/src" 
train_path = root_path+"/traintext" 

# Training Files
TRAIN01 = train_path+'/'+CORPUS_ID+'_basic-min.txt' # basic schemes of Modus barbara, Hypothetical syllogism 1, Generalized Contraposition
TRAIN02 = train_path+'/'+CORPUS_ID+'_basic-all.txt' # all basic schemes
TRAIN03 = train_path+'/'+CORPUS_ID+'_all-all.txt'       # all schemes, basic and variants

trainfile01 = open(TRAIN01,"w") 
trainfile02 = open(TRAIN02,"w") 
trainfile03 = open(TRAIN03,"w") 


# List of all jsonl train files
jsonltfiles = [jsonl_path+'/'+f for f in os.listdir(jsonl_path) if f[-11:]=='train.jsonl']
args_length = len(jsonltfiles)*10000
print('Length Arg Corpus: %s',args_length)
shuffle_ids = list(range(args_length))
random.shuffle(shuffle_ids)


# Reuters news
df_reuters = pd.read_csv("corpora/reuters/polished_stories_trc2v2.csv")
reuters_length = len(df_reuters)
print('Length News Corpus: %s',reuters_length)

# SPGutenberg paragraphs
file1 = open("corpora/spgutenberg/sub_pgcorpus_split-20200814.txt","r") 
parlist = file1.readlines()
file1.close() 
print('Length PGut Corpus: %s',len(parlist))

# Split an shuffle corpora
def partition_sentencewise(text="", min_tokens=50):
    sentences = text.split(". ")
    current = ""
    paragraphs = []
    for s in sentences:
        current = current+" "+s+"."
        if len(current.split(" "))>min_tokens:
            paragraphs.append(current)
            current = ""
    return paragraphs

# nl text corresponding to arg_id
def get_mixin(id):
    sid = shuffle_ids[id]
    if sid >= reuters_length:
        r = parlist[sid-reuters_length]
    else:
        r = df_reuters["story_text"][sid]+"\n"
    return r


# main loop
for jlfile in tqdm(jsonltfiles):
    with jsonlines.open(jlfile) as reader:
        for arg in reader:
            arg_string = arg["premise"]+arg["conclusion"]
            # TRAIN01
            if (arg["scheme_variant"]=="base_scheme") & (arg["base_scheme_group"] in ("Modus barbara","Hypothetical Syllogism 1","Generalized Contraposition")):
                trainfile01.write(arg_string+"\n")                  # Argument
                trainfile01.write(get_mixin(arg["id"]))             # Mixin
            # TRAIN02
            if (arg["scheme_variant"]=="base_scheme"):
                trainfile02.write(arg_string+"\n")                  # Argument
                trainfile02.write(get_mixin(arg["id"]))             # Mixin
            # TRAIN03
            trainfile03.write(arg_string+"\n")                     # Argument
            trainfile03.write(get_mixin(arg["id"]))        # Mixin

# close files
trainfile01.close()
trainfile02.close() 
trainfile03.close()
