from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from pycorenlp import StanfordCoreNLP
import nltk
from nltk.corpus import stopwords
import re, pprint
import numpy as np
from sklearn.metrics import precision_recall_fscore_support
# http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/ -- Dataset pulled from here


class Janitor:

    test_features = []
    
    def __init__(self, readfile, outfile):
        # Reading into the test Data
        f = open(readfile, 'r', encoding='UTF-8')
        for line in f:
            if "flavor" in line:
                # Remove characters
                line = line.replace("www", "").replace("http", "").replace("com", "").replace("htm", "".replace("html", ""))
                line = re.sub("[^a-zA-Z]", " ", line)
                line = line.lower().split()
                # Filtering out stop words
                stopped_line = [word for word in line if word not in stopwords.words("english")]
                stopped_line = " ".join(stopped_line)
                # Adds cleaned sentences back together and into the testing list
                self.test_features.append(stopped_line)
        f.close()
        f = open(outfile, "w")
        for i in self.test_features:
            f.write(i+"\n")
        f.close()


class Classifier:
    test_features = []
    test_labels = []
    train_features = []
    train_labels = []
    cross_valid_features = []
    cross_valid_labels = []
    cross_valid_results = []
    tokens = []
    nouns = {}
    filter_nouns = ["flavor", "mg", "ml", "waxy", "solid", "ramp", "shitty", "certain", "next", "label",
                    "tomorrow", "luck", "fear", "coil", "stop", "start", "similar", "profile", "cig", "names"
                    "horrendous", "get", "cheap", "vape", "problems", "spills", "backasswards", "charge", "steeps",
                    "refreshing", "case", "refreshing", "knowledge", "units", "recipes", "sounds", "coilmaster",
                    "cooking", "fashion", "levels", "chemistry", "good", "influence", "sorry", "date", "website"
                    "team", "diminishes", "toss", "exctraction", "bc", "mm", "afford", "stone", "staff", "fortune",
                    "co", "honey", "backwards", "tartness", "answer", "huhhhh", "recipe", "brain", "socks", "coilmaster",
                    "socks", "cooking", "fashion", "chemistry", "sorry", "help", "words", "experiments", "easy",
                    "stains", "boils", "attention", "kinda", "pledge", "catch", "grades", "bottles", "think", "part",
                    "mls", "holiday", "bottles", "shop", "products", "bomb", "bearing", "essence", "worth",
                    "worth", "wraps", "fuck", "hits", "hobo", "mini", "watch", "smells", "boost", "deals",
                    "depends", "fact", "lung", "def", "color", "harshness", "keeps", "attention", "kinda", "grade",
                    "questions", "part", "io", "exhale", "gargabe", "towl", "phew", "ments", "copper", "disappointing",
                    "tanks", "stay", "stainless", "ymmv", "predator", "towl", "ments", "copper", "dit", "ways", "clouds",
                    "cap", "world", "mind", "version", "let", "pull", "gsl", "let", "check", "zero", "leads",
                    "yesterday", "engine", "yesterday", "idk", "max", "varieties", "produce", "ability", "towl",
                    "heads", "lol", "ments", "copper", "dit", "disappointing", "tanks", "work", "title", "haha",
                    "vapes", "r", "oh", "worse", "background", "vendors", "effect", "paper", "water", "industry",
                    "category", "terms", "testers", "tastes", "need", "fill", "glaze", "friends", "fog", "guy",
                    "mout", "gunker", "swap", "witch", "flow", "blow", "town", "quality", "capacity", "eqjuice",
                    "pm", "builds", "weeks", "quick", "creations", "customs", "hint", "material", "pad", "figure",
                    "raspberry", "mods", "pad", "figure", "times", "looks", "p", "mean", "conditions", "sample",
                    "needs", "lingering", "save", "money", "velocity", "matter", "vapes", "approach", "oh",
                    "background", "vendors", "paper", "dump", "swag", "water", "industry", "oh", "worse", "sweeter",
                    "vendors", "effect", "paper", "swag", "vendor", "taste", "customers", "frame","story", "prefrences",
                    "percentage", "holes", "replica","discussions", "girrrrrl", "vapers", "atomizer", "gotten", "deal",
                    "cloudalchemist", "call", "rule", "description", "bakeries", "steeping", "subtle", "sinking",
                    "shipping", "giggle", "god", "cost", "batteries", "corrections",
                    "munity", "prefrences", "layer", "rule", "shops", "description", "vapers", "gotten", "tenp",
                    "ego", "chances", "edges", "budget", "remendation", "direction", "add", "step", "diner", "baker",
                    "hell", "rinse", "problem", "example", "steel", "business", "trade", "flavoring", "list", "wats", "try"]

    def __init__(self, trainingfile, testfile):
        print("Reading the testing file")
        f = open(testfile, 'r', encoding='UTF-8')
        for line in f:
            self.test_features.append(line)
        f.close()
        print("Reading the training file")
        f = open(trainingfile, 'r', encoding='UTF-8', errors='ignore')
        counter = 0
        for line in f:
            sentiment = line[0]
            line = line.replace("www", "").replace("http", "").replace("com", "").replace("htm", "".replace("html", ""))
            line = re.sub("[^a-zA-Z]", " ", line)
            line = line.lower().split()
            stopped_line = [word for word in line if word not in stopwords.words("english")]
            stopped_line = " ".join(stopped_line)
            if counter < 2000 or counter > 3000:
                self.train_features.append(stopped_line)
                self.train_labels.append(sentiment)
            else:
                self.cross_valid_features.append(stopped_line)
                self.cross_valid_labels.append(sentiment)
            if counter == 4000:
                break
            counter += 1
        f.close()
        print("Managed to read in all the files, ready for training & testing")
        print("Processing Testing Features")

    def bag_of_words(self):

        vect = CountVectorizer(analyzer="word", max_features=7000)
        # Vect Data
        training = vect.fit_transform(self.train_features).toarray()
        crosstesting = vect.transform(self.cross_valid_labels)
        testing = vect.transform(self.test_features).toarray()
        print(len(training))
        print(len(self.train_labels))
        # Forest Cross Validation
        forest = RandomForestClassifier(n_estimators=110)
        forest.fit(training, self.train_labels)
        forest_crossvalidation_results = forest.predict(crosstesting)
        # check % error
        forest_counter = 0
        for i in range(len(forest_crossvalidation_results)):
            if forest_crossvalidation_results[i] == self.cross_valid_labels[i]:
                forest_counter += 1
        print("Forest is expected to be " + str(100*(forest_counter/len(self.cross_valid_labels))))
        fscore = precision_recall_fscore_support(self.cross_valid_labels, forest_crossvalidation_results, average='micro')
        print("Precision: "+str(fscore[0]*100)+" Recall: "+str(fscore[1]*100)+" Fscore: "+str(fscore[2]*100))
        # Label testing
        self.test_labels = forest.predict(testing)

    def word_analysis(self, filter_nouns=True):
        for i in self.test_features:
            s = nltk.word_tokenize(i)
            s = nltk.pos_tag(s)
            for j in s:
                if filter_nouns == True:
                    if (j[1] in "FW NN NNS") and (j[0] not in self.filter_nouns):
                        if j[0] not in self.nouns.keys():
                            self.nouns[j[0]] = 1
                        else:
                            self.nouns[j[0]] = self.nouns[j[0]] + 1
                else:
                    if j[1] in "FW NN NNS":
                        if j[0] not in self.nouns.keys():
                            self.nouns[j[0]] = 1
                        else:
                            self.nouns[j[0]] = self.nouns[j[0]] + 1
            noun_sent = {}
            temp_nouns = self.nouns
            for sentcount in range(len(self.test_features)):
                sentance = self.test_features[sentcount]
                opinion = self.test_labels[sentcount]
                for word in temp_nouns.keys():
                    if opinion == "0":
                        opinion = -1
                    else:
                        opinion = 1
                    if (word in sentance) and (temp_nouns[word] > 0):
                        if word in noun_sent.keys():
                            noun_sent[word] = noun_sent[word] + opinion
                        else:
                            noun_sent[word] = opinion
                        temp_nouns[word] = temp_nouns[word] - 1
            print(noun_sent)



    def check_bag_of_words(self, file_answer):
        f = open(file_answer, 'r', encoding='UTF-8', errors='ignore')
        i = 0
        answers = []
        for line in f:
            if i < 100:
                sline = line.split(",")
                answers.append(sline[0])
                i +=1

        results = 0
        for slice in range(99):
            if answers[slice] == self.test_labels[slice]:
                results += 1
        print("Machine vs Man is: " + str((results/len(answers))*100))







x = Classifier("clean_train_data.csv", "clean_test_data.csv")
x.bag_of_words()
#x.check_bag_of_words("answers.csv")
#x.word_analysis()

