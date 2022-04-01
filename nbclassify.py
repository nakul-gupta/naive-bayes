#nbclassify

import sys, glob
import re
import string

def classify(file, model):
    prediction = {
        "positive_truthful": model["positive_truthful"]['prior'],
        "positive_deceptive": model["positive_deceptive"]['prior'],
        "negative_truthful": model["negative_truthful"]['prior'],
        "negative_deceptive": model["negative_deceptive"]['prior']
    }
    with open(file, 'r') as file:
            for line in file:
                for word in line.split():
                    word = word.lower()
                    isnegation = False
                    isPunctuated = False
                        
                    #end negative sentiment encoding if punctuation is encountered
                    if word[-1] in string.punctuation:
                        isnegation = False
                        isPunctuated = True

                    #negative sentiment encoding
                    alphanumeric_word = re.sub(r'[\W_]+', '', word)
                    if (alphanumeric_word == 'no' or alphanumeric_word == 'not' or alphanumeric_word == 'never') and not isPunctuated:
                        isnegation = True
                    elif isnegation == True:
                        alphanumeric_word = 'NOT_' + alphanumeric_word
                                    
                    if alphanumeric_word in model["positive_truthful"]:
                        prediction['positive_truthful'] += model['positive_truthful'][alphanumeric_word]
                    if alphanumeric_word in model["positive_deceptive"]:
                        prediction['positive_deceptive'] += model['positive_deceptive'][alphanumeric_word]
                    if alphanumeric_word in model["negative_truthful"]:
                        prediction['negative_truthful'] += model['negative_truthful'][alphanumeric_word]
                    if alphanumeric_word in model["negative_deceptive"]:
                        prediction['negative_deceptive'] += model['negative_deceptive'][alphanumeric_word]

    max_class = max(prediction, key=prediction.get)
    classified_list = []
    if max_class == "positive_truthful":
        classified_list.append("truthful")
        classified_list.append("positive")
    elif max_class == "positive_deceptive":
        classified_list.append("deceptive")
        classified_list.append("positive")
    elif max_class == "negative_truthful":
        classified_list.append("truthful")
        classified_list.append("negative")
    elif max_class == "negative_deceptive":
        classified_list.append("deceptive")
        classified_list.append("negative")
    return classified_list

path = sys.argv[1]
model_file = glob.glob("nbmodel.txt")
dev_data = glob.glob(path + "/*/*/*/*.txt")
model = {
    "positive_truthful": {},
    "positive_deceptive": {},
    "negative_truthful": {},
    "negative_deceptive": {}
}

with open(model_file[0], 'r') as file:
    for line in file:
        data = line.split()
        className = data[0]
        dataType = data[1]
        value = data[2]
        model[className][dataType] = float(value) 

#classify files
classification = {}
for pathname in dev_data:
    classification[pathname] = classify(pathname, model)

#write to outfile
file = open('nboutput.txt','w')
for pathname, classes in classification.items():
    file.write(classes[0] + " " + classes[1] + " " + pathname + "\n")
    

