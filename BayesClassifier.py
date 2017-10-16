
#************************************************************
# MISC
#************************************************************

# This function caculatees the posterior probabilities as for whether
# a given message is spam or not.
# Two tables have per-word likelihoods p(w\c) for spam and non-spam categories.
# We assume the priors are identical (p(c))

#View dictionary
def print_sorted_dict(mydict):
    for key, value in sorted(mydict.iteritems(), key=lambda (k,v): (v,k)):
        print "%s: %s" % (key, value)

#This function creates a list of lines from a text file
def common_words():
    # Imports text file
    import re
    file = open("/Users/Exilink/Downloads/Project/commonWords.txt", 'r')
    # Creates a string with lowercase version of file text
    text = file.read().lower()
    file.close()
    # replaces anything that is not a lowercase letter, a space, or an apostrophe with a space:
    text = re.sub('[^a-z\n]+', "", text)
    words = list(text.split('\n'))
    return words

#************************************************************
# SENTIMENT ANALYSIS
#************************************************************

# Package to use math.log for calculating posterior
import math

#************************************************************
# CREATING LIST FROM FILE
#************************************************************

#This function creates a list of words from a text file
def create_list_of_reviews(path):
    # Imports text file
    import re
    file = open(path, 'r')
    # Creates a string with lowercase version of file text
    text = file.read().lower()
    file.close()
    # replaces unneeded characters such as periods
    text = re.sub('[^a-z\ \'\n]+', " ", text)
    words = list(text.split('\n'))
    words.pop() #Delete last word because it is an empty sentence

    return words

#This function creates a list of reviews from a text file
def create_list_of_words(path):
    # Imports text file
    import re
    file = open(path, 'r')
    # Creates a string with lowercase version of file text
    text = file.read().lower()
    file.close()
    # replaces unneeded characters such as periods
    text = re.sub('[^a-z\ \']+', " ", text)
    words = list(text.split())

    return words

#************************************************************
# CREATING LIKELIHOOD FROM WORDS
#************************************************************

#This function creates the likelihood of each words from the training data
def create_likelihood(words):

    #Creating empty likelihood table
    likelihood = {}
    
    commonWords = common_words()
    
    #Calculating occurences of each word
    for w in words:
        # if the word is not an empty string:
        if len(w) > 3 and w not in commonWords:
            if w in likelihood:
                likelihood[w] += 1
            else:
                likelihood[w] = 1

    #EXTRA CREDIT: BIGRAMe
    #Calculating occurences of each conscutive-word pairs
    for i in range(0, len(words)-1):
        if words[i] not in commonWords or words[i+1] not in commonWords:
            w = words[i] + " " + words[i+1]; #create new word from the current word and next word
        # if either of the word is not an empty string:
            if len(w) > len(words[i]) + 1 or len(w) > len(words[i+1]):
                if w in likelihood:
                    likelihood[w] += 1
                else:
                    likelihood[w] = 1

    #Find total number of words
    count = 0
    for w in likelihood:
        count = count + likelihood[w]

    #Divide each word by number of words to find likelihood probability of each word
    for w in likelihood:
        likelihood[w] = float(likelihood[w]) / count;

    return likelihood

#************************************************************
# CALCULATING POSTERIORS
#************************************************************

#This function calculates the posteriors to judge whether sentence is positive
def is_this_positive(sentences, pos, neg):

    #Split sentence by words
    words = sentences.split(' ')
    
    pos_prob = 0
    neg_prob = 0
    
    #This function calculates the posteriors for positive and negative likelihood
    for w in words:
        if w in pos:
            pos_prob += math.log(pos[w])
        if w not in pos and w in neg:
            pos_prob += math.log(0.000000000000000000001)
        if w in neg:
            neg_prob += math.log(neg[w])
        if w not in neg and w in pos:
            neg_prob += math.log(0.000000000000000000001)

        
        #from random import randint
        #if randint(1,100) == 1:
        #print sentences + ": " + str(pos_prob > neg_prob) + "\n\n"
        
    #return true if postive
    return pos_prob > neg_prob

#This function calculates overall accuracy
def calculate_accuracy(wordList, pos, neg):
    
    #For each review, judge whether it's positive
    count = 0
    for sentences in wordList:
        if is_this_positive(sentences, pos, neg):
            count += 1 #accumulates if its positive

    print str(count) + " out of " + str(len(wordList)) + " reviews were classified as positive sentiments."

    return float(count) / len(wordList)

#************************************************************
# MAIN
#************************************************************

print "\nSENTIMENT ANALYSIS:"

# CREATING LIST OF EACH WORDS IN POS AND NEG TRAINING SET
posWords = create_list_of_words("train-pos.txt")
negWords = create_list_of_words("train-neg.txt")

# CREATING LIKELIHOOD PROBABILITIES FROM WORDS
posLikelihood = create_likelihood(posWords)
negLikelihood = create_likelihood(negWords)

# CREATING LIST OF REVIEWS
posTest = create_list_of_reviews("test-pos.txt")
negTest = create_list_of_reviews("test-neg.txt")

# CALCULATING SENTIMENT ANALYSIS FOR POSITIVE AND NEGATIVE TRAINING SET
posAccuracy = calculate_accuracy(posTest, posLikelihood, negLikelihood)
negAccuracy = 1 - calculate_accuracy(negTest, posLikelihood, negLikelihood)

print "Accuracy for positive reviews: " + str(posAccuracy*100) + "%"
print "Accuracy for negative reviews: " + str(negAccuracy*100) + "%"

print "\n"

#print "############################################################"

#print_sorted_dict(neg)


