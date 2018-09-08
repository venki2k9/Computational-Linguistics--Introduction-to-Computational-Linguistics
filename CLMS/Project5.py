import os
import numpy as np
import codecs
import unicodedata
import sys

language_models_loc = '/opt/dropbox/18-19/473/project5/language-models'

train_file = '/opt/dropbox/18-19/473/project5/train.txt'
test_file = '/opt/dropbox/18-19/473/project5/test.txt'

extra_train_file =  '/opt/dropbox/18-19/473/project5/extra-train.txt'
extra_test_file = '/opt/dropbox/18-19/473/project5/extra-test.txt'

language_score_cache = {}

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

data_type = sys.argv[1]

def remove_punctuation(text):
    return text.translate(tbl)

#building the language model score cache
for f in os.listdir(language_models_loc):
    lang_code = f.replace('.unigram-lm','')
    f = os.path.join(language_models_loc, f)
    file = codecs.open(f, encoding="latin-1")
    lines = file.readlines()
    scores_dict = {}
    for line in lines:
        line = line.strip()
        line_split = line.split('\t')
        word = line_split[0]
        word_count = int(line_split[1])
        scores_dict[word] = word_count

    language_score_cache[lang_code] = scores_dict


def ProbabilityWordGivenLanguage(language,word,method='add-one-smoothing'):
    min_prob_of_word = np.min(language_score_cache[language].values())
    if language_score_cache[language].has_key(word):
        word_freq = language_score_cache[language][word]
    else:
        if method == 'add-one-smoothing':
            word_freq = 0
        else:
            word_freq = min_prob_of_word
    total_word_freq = np.sum(language_score_cache[language].values())
    distinct_word_count = len(language_score_cache[language].keys())
    conditional_prob =  (float(word_freq)+1.00)/(float(total_word_freq) + float(distinct_word_count))
    log_conditional_prob = np.log10(conditional_prob)
    return log_conditional_prob

def accuracy(results):
    correct = 0
    for ele in results:
        if ele[0] == ele[1]:
            correct = correct + 1
    acc =  float(correct) * 100.00 / float(len(results))
    return acc


def Predict(train_file,method):
    file = codecs.open(train_file, encoding="latin-1")
    lines = file.readlines()
    results_list = []
    for line in lines:
        print(line.encode('utf-8'))
        line = remove_punctuation(line)
        line = line.strip()
        train_language_label_or_id = line.split('\t')[0]
        line_split = line.split('\t')[1].split(" ")
        max_lang_code_log_prob = None
        most_probable_lang_code = None
        for lang_code in language_score_cache.keys():
            lang_code_log_prob = 0
            for word in line_split:
                lang_code_log_prob = lang_code_log_prob + ProbabilityWordGivenLanguage(lang_code,word,method)
            print(lang_code+'\t'+str(lang_code_log_prob))
            if max_lang_code_log_prob:
                if max_lang_code_log_prob < lang_code_log_prob:
                    max_lang_code_log_prob = lang_code_log_prob
                    most_probable_lang_code = lang_code
            else:
                max_lang_code_log_prob = lang_code_log_prob
                most_probable_lang_code = lang_code

        print("result"+'\t'+ most_probable_lang_code)
        results_list.append((train_language_label_or_id,most_probable_lang_code) )

    return results_list



#results = Predict(extra_train_file,method='add-one-smoothing')
#print("accuracy:"+ str( accuracy(results) ))

if data_type == 'train':
    results = Predict(train_file,method='rarest-prob')
elif data_type == 'test':
    results = Predict(test_file, method='rarest-prob')
elif data_type == 'extra_train':
    results = Predict(extra_train_file, method='rarest-prob')
else:
    results = Predict(extra_test_file, method='rarest-prob')

#print("accuracy:"+ str( accuracy(results) ))






