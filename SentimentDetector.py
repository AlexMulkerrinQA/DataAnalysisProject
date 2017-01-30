#! /usr/bin/env python

# Old code from Natural Language Programming project, won't run without example text files.

import re, random, math, collections, itertools, os
def readFiles(EmoSentences,sentencesTrain,sentencesTest,emotions,totalEmo):
    filenames = os.listdir("emotions")

	#BUGFIX
    #there is a copyright notice called 'readme.txt' in folder, don't parse!
    if 'readme.txt' in filenames:
        filenames.remove('readme.txt')
    
    for filename in filenames:

        match = re.search('.*(?=[.].*$)',filename)
        if match:
            emotions.append(match.group(0))
        else:
            emotions.append(filename)

        text = open('emotions/'+filename,'r')
        EmoSentences[emotions[-1]] = re.split(r'\n', text.read())

    totalAll=0
    for emotion in emotions:
        totalEmo[emotion]=0
        for i in EmoSentences[emotion]:
            totalEmo[emotion]+=1
            totalAll+=1
    for emotion in emotions:
        totalEmo[emotion]= totalEmo[emotion] / float(totalAll)

    for emotion in emotions:
        for i in EmoSentences[emotion]:
            if random.randint(1,10)<2:
                sentencesTest[i]=emotion
            else:
                sentencesTrain[i]=emotion  
