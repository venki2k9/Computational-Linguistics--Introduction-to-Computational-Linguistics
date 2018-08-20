import re
from os import listdir
from os.path import isfile, join

str = "Ocomes's"
str = "O'conners's"
str = "storied'"
str = "l'ore"

pattern1 = "[A-Za-z]{1}\'?[A-Za-z]{1,}s'?"

pattern2 = "[A-Za-z]{1}\'?[A-Za-z]{1,}'s?"

pattern3 = "[A-Za-z]'?[A-Za-z]{1,}"

pattern4 = "[A-Za-z]+"


pattern='NOT'
targ_str = '(S=100 AND NOT(S=200 OR s=300))'
re_strip_pi1 = re.compile(pattern)
targ_match = re_strip_pi1.findall(targ_str)

print(targ_match)

result = []

re_strip_pi1 = re.compile(pattern1)
match1 = re_strip_pi1.findall(str)

re_strip_pi2 = re.compile(pattern2)
match2 = re_strip_pi2.findall(str)

re_strip_pi3 = re.compile(pattern3)
match3 = re_strip_pi3.findall(str)

if match1:
    for ele in match1:
        print("match1")
        result.append(ele)
elif match2:
    for ele in match2:
        print("match2")
        result.append(ele)
elif match3:
    for ele in match3:
        print("match3")
        result.append(ele)
else:
    pass



if result:
    print(result)


print u"<html><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><body>"
print(u"\u0E48")
print u"</body></html>"



file_path = "/Users/tumuluri/CLMS-Projects/Project3/fsm-input.utf8.txt"
fl = open(file_path,'r')

print u"<html><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><body>"

for line in fl.readlines():
    #line = line.rstrip()
    fsm_modified_line = ''.encode('UTF-8')
    eof = False
    idx = 0
    line = line.decode('UTF-8')
    while not eof:
        chr = line[idx]
        if chr == '\n'.encode('UTF-8'):
            eof = True
        print("chr:"+chr)
        idx = idx + 1
    break