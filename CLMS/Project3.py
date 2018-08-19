##!/opt/python-2.7/bin/python2.7 -S
##  -*- coding: utf-8 -*-

# Script to copy standard input to standard output, one line at a time.

# This gets various items to interfaces with the OS, including the
# standard input stream.
import sys
import os
import encodings

# This is apparently for Python rogues, but I got it from SO and it seems to work.
# http://stackoverflow.com/questions/11741574/how-to-set-the-default-encoding-to-utf-8-in-python
# A key trick is the -S business above in the shebang line.
#sys.setdefaultencoding("UTF-8")

print sys.getdefaultencoding()
import site

import codecs

V1 = u"\u0E40\u0E41\u0E42\u0E43\u0E44"
C1 = u"\u0E01\u0E02\u0E03\u0E04\u0E05\u0E06\u0E07\u0E08\u0E09\u0E0A\u0E0B\u0E0C\u0E0D\u0E0E\u0E0F" \
     + u"\u0E10\u0E11\u0E12\u0E13\u0E14\u0E15\u0E16\u0E17\u0E18\u0E19\u0E1A\u0E1B\u0E1C\u0E1D\u0E1E\u0E1F" \
     + u"\u0E20\u0E21\u0E22\u0E23\u0E24\u0E25\u0E26\u0E27\u0E28\u0E29\u0E2A\u0E2B\u0E2C\u0E2D\u0E2E"
C2 = u"\u0E23\u0E25\u0E27\u0E19\u0E21"
V2 = u"\u0E34\u0E35\u0E36\u0E37\u0E38\u0E39\u0E31\u0E47"
T = u"\u0E48\u0E49\u0E4A\u0E4B"
V3 = u"\u0E32\u0E2D\u0E22\u0E27"
C3 = u"\u0E07\u0E19\u0E21\u0E14\u0E1A\u0E01\u0E22\u0E27"


master_char_dict = {}


def PopulateMasterDict(chr,chr_set):
    if master_char_dict.has_key(chr):
        master_char_dict[chr][chr_set] = chr
    else:
        d = dict()
        d[chr_set] = chr
        master_char_dict[chr] = d


for chr in V1:
    PopulateMasterDict(chr,"V1")
for chr in C1:
    PopulateMasterDict(chr, "C1")
for chr in C2:
    PopulateMasterDict(chr, "C2")
for chr in V2:
    PopulateMasterDict(chr, "V2")
for chr in T:
    PopulateMasterDict(chr, "T")
for chr in V3:
    PopulateMasterDict(chr, "V3")
for chr in C3:
    PopulateMasterDict(chr, "C3")

final_states_set = set([7,8,9])

def GenerateFSM():
    FSM = []

    for i in range(10):
        d = dict()
        FSM.append(d)

    FSM[0]["V1"] = 1
    FSM[0]["C1"] = 2
    FSM[0]["C2"] = None
    FSM[0]["V2"] = None
    FSM[0]["T"] = None
    FSM[0]["V3"] = None
    FSM[0]["C3"] = None
    FSM[0]["br"] = False
    FSM[0]["prev"] = False
    FSM[0]["order"] = ["V1","C1"]

    FSM[1]["V1"] = None
    FSM[1]["C1"] = 2
    FSM[1]["C2"] = None
    FSM[1]["V2"] = None
    FSM[1]["T"] = None
    FSM[1]["V3"] = None
    FSM[1]["C3"] = None
    FSM[1]["br"] = False
    FSM[1]["prev"] = False
    FSM[1]["order"] = ["C1"]

    FSM[2]["V1"] = 7
    FSM[2]["C1"] = 8
    FSM[2]["C2"] = 3
    FSM[2]["V2"] = 4
    FSM[2]["T"] = 5
    FSM[2]["V3"] = 6
    FSM[2]["C3"] = 9
    FSM[2]["br"] = False
    FSM[2]["prev"] = False
    FSM[2]["order"] = ["C2","V2","T","V3","C3","V1","C1"]

    FSM[3]["V1"] = None
    FSM[3]["C1"] = None
    FSM[3]["C2"] = None
    FSM[3]["V2"] = 4
    FSM[3]["T"] = 5
    FSM[3]["V3"] = 6
    FSM[3]["C3"] = 9
    FSM[3]["br"] = False
    FSM[3]["prev"] = False
    FSM[3]["order"] = ["V2","T","V3","C3"]

    FSM[4]["V1"] = 7
    FSM[4]["C1"] = 8
    FSM[4]["C2"] = None
    FSM[4]["V2"] = None
    FSM[4]["T"] = 5
    FSM[4]["V3"] = 6
    FSM[4]["C3"] = 9
    FSM[4]["br"] = False
    FSM[4]["prev"] = False
    FSM[4]["order"] = ["T","V3","C3","V1","C1"]


    FSM[5]["V1"] = 7
    FSM[5]["C1"] = 8
    FSM[5]["C2"] = None
    FSM[5]["V2"] = None
    FSM[5]["T"] = None
    FSM[5]["V3"] = 6
    FSM[5]["C3"] = 9
    FSM[5]["br"] = False
    FSM[5]["prev"] = False
    FSM[5]["order"] = ["V3","C3","V1","C1"]

    FSM[6]["V1"] = 7
    FSM[6]["C1"] = 8
    FSM[6]["C2"] = None
    FSM[6]["V2"] = None
    FSM[6]["T"] = None
    FSM[6]["V3"] = None
    FSM[6]["C3"] = 9
    FSM[6]["br"] = False
    FSM[6]["prev"] = False
    FSM[6]["order"] = ["C3","V1","C1"]


    FSM[7]["next_state"] = 1
    FSM[7]["br"] = True
    FSM[7]["prev"] = True
    FSM[7]["order"] = ["next_state"]



    FSM[8]["next_state"] = 2
    FSM[8]["br"] = True
    FSM[8]["prev"] = True
    FSM[8]["order"] = ["next_state"]


    FSM[9]["next_state"] = 0
    FSM[9]["br"] = True
    FSM[9]["prev"] = False
    FSM[9]["order"] = ["next_state"]

    #print(FSM[0])
    return FSM


