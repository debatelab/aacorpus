from aacorpus import *
import json
import jsonlines
import random
import itertools
import re
import os
from tqdm import tqdm
from string import Template
random.seed()

CORPUS_ID = "20201106-TEST_ONLY-SYL02"
SIZE_TRAIN = 9000
SIZE_TEST = 100

# Global arg_id counter
arg_id = 1


# Load config
config_file = open('conf_syllogistic_corpus-02.json')
config_str = config_file.read()
corpus_config = json.loads(config_str)

# Config ids
domain_ids = [domain["id"] for domain in corpus_config["domains"]]
scheme_ids = [s["id"] for s in corpus_config["formal_argument_schemes"]]


# Directories
root_path = "./corpora/"+CORPUS_ID 
jsonl_path = root_path+"/jsonlines" 
src_path = root_path+"/src" 
train_path = root_path+"/traintext" 

try: 
    os.makedirs(jsonl_path)
    os.makedirs(src_path)
    os.makedirs(train_path)
except OSError:
    print ("Creation of the directories failed.")
else:
    print ("Successfully created the directories.")



def create_train_json(scheme_id):
    global arg_id
    file = jsonl_path+'/'+CORPUS_ID+'-'+scheme_id+'-train.jsonl'
    with jsonlines.open(file, mode='w') as writer:
        for i in range(SIZE_TRAIN):
            argument = pipeline_create_argument(corpus_config, 
                                                random.choice(domain_ids), 
                                                scheme_id, 
                                                permutate_premises=True,
                                                argument_id=arg_id,
                                                split_arg=False)
            arg_id = arg_id + 1
            writer.write(argument)   

    return True


def create_test_json(scheme_id):
    global arg_id
    file = jsonl_path+'/'+CORPUS_ID+'-'+scheme_id+'-test.jsonl'
    with jsonlines.open(file, mode='w') as writer:
        for i in range(SIZE_TEST):
            argument = pipeline_create_argument(corpus_config, 
                                                random.choice(domain_ids), 
                                                scheme_id, 
                                                permutate_premises=True,
                                                argument_id=arg_id,
                                                split_arg=True)
            arg_id = arg_id + 1
            writer.write(argument)   

    return True


# Main loop: iterate over schemes
for scheme_id in tqdm(scheme_ids):
    # create_train_json(scheme_id)
    create_test_json(scheme_id)

