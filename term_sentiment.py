# Kayla Hoffman
# COSI 143B, Fall 2021
# Programming Assignment #1
#
# Description: This file is for Question 3: Derive the sentiment of new terms

import sys
import re

def create_sent_dict(sentiment_file):
    """A function that creates a dictionary which contains terms as keys and their sentiment score as value

        Args:
            sentiment_file (string): The name of a tab-separated file that contains
                                     all terms and scores (e.g., the AFINN file).

        Returns:
            dicitonary: A dictionary with schema d[term] = score
        """
    afinnfile_name = 'AFINN-111.txt' # to read strings from the command line you can use instead open(sys.argv[1])
    afinnfile = open(afinnfile_name, 'r')
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score = line.split("\t") # The file is tab-delimited and "\t" means tab character
        scores[term] = int(score) # Convert the score to an integer. It was parsed as a string.
    afinnfile.close()
    return scores

def get_tweet_sentiment(tweet, sent_scores):
    """A function that find the sentiment of a tweet and outputs a sentiment score.

            Args:
                tweet (string): A clean tweet
                sent_scores (dictionary): The dictionary output by the method create_sent_dict

            Returns:
                score (numeric): The sentiment score of the tweet

        """
    score = 0
    tweet = re.sub(r'\n', '', tweet)
    words = tweet.split(" ")
    #traverses each word in the tweet to find its score
    for i in range(len(words)):
        #if we know the value for the word from the dictionary
        if words[i] in sent_scores:
            score += sent_scores.get(words[i])
    return score

def term_sentiment(sent_scores, tweets_file):
    """A function that creates a dictionary which contains terms as keys and their sentiment score as value

            Args:
                sent_scores (dictionary): A dictionary with terms and their scores (the output of create_sent_dict)
                tweets_file (string): The name of a txt file that contain the clean tweets
            Returns:
                dicitonary: A dictionary with schema d[new_term] = score
            """
    new_term_sent = {}
    #read from the file of cleaned tweets
    fileObj = open(tweets_file, "r") #opens the file in read mode
    tweetArray = fileObj.read().splitlines() #puts the file into an array of tweets
    fileObj.close()
    #for each line of tweets, designate a sentiment to each new term
    for i in range(len(tweetArray)):
        #line is a single tweet from the array of tweets
        line = tweetArray[i].strip('\n')
        term = line.split(" ") # The file is tab-delimited and "\s" means space character
        #for a word in the tweet
        for j in range(len(term)):
            #if word does not already have sentiment in dictionary
            if term[j] not in sent_scores:
                #the total score of tweets that contain this word
                wScore = 0
                #the number of times the word appears
                wNum = 0
                #compare word from tweet with all its occurences
                for comp in range(len(tweetArray)):
                    if term[j] in tweetArray[comp]:
                        #sum all of the sentiments of tweets containing this word
                       wScore += get_tweet_sentiment(tweetArray[comp], sent_scores)
                       wNum += 1
                #compute average of this word's occurences
                wScore = float(wScore/wNum)
                #add term and sentiment to the new dictionary
                new_term_sent[term[j]] = wScore
    return new_term_sent

def main():
    sentiment_file = sys.argv[1]
    tweets_file = sys.argv[2]

    # Read the AFINN-111 data into a dictionary
    sent_scores = create_sent_dict(sentiment_file)

    # Derive the sentiment of new terms
    new_term_sent = term_sentiment(sent_scores, tweets_file)

    for term in new_term_sent:
        print(term, new_term_sent[term])


if __name__ == '__main__':
    main()