def trainBayes(sentencesTrain, emotions, pWordEmo, pWordNotEmo, pWord):
#calculates p(W|emotion), p(W|NOTemotion) and p(W) for all words in training data
    freqEmo = {}
    freqNotEmo = {}
    EmoWordsTot = {}
    NotEmoWordsTot = {}
    EmoBigramTot = {}
    NotEmoBigramTot = {}
    EmoTrigramTot = {}
    NotEmoTrigramTot = {}
    for emotion in emotions:
        freqEmo[emotion] = {}
        freqNotEmo[emotion] = {}
        EmoWordsTot[emotion] = 0
        NotEmoWordsTot[emotion] = 0
        EmoBigramTot[emotion] = 0
        NotEmoBigramTot[emotion] = 0
        EmoTrigramTot[emotion] = 0
        NotEmoTrigramTot[emotion] = 0
    dictionary = {}
    dictBigram = {}
    dictTrigram = {}
    allWordsTot = 0
    allBigramTot = 0
    allTrigramTot = 0

    #iterate through each sentence/sentiment pair in the training data
    for sentence, sentiment in sentencesTrain.items():
        wordList = re.findall(r"[\w']+", sentence) #get word list
        # form lists of N-grams
        last='<s>'
        secondLast='<s>'
        bigramList=[] #initialise bigramList
        trigramList=[] #initialise trigramList
        for word in wordList:
            bigram=last+'_'+word
            bigramList.append(bigram)
            trigram=secondLast+"_"+last+'_'+word
            trigramList.append(trigram)
            secondLast = last        
            last = word 
        #add unigrams to dictionary and count frequencies
        for word in wordList:
            allWordsTot += 1 #keep count of total words in dataset
            if not (word in dictionary):
                dictionary[word] = 1
            for emotion in emotions:
                if sentiment == emotion:
                    EmoWordsTot[emotion] += 1 # keep count of total words in emotion class
                    if not (word in freqEmo[emotion]):
                        freqEmo[emotion][word] = 1
                    else:
                        freqEmo[emotion][word] += 1
                else:
                    NotEmoWordsTot[emotion] += 1 #keeps count of words not of this emotion
                    if not (word in freqNotEmo[emotion]):
                        freqNotEmo[emotion][word] = 1
                    else:
                        freqNotEmo[emotion][word] += 1
                        
        #...add bigrams to dictionary and count frequencies                
        for bigram in bigramList:
            allBigramTot += 1 #keep count of total words in dataset
            if not (bigram in dictBigram):
                dictBigram[bigram] = 1
            for emotion in emotions:
                if sentiment == emotion:
                    EmoBigramTot[emotion] += 1 # keep count of total bigrams in emotion class
                    if not (bigram in freqEmo[emotion]):
                        freqEmo[emotion][bigram] = 1
                    else:
                        freqEmo[emotion][bigram] += 1
                else:
                    NotEmoBigramTot[emotion] += 1 #keeps count of bigrams not of this emotion
                    if not (bigram in freqNotEmo[emotion]):
                        freqNotEmo[emotion][bigram] = 1
                    else:
                        freqNotEmo[emotion][bigram] += 1
                        
        #and again...add trigrams to dictionary and count frequencies
        for trigram in trigramList:
            allTrigramTot += 1 #keep count of total words in dataset
            if not (trigram in dictTrigram):
                dictTrigram[trigram] = 1
            for emotion in emotions:
                if sentiment == emotion:
                    EmoTrigramTot[emotion] += 1 # keep count of total trigrams in emotion class
                    if not (trigram in freqEmo[emotion]):
                        freqEmo[emotion][trigram] = 1
                    else:
                        freqEmo[emotion][trigram] += 1
                else:
                    NotEmoTrigramTot[emotion] += 1 #keeps count of trigrams not of this emotion
                    if not (trigram in freqNotEmo[emotion]):
                        freqNotEmo[emotion][trigram] = 1
                    else:
                        freqNotEmo[emotion][trigram] += 1
                    
    for word in dictionary:
        for emotion in emotions:
            if not (word in freqNotEmo[emotion]):
                freqNotEmo[emotion][word] = 0
            if not (word in freqEmo[emotion]):
                freqEmo[emotion][word] = 0
            #calculate probability(word|emotion)
            pWordEmo[emotion][word] = (freqEmo[emotion][word]+0.01) /float(EmoWordsTot[emotion])
            #calculate probability(word|not emotion)
            pWordNotEmo[emotion][word] = (freqNotEmo[emotion][word]+0.01) / float(NotEmoWordsTot[emotion])
        # calculate probability(word)
        appearance=0
        for emotion in emotions:
            appearance+=freqEmo[emotion][word] + freqNotEmo[emotion][word]
        pWord[word] = appearance / float(allWordsTot)


    for bigram in dictBigram:
        for emotion in emotions:
            if not (bigram in freqNotEmo[emotion]):
                freqNotEmo[emotion][bigram] = 0
            if not (bigram in freqEmo[emotion]):
                freqEmo[emotion][bigram] = 0
            #calculate probability(bigram|emotion)
            pWordEmo[emotion][bigram] = (freqEmo[emotion][bigram]+0.01) /float(EmoBigramTot[emotion])
            #calculate probability(bigram|not emotion)
            pWordNotEmo[emotion][bigram] = (freqNotEmo[emotion][bigram]+0.01) / float(NotEmoBigramTot[emotion])
        # calculate probability(bigram)
        appearance=0
        for emotion in emotions:
            appearance+=freqEmo[emotion][bigram] + freqNotEmo[emotion][bigram]
        pWord[bigram] = appearance / float(allBigramTot)

    for trigram in dictTrigram:
        for emotion in emotions:
            if not (trigram in freqNotEmo[emotion]):
                freqNotEmo[emotion][trigram] = 0
            if not (trigram in freqEmo[emotion]):
                freqEmo[emotion][trigram] = 0
            #calculate probability(trigram|emotion)
            pWordEmo[emotion][trigram] = (freqEmo[emotion][trigram]+0.01) /float(EmoTrigramTot[emotion])
            #calculate probability(trigram|not emotion)
            pWordNotEmo[emotion][trigram] = (freqNotEmo[emotion][trigram]+0.01) / float(NotEmoTrigramTot[emotion])
        # calculate probability(trigram)
        appearance=0
        for emotion in emotions:
            appearance+=freqEmo[emotion][trigram] + freqNotEmo[emotion][trigram]
        pWord[trigram] = appearance / float(allTrigramTot)
