#nblearn

import sys, glob
import re
import math
import string

def tokenize(class_files, class_frequency, vocab):
    for file in class_files:
        file_vocab = []
        with open(file, 'r') as file:
            for line in file:
                isnegation = False
                isPunctuated = False
                for word in line.split():
                    word = word.lower()
                    
                    #end negative sentiment encoding if punctuation is encountered
                    if word[-1] in string.punctuation:
                        isnegation = False
                        isPunctuated = True
                    
                    alphanumeric_word = re.sub(r'[\W_]+', '', word)
                    if alphanumeric_word == '':
                        continue
                    else:
                        
                        #encode negative sentiment
                        if (alphanumeric_word == 'no' or alphanumeric_word == 'not' or alphanumeric_word == 'never') and not isPunctuated:
                            isnegation = True
                        elif isnegation == True:
                            alphanumeric_word = 'NOT_' + alphanumeric_word
                        
                        #add to master vocab 
                        if alphanumeric_word not in vocab:
                            vocab.append(alphanumeric_word) 
                        
                        #binary frequency counts
                        if alphanumeric_word not in file_vocab:
                            file_vocab.append(alphanumeric_word)
                            if alphanumeric_word not in class_frequency:
                                class_frequency[alphanumeric_word] = 1
                            else:
                                class_frequency[alphanumeric_word] += 1
                        else:
                            continue            

def calculate_conditional(class_freq, vocab):
    total_class_freq = len(vocab)
    for word in vocab:
        if word in class_freq:
            total_class_freq += class_freq[word]
    for word in vocab:
        conditional = 0
        if word in class_freq:
            conditional = (class_freq[word] + 1)/total_class_freq
        else:
            conditional = 1/total_class_freq
        class_freq[word] = math.log2(conditional)

def write_class_model(file, class_name, class_conditionals, class_prior):
    file.write(class_name + " prior " + str(class_prior) + "\n")
    for word, conditional in class_conditionals.items():
        if conditional == 0:
            continue
        else:
            file.write(class_name + " " + word + " " + str(conditional) + "\n")

path = sys.argv[1]
positive_truthful = glob.glob(path + '/positive_polarity/truthful_from_TripAdvisor/*/*.txt')
positive_deceptive = glob.glob(path + '/positive_polarity/deceptive_from_MTurk/*/*.txt')
negative_truthful = glob.glob(path + '/negative_polarity/truthful_from_Web/*/*.txt')
negative_deceptive = glob.glob(path + '/negative_polarity/deceptive_from_MTurk/*/*.txt')

#calculate priors
total_docs = len(positive_truthful) + len(positive_deceptive) + len(negative_deceptive) + len(negative_truthful)
positive_truthful_prior = math.log2(len(positive_truthful)/total_docs)
positive_deceptive_prior = math.log2(len(positive_deceptive)/total_docs)
negative_truthful_prior = math.log2(len(negative_truthful)/total_docs)
negative_deceptive_prior = math.log2(len(negative_deceptive)/total_docs)

#calculate conditional probabilites
vocab = []
positive_truthful_freq = {}
positive_deceptive_freq = {}
negative_truthful_freq = {}
negative_deceptive_freq = {}

tokenize(positive_truthful, positive_truthful_freq, vocab)
tokenize(positive_deceptive, positive_deceptive_freq, vocab)
tokenize(negative_truthful, negative_truthful_freq, vocab)
tokenize(negative_deceptive, negative_deceptive_freq, vocab)

calculate_conditional(positive_truthful_freq, vocab)
calculate_conditional(positive_deceptive_freq, vocab)
calculate_conditional(negative_truthful_freq, vocab)
calculate_conditional(negative_deceptive_freq, vocab)

#output model
file = open('nbmodel.txt','w')
write_class_model(file, "positive_truthful", positive_truthful_freq, positive_truthful_prior)
write_class_model(file, "positive_deceptive", positive_deceptive_freq, positive_deceptive_prior)
write_class_model(file, "negative_truthful", negative_truthful_freq, negative_truthful_prior)
write_class_model(file, "negative_deceptive", negative_deceptive_freq, negative_deceptive_prior)


