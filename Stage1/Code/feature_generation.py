
import os
import re
import math
import nltk
import csv
import operator

train_files_path = "/Users/raghavan/PycharmProjects/DataScience/Dataset/AllFiles/train/"
test_files_path = "/Users/raghavan/PycharmProjects/DataScience/Dataset/AllFiles/test/"
word_count = {}
word_count_file = {}
file_word_count = {}
feature_vector = []
no_of_files = 0
feature_vector = []
next_word_tag = {}

def get_files(path):
    files = os.listdir(path)
    return files

def get_before(words, i, flag):
    before = ""
    if flag:
        if i>=3:
            before = words[i-3] + " " + words[i-2]
        elif i>=2:
            before = words[i-2]
    else:
        if(i >= 2):
            before = words[i-2] + " " + words[i-1]
        elif(i >= 1):
            before = words[i-1]
    return before

def get_after(words, i, flag):
    after = ""
    if(i < len(words)-2):
        after = words[i+1] + " " + words[i+2]
    elif(i < len(words)-1):
        after = words[i+1]
    return after


def word_counts(files, path):
    total_word_count = 0
    for file in files:
        count = 0
        file_dict = {}
        with open(path + file) as f:
            file_content = f.read()
        file_content_re = re.compile(r'[^\s\.][^\.\n]+')
        lines = file_content_re.findall(file_content)
        for line in lines:
            line = line.replace("<name>","")
            line = line.replace("</name>","")
            result = [x.strip() for x in line.split()]
            for word in result:
                count = count + 1
                word_count[word] = word_count.get(word, 0) + 1
                file_dict[word] = file_dict.get(word, 0) + 1
        total_word_count = total_word_count + count
        file_word_count[file] = count
        word_count_file[file] = file_dict
    print total_word_count

def is_word_title(word):
    return word.istitle()

def is_word_noun(word, pos_tag):
    for pos_tag_item in pos_tag:
        if pos_tag_item[0] == word:
            if pos_tag_item[1] == 'NN' or pos_tag_item[1] == 'NNP' or pos_tag_item[1] == 'NNS':
                return 1
    return 0

def keywords_before(word):
    before_keywords = ["sir", "captain", "spinner",
                       "drives", "sweeps", "off", "with",
                       "bowler", "coach", "chairman", "batsman",
                       "paceman", "said", "when", "and", "added",
                       "feels", "spokesman", "skipper", "by", "manager", "director", "against", "striker", "goalkeeper"]
    if word:
        if word[0].lower() in before_keywords:
            return 1
    return 0

def keywords_after(word):
    after_keywords = ["is", "was", "has",
                      "had", "played", "bowled",
                      "who", "said", "batsman", "whose",
                      "and", "opener", "after", "batted", "says", "told", "of", "in", "said:", "for"]
    if word:
        if word[0].lower() in after_keywords:
            return 1
    return 0

def is_name(word):
    temp = word
    temp = strip_word(temp)
    if temp == word:
        return 0
    return 1

def strip_word(word):
    word = word.replace("<name>", "")
    word = word.replace("</name>", "")
    return word

def word_stop_word(word):
    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
                  "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
                  'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
                  'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
                  'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
                  'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
                  'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                  'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                  'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                  'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                  'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
                  'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd',
                  'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',
                  "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn',
                  "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
                  'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",
                  "mr", "ms", "the"]
    for w in word:
        if w in stop_words:
            return 1
    return 0

def compute_tfidf(word, file):
    tf_value = (float)(word_count_file[file].get(word, 0)) / file_word_count[file]
    df_value = (float)(word_count.get(word, 0)) / no_of_files
    tf_idf = ((float)(tf_value) / (1+df_value))
    if tf_idf == 0.0:
        return 0.0
    return math.log(tf_idf)

def word_tf(word, file):
    if word:
        return (float)(word_count_file[file].get(word[0], 0)) / file_word_count[file]
    return 0

def word_df(word, file):
    if word:
        return (float)(word_count.get(word[0], 0)) / no_of_files
    return 0