def testBayes(sentencesTest, dataName, emotions, pWordPos,pWordNeg, pWord, pEmotion):
#implement naive bayes algorithm
#INPUTS:
#  sentencesTest is a dictonary with sentences associated with sentiment 
#  dataName is a string (used only for printing output)
#  pWordPos is dictionary storing p(word|positive) for each word
#  pWordNeg is dictionary storing p(word|negative) for each word
#  pWord is dictionary storing p(word)
#  pPos is a real number containing the fraction of positive reviews in the dataset
    total=0
    correct=0
    totalEmo={}
    correctEmo={}
    #find most likely emotion class (fallback prediction)
    mostLikelyEmo=False
    for emotion in emotions:
        if not mostLikelyEmo:
            mostLikelyEmo=emotion
        else:
            if pEmotion[emotion]>pEmotion[mostLikelyEmo]:
                mostLikelyEmo=emotion

    # confusion matrix to check miss-classification
    confusionMatrix={}
    for emotion in emotions:
        totalEmo[emotion] = 0
        correctEmo[emotion] = 0
        confusionMatrix[emotion]={} #using dicts in dicts as multi dimensioned arrays..D:
        for emo in emotions:
            confusionMatrix[emotion][emo]=0;   

    for sentence, sentiment in sentencesTest.items():
        Words = re.findall(r"[\w']+", sentence)
        
        bestScore=0
        predictedEmotion=mostLikelyEmo #fallback prediction if ALL emotions return 0% prob is most frequent in corpus
        for emotion in emotions:
            score = emotionProbability(emotion,Words,pWordPos,pWordNeg,pWord, pEmotion[emotion])
            if (score>bestScore):
                bestScore=score
                predictedEmotion=emotion
                
        confusionMatrix[sentiment][predictedEmotion]+=1
        total+=1
        totalEmo[sentiment]+=1
        if sentiment == predictedEmotion:
            correct+=1
            correctEmo[predictedEmotion]+=1

    acc= math.floor(correct/float(total) * 100) / 100 #floor value so no rounding up to 100% !
    print(dataName + " Accuracy (All)\t\t= %0.2f" % acc +"%% (%d" % correct +"/%d" % total +")")
    for emotion in emotions:
        accpos= math.floor(correctEmo[emotion]/float(totalEmo[emotion]) * 100) / 100
        print (dataName + " Accuracy ("+emotion +") \t= %0.2f" % accpos + "%% (%d" % correctEmo[emotion] + "/%d" % totalEmo[emotion] + ")")
    print('')
    string='prediction ->\t'
    for emotion in emotions:
        string+=emotion+' '
    print (string)
    print ('actual -v')
    for emotion in emotions:
        string=emotion[:6]+':\t\t'
        for emo in emotions:
            string+=str(confusionMatrix[emotion][emo])+'\t'
        print(string)
    print('')
def emotionProbability(emotion,Words,pWordPos,pWordNeg,pWord,pPos):
    scorePos = pPos
    scoreNeg = 1-pPos

    last='<s>'
    secondLast='<s>'
    segment=False #N-gram to use probability of
    for word in Words:
        segment=False #N-gram to use probability of
        #check trigrams then backoff to bigrams then unigrams
        trigram=secondLast+"_"+last+'_'+word
        if (trigram in pWord):
            segment=trigram      
        #no trigram? check bigram
        if not(segment):
            bigram=last+'_'+word
            if (bigram in pWord):
                segment=bigram
            #no bigram? just use unigram
       # if not(segment):
        if (word in pWord):
            segment=word

        secondLast = last        
        last = word
        #was a valid N-gram found?
        if segment:
            if (segment in pWordPos[emotion]): 
                scorePos *= pWordPos[emotion][segment]
            else:
                scorePos *= pPos
            if (segment in pWordNeg[emotion]):
                scoreNeg *= pWordNeg[emotion][segment]
            else:
                scoreNeg *= 1-pPos
        else: # no N-gram? assume distribution of emotion probabilities for unknown words are like corpus
            scorePos *= pPos
            scoreNeg *= 1-pPos
    if (scorePos+scoreNeg>0): #can't divide by zero! (this situation implies both pPos and pNeg are zero)       
        return scorePos / float(scorePos+scoreNeg)
    else:
        return 0
def detectSentiment(sentence, emotions,  pWordPos, pWordNeg, pWord, pEmotion):
#----------------- single sentence appraisal ---------------------
    Words = re.findall(r"[\w']+", sentence)    
    bestScore=0
    predictedEmotion='well, not sure... Good job outsmarting me! :P' #fallback prediction if ALL emotions return 0% prob is most frequent in corpus
    for emotion in emotions:
        score = emotionProbability(emotion,Words,pWordPos,pWordNeg,pWord, pEmotion[emotion])
        if (score>bestScore):
            bestScore=score
            predictedEmotion=emotion
                
    print('I think you are: '+str(predictedEmotion))
