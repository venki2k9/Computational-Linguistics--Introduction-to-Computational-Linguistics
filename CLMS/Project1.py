import re
from os import listdir
from os.path import isfile, join

master_sentences = []
master_NP = []
master_VP = []
master_DVP = []
master_IVP = []

def construct_parent(idx,input_str,child_idx):
    root_end_index = list(input_str[idx+1:]).index(" ")
    paranthesis_index = list(input_str[idx+1:]).index("(")
    if paranthesis_index > root_end_index:
        root = input_str[idx+1:idx+1+root_end_index]
        root = ('Parent:' + root, idx, child_idx)
    else:
        root = ('Parent:StringStart', idx, child_idx)

    return root


def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    loop = 0
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            if len(stack)>0:
                loop=stack[-1]
                loop = construct_parent(loop,string,start)
            else:
                loop='Parent:Root'
            yield ( (loop,"level:"+str(len(stack))), string[start + 1: i])


file_path = '/corpora/LDC/LDC99T42/RAW/parsed/prd/wsj/14/'

for f in listdir(file_path):
    f = join(file_path, f)
    with open(f, 'r') as myfile:
        input_string = myfile.read()
    sentence_count=0
    np_count=0
    vp_count=0
    dvp_count = 0
    ivp_count=0

    input_string = '('+input_string+')'
    result = list(parenthetic_contents(input_string))
    tags =[]
    for ele in result:
        element_metadata = ele[0]
        tags.append(element_metadata[0])
    tag_set = set(tags)
    tag_dict = {}
    for ele in tag_set:
         tag_dict[ele[1]] = (ele[0],ele[2])

    child_set = set()
    for ele in tag_set:
        if not tag_dict.has_key(ele[2]):
            child_set.add(ele[2])

    child_dict = {}
    for ele in result:
        if ("(" not in ele[1]) and (")" not in ele[1]):
            child_dict[ele[0][0][2]] = ele[1]

    child_sentence_count = 0
    child_vp_count = 0
    child_np_count = 0
    for ele in child_set:
        if child_dict.has_key(ele):
            child_stripped = filter( lambda x: x in set(['S','VP','NP']) , child_dict[ele].split(" "))
            if len(child_stripped) > 0 :
                if child_stripped[0] == 'S':
                    child_sentence_count = child_sentence_count + 1
                if child_stripped[0] == 'VP':
                    child_vp_count = child_vp_count + 1
                if child_stripped[0] == 'NP':
                    child_np_count = child_np_count + 1




    sentence_count = len(set(map( lambda x: (x[0],x[1]) ,filter(lambda x: x[0] == 'Parent:S', tags)))) + child_sentence_count
    np_count = len(set(map( lambda x: (x[0],x[1]) ,filter(lambda x: x[0] == 'Parent:NP', tags)))) + child_np_count
    vp_count = len(set(map( lambda x: (x[0],x[1]) ,filter(lambda x: x[0] == 'Parent:VP', tags)))) + child_vp_count



    vp_list = filter(lambda x: x[0][0][0] =='Parent:VP', result)


    vp_dict = {}

    for ele in vp_list:
        parent = ele[0][0][1]
        child = ele[0][0][2]

        if vp_dict.has_key(tag_dict[parent]):
             val = vp_dict[tag_dict[parent]]
             if val is not None:
                 if tag_dict.has_key(child):
                     val.append(tag_dict[child])
                 else:
                     val.append(child)
        else:
             val_list = []
             if tag_dict.has_key(child):
                 val_list.append(tag_dict[child])
             else:
                 val_list.append(child)

             vp_dict[tag_dict[parent]] = val_list




    for parent,child in vp_dict.iteritems():
        np_cnt=0
        non_np_cnt= 0
        for ele in child:
            if type(ele) is tuple:
                if ele[0] == 'Parent:NP':
                    np_cnt = np_cnt +1
                else:
                    non_np_cnt = non_np_cnt + 1
            else:
                if 'NP' in set(child_dict[ele].split(" ")):
                    np_cnt = np_cnt + 1
                else:
                    non_np_cnt = non_np_cnt + 1

        if np_cnt ==2:
            dvp_count = dvp_count + 1

    ivp_count = child_vp_count

    master_sentences.append(sentence_count)
    master_NP.append(np_count)
    master_VP.append(vp_count)
    master_DVP.append(dvp_count)
    master_IVP.append(ivp_count)



total_sentences = reduce(lambda x, y: x + y, master_sentences)
total_noun_phrases = reduce(lambda x, y: x + y, master_NP)
total_verb_phrases = reduce(lambda x, y: x + y, master_VP)
total_ditransitive_verb_prhases = reduce(lambda x, y: x + y, master_DVP)
total_intransitive_verb_phrases = reduce(lambda x, y: x + y, master_IVP)


print("Sentence    " + str(total_sentences))
print("Noun Phrase  "+ str(total_noun_phrases))
print("Verb Phrases "+str(total_verb_phrases))
print("Ditransitive Verb Phrases    "+str(total_ditransitive_verb_prhases))
print("Intransitive Verb Phrases    "+str(total_intransitive_verb_phrases))