file_path = "/Users/tumuluri/CLMS-Projects/Project3/fsm-input.utf8.txt"
fl = open(file_path,'r')

print u"<html><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><body>"
FSM = GenerateFSM()

for line in fl.readlines():
    line = line.rstrip()
    fsm_modified_line = ''.encode('UTF-8')
    state = 0
    next_state = 0
    for chr in line.decode('UTF-8'):
        if state in final_states_set:
            state = FSM[state]["next_state"]

        required_chr_set = ""
        for chr_set in FSM[state]["order"]:
            if master_char_dict[chr].has_key(chr_set):
                required_chr_set = chr_set
            else:
                pass

        brk = FSM[state]["br"]
        prevChr = FSM[state]["prev"]

        if state not in final_states_set:
            next_state = FSM[state][required_chr_set]

        next_brk = FSM[next_state]["br"]
        next_prevChr = FSM[next_state]["prev"]
        if next_brk and next_prevChr:
             fsm_modified_line = fsm_modified_line+" ".encode('UTF-8')+chr
        elif next_brk and not next_prevChr:
            fsm_modified_line = fsm_modified_line + chr+ " ".encode('UTF-8')
        else:
            fsm_modified_line = fsm_modified_line + chr


        state = next_state

    fsm_modified_line = fsm_modified_line + "</br>"
    print(fsm_modified_line)
print u"</body></html>"

file_path = "/Users/tumuluri/CLMS-Projects/Project3/fsm-input.utf8.txt"
fl = open(file_path,'r')

print u"<html><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><body>"
FSM = GenerateFSM()

for line in fl.readlines():
    line = line.rstrip()
    fsm_modified_line = ''.encode('UTF-8')
    state = 0
    next_state = 0
    for chr in line.decode('UTF-8'):
        if state in final_states_set:
            state = FSM[state]["next_state"]

        required_chr_set = ""
        for chr_set in FSM[state]["order"]:
            if master_char_dict[chr].has_key(chr_set):
                required_chr_set = chr_set
            else:
                pass

        brk = FSM[state]["br"]
        prevChr = FSM[state]["prev"]

        if state not in final_states_set:
            next_state = FSM[state][required_chr_set]

        next_brk = FSM[next_state]["br"]
        next_prevChr = FSM[next_state]["prev"]
        if next_brk and next_prevChr:
             fsm_modified_line = fsm_modified_line+" ".encode('UTF-8')+chr
        elif next_brk and not next_prevChr:
            fsm_modified_line = fsm_modified_line + chr+ " ".encode('UTF-8')
        else:
            fsm_modified_line = fsm_modified_line + chr


        state = next_state

    fsm_modified_line = fsm_modified_line + "</br>"
    print(fsm_modified_line)
print u"</body></html>"