def mostUseful(emotions,pWord,pWordPos,pWordNeg,n,predictFeatures):
#-------------------------find most useful predictors ----------------------
    predictPower={}
    for emotion in emotions:
        predictPower[emotion]={}
        for word in pWord:
            if not ('_' in word): # only use unigrams for predictors, others are too rare!
                if pWordNeg[emotion][word]<0.0000001:
                    predictPower[emotion][word]=1000000000
                else:
                    predictPower[emotion][word]=pWordPos[emotion][word] / pWordNeg[emotion][word]
            else:
                predictPower[emotion][word]=0
        sortedPower = sorted(predictPower[emotion], key = predictPower[emotion].get)
        head, tail = sortedPower[:n], sortedPower[len(predictPower[emotion])-n:]
        #print (str(emotion)+":")
        #print(tail)
		#print('\nNot '+str(emotion)+':')
        #print(head)
        #print('\n')
        predictFeatures[emotion]=tail
def tagSentencesByFeature(sentences,features,emotions,presence):
#----------------------------check for existence of predictors ---------------
    i=0
    for emo in emotions:
        for sentence in sentences[emo]:
            Words = re.findall(r"[\w']+", sentence)
           # print(Words)
            presence[i]=[]
            for emotion in emotions: #yes I know silly to iterate twice....
                for feature in features[emotion]:
                    if feature in Words:
                        presence[i].append('yes')
                    else:
                        presence[i].append('no')
            presence[i].append(emo) #needed in output data
            i+=1
def writeArffFile(emotions,features,presence):
    f =open('emotion.arff','w')
    f.write('@relation emotion\n\n')
    for emo in emotions:
        for i in features[emo]:
            string='@attribute "'+str(i)+':'+str(emo)+'" {yes,no}\n' #attributes named <word>:<associated emotion>
            f.write(string)
    string='\n@attribute emotion {' #class of each sentence
    first=True
    for i in emotions:
        if first:
            string+=str(i)
            first=False
        else:
            string+=','+str(i)
    string+='}\n'
    f.write(string)
    f.write('\n@data\n')
    #create dataset of existence of keywords
    for i in presence:
        string=''
        first=True
        for val in presence[i]: #already in 'yes'/'no' form
            if first:
                string+=val
                first=False
            else:
                string+=', '+val #only add commas before values AFTER the first
        f.write(string+'\n')
    f.close() 
#---------- Main Script --------------------------
allSentences={}
sentencesTrain={}
sentencesTest={}
emotions=[]
pEmotion={}
# get data from files
readFiles(allSentences,sentencesTrain,sentencesTest,emotions,pEmotion)
#create datasets for probabilities indexed by emotion class
pWordEmotion={} # p(W|Positive)
pWordNotEmotion={} # p(W|Negative)
pWord={}    # p(W)
predictFeatures={} # list of most useful features for predicting each emotion
for emotion in emotions:
    pWordEmotion[emotion]={}
    pWordNotEmotion[emotion]={}
    predictFeatures[emotion]={}
#build conditional probabilities using training data
trainBayes(sentencesTrain, emotions, pWordEmotion, pWordNotEmotion, pWord)
#run naive bayes classifier on datasets
print ("Naive Bayes")
testBayes(sentencesTrain,  "(Train Data)\t", emotions, pWordEmotion, pWordNotEmotion, pWord, pEmotion)
testBayes(sentencesTest,  "(Test Data)\t",  emotions, pWordEmotion, pWordNotEmotion, pWord, pEmotion)

# find most useful tags and create arff file
presentFeatures={} # array of features present in each sentence in corpus
mostUseful(emotions,pWord,pWordEmotion,pWordNotEmotion,20,predictFeatures)
#create string of attribute presence for each sentence
tagSentencesByFeature(allSentences,predictFeatures,emotions,presentFeatures)
# output to emotion.arff
writeArffFile(emotions,predictFeatures,presentFeatures)
# ---------- END -------(bonus!)
sentence = input("Got anything to say?\n")
detectSentiment(sentence, emotions, pWordEmotion, pWordNotEmotion, pWord, pEmotion);