def next_word_verb(after):
    if after:
        if len(after[0]) > 1 and after[0][-2] == "ed":
            return 1
    return 0

def before_word_pos_tag(word, pos_tag):
    if word:
        for pos_tag_item in pos_tag:
            if pos_tag_item[0] == word[0]:
                if pos_tag_item[1] == 'CC' or pos_tag_item[1] == 'NN' or pos_tag_item[1] == 'NNP':
                    return 1
    return 0

def after_word_pos_tag(word, pos_tag, label):
    if label:
        if word:
            for pos_tag_item in pos_tag:
                if pos_tag_item[0] == word[0]:
                    if pos_tag_item[1] == 'VBD' or pos_tag_item[1] == 'VBG' or pos_tag_item[1] == 'NNP':
                        return 1
    return 0

def is_first_word(before):
    if before:
        return 0
    return 1

def get_feature_vector(word, before, after, pos_tag, file):
    feature_vector_word = []
    feature_vector_dict = {}
    label = is_name(word)
    word = strip_word(word)
    before = strip_word(before)
    after = strip_word(after)
    before = before.split()
    before.reverse()
    after = after.split()
    feature_vector_dict['is_word_title'] = is_word_title(word)
    feature_vector_dict['is_word_noun'] = is_word_noun(word, pos_tag)
    feature_vector_dict['keywords_before'] = keywords_before(before)
    feature_vector_dict['keywords_after'] = keywords_after(after)
    feature_vector_dict['word_stop_word'] = word_stop_word(word)
    feature_vector_dict['before_word_tf'] = word_tf(before, file)
    feature_vector_dict['before_word_df'] = word_df(before, file)
    feature_vector_dict['before_word_pos'] = before_word_pos_tag(before, pos_tag)
    feature_vector_dict['is_first_word'] = is_first_word(before)
    feature_vector_dict['after_word_tf'] = word_tf(after, file)
    feature_vector_dict['after_word_df'] = word_df(after, file)
    feature_vector_dict['after_word_pos'] = after_word_pos_tag(after, pos_tag, label)
    feature_vector_dict['next_word_verb'] = next_word_verb(after)
    feature_vector_dict['label'] = label
    feature_vector.append(feature_vector_dict)

def get_processed_data(files, path):
    count = 0
    for file in files:
        if not file.endswith(".txt"):
            continue

        with open(path + file) as f:
            file_content = f.read()
        file_content_re = re.compile(r'[^\s\.][^\.\n]+')
        lines = file_content_re.findall(file_content)
        for line in lines:
            temp = line
            temp = strip_word(temp)
            result = [x.strip() for x in line.split()]
            pos_tag = nltk.pos_tag(temp.split())
            for i in range(len(result)):
                count = count + 1
                before = get_before(result, i, 0)
                after = get_after(result, i, 0)
                get_feature_vector(result[i], before, after, pos_tag, file)
                if i < len(result) - 1:
                    before = get_before(result, i+1, 1)
                    after = get_after(result, i+1, 1)
                    get_feature_vector(result[i]+" "+result[i+1], before, after, pos_tag, file)

fieldnames = ['is_word_title', 'is_word_noun', 'keywords_before',
                  'keywords_after', 'word_stop_word', 'before_word_tf', 'before_word_df', 'before_word_pos',
                   'is_first_word', 'after_word_tf', 'after_word_df',
       'after_word_pos',
                  'next_word_verb',
                  'label']
if __name__ == "__main__":
    files = get_files(train_files_path)
    no_of_files = len(files)
    word_counts(files, train_files_path)
    get_processed_data(files, train_files_path)
    with open('trainFeature.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(feature_vector)
    word_count = {}
    word_count_file = {}
    file_word_count = {}
    feature_vector = []
    no_of_files = 0
    files = get_files(test_files_path)
    no_of_files = len(files)
    word_counts(files, test_files_path)
    get_processed_data(files, test_files_path)
    with open('testFeature.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(feature_vector)


