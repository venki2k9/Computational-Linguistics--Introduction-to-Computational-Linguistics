import re
import os
import string

file_path =   "/corpora/LDC/LDC02T31/nyt/2000/" #" /Users/tumuluri/unigram/test/"

class UnigramLanguageModel:
    staging_unigram_count = {}
    unigram_count = {}
    sgml_tag_dict = {}
    file_path = ''
    unwanted_char_list = set()

    def __init__(self,fp):
        self.file_path = fp
        pattern = '[^A-Za-z\']'
        self.unwanted_char_list = set(self.matchRegex(pattern, string.printable))


    def matchRegex(self,pattern,data):
        return_list = []
        re_strip_pi = re.compile(pattern)
        match = re_strip_pi.findall(data)
        if match:
            for ele in match:
                return_list.append(ele)
        return return_list


    def ReadAndCleanData(self,data):
        data = data.replace('\r','')
        data = data.replace('\n','')
        data = data.strip()
        return data

    def CollectTags(self,data):
        pattern = '</?[A-Z_]*>'
        all_tags = self.matchRegex(pattern,data)
        if all_tags:
            for tag in all_tags:
                if self.sgml_tag_dict.has_key(tag):
                    self.sgml_tag_dict[tag] = 0

    def IsTag(self,data):
        if self.sgml_tag_dict.has_key(data):
            return True
        else:
            return False

    def FilterUnwantedCharecters(self,data):
        for unwanted_char in self.unwanted_char_list:
            data = data.replace(unwanted_char," ")
        return data

    def SplitFileCollectWords(self,data):
        cleaned_word_list = []
        for word in data.split():
            pattern1 = "[A-Za-z]{1}\'?[A-Za-z]{1,}s'"

            pattern2 = "[A-Za-z]{1}\'?[A-Za-z]{1,}'s"

            pattern3 = "[A-Za-z]'?[A-Za-z]{1,}"

            pattern4 = "[A-Za-z]+"

            if len(self.matchRegex(pattern1, word)) >0:
                cleaned_word_list.append(self.matchRegex(pattern1, word)[0])
            elif len(self.matchRegex(pattern2, word))>0:
                cleaned_word_list.append(self.matchRegex(pattern2, word)[0])
            elif len(self.matchRegex(pattern3, word))>0:
                cleaned_word_list.append(self.matchRegex(pattern3, word)[0])
            elif len(self.matchRegex(pattern4, word))>0:
                cleaned_word_list.append(self.matchRegex(pattern4, word)[0])
            else:
                pass

        return cleaned_word_list

    def UpdateWordCount(self,word,count):
        if self.unigram_count.has_key(word):
            existing_count = self.unigram_count[word]
            self.unigram_count[word] = existing_count + count
        else:
            self.unigram_count[word] = count

    def UpdateStagingWordCount(self,word):
        if self.staging_unigram_count.has_key(word):
            existing_count = self.staging_unigram_count[word]
            self.staging_unigram_count[word] = existing_count + 1
        else:
            self.staging_unigram_count[word] = 1

    def RecordWordCounts(self,word_list,count):
        for word in word_list:
            self.UpdateWordCount(word,count)


    def ProcessFiles(self):
        data = ''
        for f in os.listdir(self.file_path):
            f = os.path.join(self.file_path, f)
            data = open(f, 'r').read()
            for word in data.split():
                word = word.lower()
                self.UpdateStagingWordCount(word)


        for data,word_count in self.staging_unigram_count.iteritems():
            data = self.ReadAndCleanData(data)
            self.CollectTags(data)
            if self.IsTag(data) is False:
                data=self.FilterUnwantedCharecters(data)
                word_list = self.SplitFileCollectWords(data)
                if len(word_list) >0:
                    self.RecordWordCounts(word_list,word_count)

    def getUnigramModel(self):
        return self.unigram_count

unigram_model = UnigramLanguageModel(file_path)
unigram_model.ProcessFiles()
master_counts = unigram_model.getUnigramModel()

for key,count in master_counts.iteritems():
    print(key+" "+str(count))