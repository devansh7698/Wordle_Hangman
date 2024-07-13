# -*- coding: utf-8 -*-
def hangman(secret_word, guesser, max_mistakes=5, verbose=True, **guesser_args):
    """
        This function plays the hangman game with the provided guesser and returns the number of incorrect guesses.

        secret_word: a string of lower-case alphabetic characters, i.e., the answer to the game
        guesser: a function which guesses the next character at each stage in the game
            The function takes a:
                mask: what is known of the word, as a string with _ denoting an unknown character
                guessed: the set of characters which already been guessed in the game
                guesser_args: additional (optional) keyword arguments, i.e., name=value
        max_mistakes: limit on length of game, in terms of number of allowed mistakes
        verbose: silent or verbose diagnostic prints
        guesser_args: keyword arguments to pass directly to the guesser function
    """
    secret_word = secret_word.lower()
    mask = ['_'] * len(secret_word)
    guessed = set()
    correct=set()
    len_word=len(secret_word)

    if verbose:
        print("Starting hangman game. Target is", ' '.join(mask), 'length', len(secret_word))

    mistakes = 0
    # mis=0
    i=0
    # flag=0
    to_do=1
    print(secret_word)
    while mistakes < max_mistakes:
    #     if flag<1 and len_word<7 and to_do:
    #         flag+=1
    #         if(len_word==3):
    #             letters_1 = ['a','s','e','o']
    #             guess=letters_1[i]
    #             print(guess,secret_word)
    #             i+=1
    #     if flag==1:
    #         to_do=0
    #A E O I U Y H
        arr=['e','a','i','o','u']
        if (len(correct)==0 and False):
            guess=arr[i]
            i+=1
            print("*")
        else :
            to_do=0


        if verbose:
            print("You have", (max_mistakes-mistakes), "attempts remaining.")

        if to_do==0:
            guess = guesser(mask, guessed, **guesser_args)
        #print(guess , secret_word ,mistakes)
        print(guess)
        if verbose:
            print('Guess is', guess)
        if guess in guessed:
            if verbose:
                print('Already guessed this before.')
            mistakes += 1
        else:
            guessed.add(guess)
            if guess in secret_word and len(guess) == 1:
                for i, c in enumerate(secret_word):
                    if c == guess:
                        mask[i] = c
                correct.add(guess)
                if verbose:
                    print('Good guess:', ' '.join(mask))
            else:
                if len(guess) != 1:
                    print('Please guess with only 1 character.')
                if verbose:
                    print('Sorry, try again.')
                mistakes += 1

        if '_' not in mask:
            if verbose:
                print('Congratulations, you won.')
            return 1

    if verbose:
        print('Out of guesses. The word was', secret_word)
    #print(secret_word,guessed)
    print('-'*20)
    return 0

import agentAPI.hangman as game
def hangman_api(guesser, **guesser_args):
  """
  Starts and plays a single hangman game using the guesser.
  Returns (win_lost, word, attempts) where win_lost is True 
  if the game was won, mask is the secret word, and guessed 
  is the set of guesses made.
  """
  mask = game.start()
  guessed = set()
  status = "ongoing"
  while (status == "ongoing"):
    (status, mask, guessed) = game.postTry(guesser(mask, guessed, **guesser_args))
  return ((status == "won"), mask, guessed)

"""## Data Pre-processing
Use NLTK's Brown corpus for training an artificial intelligence guessing algorithm, and for evaluating the quality of the algorithm.

1. compute the number of **unique word types** occurring in the Brown corpus, using `nltk.corpus.brown` and the `words` method, and select only words that are **entirely comprised of alphabetic characters**.

2. **Lowercase the words**.

3. Finally, randomly shuffle (`numpy.random.shuffle`) this collection of word types, and split them into disjoint training and testing sets. Both `training_set` and `test_set` should be a python `list`. Besides, `test_set` should contain 1000 word types.
"""

# from nltk.corpus import words, brown, wordnet
from collections import Counter
import numpy as np
import string
np.random.seed(1)

processed_words = []
'''
#words from brown corpus
words_words = words.words()
brown_words = brown.words()
wordnet_words = wordnet.words()

#lowercase the corpus and remove the word which contain non-alphabetic characters
for word in brown_words:
    if word.isalpha():
        processed_words.append(word.lower())
for word in words_words:
    if word.isalpha():
        processed_words.append(word.lower())
for word in wordnet_words:
    if word.isalpha():
        processed_words.append(word.lower())
'''

file1 = open("word_list_largest.txt")
my_words = []
lines = file1.readlines()
for line in lines:
    my_words.append(line.strip())
file1.close()

file2 = open("word_list_largest.txt")
lines = file2.readlines()
for line in lines:
    processed_words.append(line.strip())
file2.close()

#unique words in brown corpus
#nltk_words = list(set(processed_words))

#print(len(my_words),len(nltk_words))

#my_words = list(set(my_words).intersection(set(nltk_words)))
print(len(my_words))

length_dict = Counter()
for word in my_words:
    length_dict[len(word)] +=1
for i in sorted(length_dict):
    print(i, length_dict[i])

"""**Shuffle Data and create training, test dataset**"""

my_words = np.array(my_words)
np.random.shuffle(my_words)
my_words = my_words.tolist()


my_word = np.array(processed_words)
np.random.shuffle(my_word)
my_word = my_word.tolist()

test_set = my_word[:1000]
training_set = my_words#[:1000]
print("Number of word types in test =", len(test_set))
print("Number of word types in train =", len(training_set))

"""## Test Guesser      
`test_guesser` method that takes a guesser and measures the accuracy over all the words in the `test_set` provided to you.
"""

def test_guesser(guesser, test=test_set):
    total = 0
    for word in test:
        total += hangman(word, guesser, 6, False)
    return total / float(len(test))

def api_test(guesser, games):
    total = 0
    for _ in range(0, games):
        (status, word, letters) = hangman_api(guesser)
        if (status):
            total += 1
            status = "won"
        else:
        	status = "lost"
        print(f"Game {status} - word: {word} - guesses: {''.join(list(letters))}")
    return total/float(games)

"""## 4-Gram Model

1. Pad \$\$\$ to the front of the words and \#\#\# to the back of words
2. Get the unigram, bigram, trigram and 4-gram count from training set
3. Apply 4-gram model to each blank position in the secret word by using its adjacent context characters
4. We need to apply 4-gram, trigram, bigram and unigram based on different situations.
5. Sum up the probability distribution (over all alphabets from a to z) for every blank.
6. Take the max probability of the character
"""

from collections import defaultdict, Counter

def sevengram(corpus):

    ## Initializing the n-gram counter dictionaries
    unigram_counts = defaultdict(Counter)
    #print(unigram_counts)
    bigram_counts_second = defaultdict(Counter)
    bigram_counts_first = defaultdict(Counter)

    trigram_counts_third = defaultdict(Counter)
    trigram_counts_second = defaultdict(Counter)
    trigram_counts_first = defaultdict(Counter)

    fourgram_counts_first = defaultdict(Counter)
    fourgram_counts_second = defaultdict(Counter)
    fourgram_counts_third = defaultdict(Counter)
    fourgram_counts_fourth = defaultdict(Counter)

    fivegram_counts_first = defaultdict(Counter)
    fivegram_counts_second = defaultdict(Counter)
    fivegram_counts_third = defaultdict(Counter)
    fivegram_counts_fourth = defaultdict(Counter)
    fivegram_counts_fifth = defaultdict(Counter)

    sixgram_counts_first = defaultdict(Counter)
    sixgram_counts_second = defaultdict(Counter)
    sixgram_counts_third = defaultdict(Counter)
    sixgram_counts_fourth = defaultdict(Counter)
    sixgram_counts_fifth = defaultdict(Counter)
    sixgram_counts_sixth = defaultdict(Counter)

    sevengram_counts_first = defaultdict(Counter)
    sevengram_counts_second = defaultdict(Counter)
    sevengram_counts_third = defaultdict(Counter)
    sevengram_counts_fourth = defaultdict(Counter)
    sevengram_counts_fifth = defaultdict(Counter)
    sevengram_counts_sixth = defaultdict(Counter)
    sevengram_counts_seventh = defaultdict(Counter)


    # Generate a list of unigram_counts
    for word in corpus:
        length = len(word)
        for char in word:
            #index will be[word's length][character]
            unigram_counts[length][char] += 1

    for key in unigram_counts.keys():
        if not len(unigram_counts[key]) == 26:
            add_char = set(string.ascii_lowercase) - set(list(unigram_counts[key].keys()))

            for char in add_char:
                unigram_counts[key][char] = 0


    for word in corpus:
        word = "$$$$$$" + word + "######"

        # generate a list of bigrams
        bigram_list = zip(word, word[1:])

        # generate a list of trigrams
        trigram_list = zip(word, word[1:], word[2:])

        # generate a list of fourgrams
        fourgram_list = zip(word, word[1:], word[2:], word[3:])

        # generate a list of fivegrams
        fivegram_list = zip(word, word[1:], word[2:], word[3:], word[4:])

        # generate a list of sixgrams
        sixgram_list = zip(word, word[1:], word[2:], word[3:], word[4:], word[5:])

        # generate a list of sevengrams
        sevengram_list = zip(word, word[1:], word[2:], word[3:], word[4:], word[5:], word[6:])

        # iterate over bigrams
        for bigram in bigram_list:
            first, second = bigram
            bigram_counts_second[first][second] += 1
            bigram_counts_first[second][first] += 1
        bigram_counts = [bigram_counts_first, bigram_counts_second]

        # iterate over trigrams
        for trigram in trigram_list:
            first, second, third = trigram
            trigram_counts_third[first+second][third] += 1
            trigram_counts_second[first+third][second] += 1
            trigram_counts_first[second+third][first] += 1
        trigram_counts = [trigram_counts_first, trigram_counts_second, trigram_counts_third]

        # iterate over fourgrams
        for fourgram in fourgram_list:
            first, second, third, fourth = fourgram
            fourgram_counts_fourth[first+second+third][fourth] += 1
            fourgram_counts_third[first+second+fourth][third] += 1
            fourgram_counts_second[first+third+fourth][second] += 1
            fourgram_counts_first[second+third+fourth][first] += 1
        fourgram_counts = [fourgram_counts_first, fourgram_counts_second, fourgram_counts_third, fourgram_counts_fourth]

        # iterate over fivegrams
        for fivegram in fivegram_list:
            first, second, third, fourth, fifth = fivegram
            fivegram_counts_fifth[first+second+third+fourth][fifth] += 1
            fivegram_counts_fourth[first+second+third+fifth][fourth] += 1
            fivegram_counts_third[first+second+fourth+fifth][third] += 1
            fivegram_counts_second[first+third+fourth+fifth][second] += 1
            fivegram_counts_first[second+third+fourth+fifth][first] += 1
        fivegram_counts = [fivegram_counts_first, fivegram_counts_second, fivegram_counts_third, fivegram_counts_fourth, fivegram_counts_fifth]

        # iterate over sixgrams
        for sixgram in sixgram_list:
            first, second, third, fourth, fifth, sixth = sixgram
            sixgram_counts_sixth[first+second+third+fourth+fifth][sixth] += 1
            sixgram_counts_fifth[first+second+third+fourth+sixth][fifth] += 1
            sixgram_counts_fourth[first+second+third+fifth+sixth][fourth] += 1
            sixgram_counts_third[first+second+fourth+fifth+sixth][third] += 1
            sixgram_counts_second[first+third+fourth+fifth+sixth][second] += 1
            sixgram_counts_first[second+third+fourth+fifth+sixth][first] += 1
        sixgram_counts = [sixgram_counts_first, sixgram_counts_second, sixgram_counts_third, sixgram_counts_fourth, sixgram_counts_fifth, sixgram_counts_sixth]

        # iterate over sevengrams
        for sevengram in sevengram_list:
            first, second, third, fourth, fifth, sixth, seventh = sevengram
            sevengram_counts_seventh[first+second+third+fourth+fifth+sixth][seventh] += 1
            sevengram_counts_sixth[first+second+third+fourth+fifth+seventh][sixth] += 1
            sevengram_counts_fifth[first+second+third+fourth+sixth+seventh][fifth] += 1
            sevengram_counts_fourth[first+second+third+fifth+sixth+seventh][fourth] += 1
            sevengram_counts_third[first+second+fourth+fifth+sixth+seventh][third] += 1
            sevengram_counts_second[first+third+fourth+fifth+sixth+seventh][second] += 1
            sevengram_counts_first[second+third+fourth+fifth+sixth+seventh][first] += 1
        sevengram_counts = [sevengram_counts_first, sevengram_counts_second, sevengram_counts_third, sevengram_counts_fourth, sevengram_counts_fifth, sevengram_counts_sixth, sevengram_counts_seventh]

    return unigram_counts, bigram_counts, trigram_counts, fourgram_counts, fivegram_counts, sixgram_counts, sevengram_counts

unigram_counts, bigram_counts, trigram_counts, fourgram_counts, fivegram_counts, sixgram_counts, sevengram_counts = sevengram(training_set)

unigram_counts = unigram_counts
bigram_counts_first, bigram_counts_second = bigram_counts
trigram_counts_first, trigram_counts_second, trigram_counts_third = trigram_counts
fourgram_counts_first, fourgram_counts_second, fourgram_counts_third, fourgram_counts_fourth = fourgram_counts
fivegram_counts_first, fivegram_counts_second, fivegram_counts_third, fivegram_counts_fourth, fivegram_counts_fifth = fivegram_counts
sixgram_counts_first, sixgram_counts_second, sixgram_counts_third, sixgram_counts_fourth, sixgram_counts_fifth, sixgram_counts_sixth = sixgram_counts
sevengram_counts_first, sevengram_counts_second, sevengram_counts_third, sevengram_counts_fourth, sevengram_counts_fifth, sevengram_counts_sixth, sevengram_counts_seventh = sevengram_counts

# Calculate the ngram probability
def ngram_prob(key, char, ngram_counts):
    if float(sum(ngram_counts[key].values()))==0:
        return 0
    return ngram_counts[key][char] / float(sum(ngram_counts[key].values()))

def sevengram_guesser(mask, guessed):
    # available is a list that does not contain the character in guessed
    available = list(set(string.ascii_lowercase) - guessed)

    # The probabilities of available character
    sevengram_probs = []
    n = len(mask)

    # if len(mask) = 1, means that there is only a character. Therefore, need to pad in order to avoid error from
    # traverse mask[index - 6] to mask[index + 6].
    mask = ['$', '$', '$', '$', '$', '$'] + mask + ['#', '#', '#', '#', '#', '#']

    for char in available:
        char_prob = 0
        for index in range(6,n+6):
            prob1, prob2, prob3, prob4, prob5, prob6, prob7 = 0, 0, 0, 0, 0, 0, 0

            # The first case is that the char has not been guessed
            if mask[index] == '_':

                # Case 1
                if not mask[index+1] == '_':
                    if not mask[index+2] == '_':
                        if not mask[index+3] == '_':
                            if not mask[index+4] == '_':
                                if not mask[index+5] == '_':
                                    if not mask[index+6] == '_':
                                        prob1 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4]+mask[index+5]+mask[index+6], char, sevengram_counts_first)
                                    else:
                                        prob1 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4]+mask[index+5], char, sixgram_counts_first)
                                else:
                                    prob1 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4], char, fivegram_counts_first)
                            else:
                                prob1 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3], char, fourgram_counts_first)
                        else:
                            prob1 = ngram_prob(mask[index+1]+mask[index+2], char, trigram_counts_first)
                    else:
                        prob1 = ngram_prob(mask[index+1], char, bigram_counts_first)
                else:
                    prob1 = ngram_prob(n, char, unigram_counts)

                # Case 2
                if not mask[index-1] == '_':
                    if not mask[index+1] == '_':
                        if not mask[index+2] == '_':
                            if not mask[index+3] == '_':
                                if not mask[index+4] == '_':
                                    if not mask[index+5] == '_':
                                        prob2 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4]+mask[index+5], char, sevengram_counts_second)
                                    else:
                                        prob2 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4], char, sixgram_counts_second)
                                else:
                                    prob2 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3], char, fivegram_counts_second)
                            else:
                                prob2 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2], char, fourgram_counts_second)
                        else:
                            prob2 = ngram_prob(mask[index-1]+mask[index+1], char, trigram_counts_second)
                    else:
                        prob2 = ngram_prob(mask[index-1], char, bigram_counts_second)
                else:
                    if not mask[index+1] == '_':
                        if not mask[index+2] == '_':
                            if not mask[index+3] == '_':
                                if not mask[index+4] == '_':
                                    if not mask[index+5] == '_':
                                        prob2 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4]+mask[index+5], char, sixgram_counts_first)
                                    else:
                                        prob2 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4], char, fivegram_counts_first)
                                else:
                                    prob2 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3], char, fourgram_counts_first)
                            else:
                                prob2 = ngram_prob(mask[index+1]+mask[index+2], char, trigram_counts_first)
                        else:
                            prob2 = ngram_prob(mask[index+1], char, bigram_counts_first)
                    else:
                        prob2 = ngram_prob(n, char, unigram_counts)

                # Case 3
                if not mask[index-2] == '_':
                    if not mask[index-1] == '_':
                        if not mask[index+1] == '_':
                            if not mask[index+2] == '_':
                                if not mask[index+3] == '_':
                                    if not mask[index+4] == '_':
                                        prob3 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4], char, sevengram_counts_third)
                                    else:
                                        prob3 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3], char, sixgram_counts_third)
                                else:
                                    prob3 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2], char, fivegram_counts_third)
                            else:
                                prob3 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1], char, fourgram_counts_third)
                        else:
                            prob3 = ngram_prob(mask[index-2]+mask[index-1], char, trigram_counts_third)
                    else:
                        if not mask[index+1] == '_':
                            if not mask[index+2] == '_':
                                if not mask[index+3] == '_':
                                    if not mask[index+4] == '_':
                                        prob3 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4], char, fivegram_counts_first)
                                    else:
                                        prob3 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3], char, fourgram_counts_first)
                                else:
                                    prob3 = ngram_prob(mask[index+1]+mask[index+2], char, trigram_counts_first)
                            else:
                                prob3 = ngram_prob(mask[index+1], char, bigram_counts_first)
                        else:
                            prob3 = ngram_prob(n, char, unigram_counts)
                else:
                    if not mask[index-1] == '_':
                        if not mask[index+1] == '_':
                            if not mask[index+2] == '_':
                                if not mask[index+3] == '_':
                                    if not mask[index+4] == '_':
                                        prob3 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4], char, sixgram_counts_second)
                                    else:
                                        prob3 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3], char, fivegram_counts_second)
                                else:
                                    prob3 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2], char, fourgram_counts_second)
                            else:
                                prob3 = ngram_prob(mask[index-1]+mask[index+1], char, trigram_counts_second)
                        else:
                            prob3 = ngram_prob(mask[index-1], char, bigram_counts_second)
                    else:
                        if not mask[index+1] == '_':
                            if not mask[index+2] == '_':
                                if not mask[index+3] == '_':
                                    if not mask[index+4] == '_':
                                        prob3 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3]+mask[index+4], char, fivegram_counts_first)
                                    else:
                                        prob3 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3], char, fourgram_counts_first)
                                else:
                                    prob3 = ngram_prob(mask[index+1]+mask[index+2], char, trigram_counts_first)
                            else:
                                prob3 = ngram_prob(mask[index+1], char, bigram_counts_first)
                        else:
                            prob3 = ngram_prob(n, char, unigram_counts)

                # Case 4
                if not mask[index-1] == '_':
                    if not mask[index-2] == '_':
                            if not mask[index-3] == '_':
                                if not mask[index+1] == '_':
                                    if not mask[index+2] == '_':
                                        if not mask[index+3] == '_':
                                            prob4 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3], char, sevengram_counts_fourth)
                                        else:
                                            prob4 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2], char, sixgram_counts_fourth)
                                    else:
                                        prob4 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1], char, fivegram_counts_fourth)
                                else:
                                    prob4 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1], char, fourgram_counts_fourth)
                            else:
                                if not mask[index+1] == '_':
                                    if not mask[index+2] == '_':
                                        if not mask[index+3] == '_':
                                            prob4 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3], char, sixgram_counts_third)
                                        else:
                                            prob4 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2], char, fivegram_counts_third)
                                    else:
                                        prob4 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1], char, fourgram_counts_third)
                                else:
                                    prob4 = ngram_prob(mask[index-2]+mask[index-1], char, trigram_counts_third)
                    else:
                        if not mask[index+1] == '_':
                            if not mask[index+2] == '_':
                                if not mask[index+3] == '_':
                                    prob4 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2]+mask[index+3], char, fivegram_counts_second)
                                else:
                                    prob4 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2], char, fourgram_counts_second)
                            else:
                                prob4 = ngram_prob(mask[index-1]+mask[index+1], char, trigram_counts_second)
                        else:
                            prob4 = ngram_prob(mask[index-1], char, bigram_counts_second)
                else:
                    if not mask[index+1] == '_':
                        if not mask[index+2] == '_':
                            if not mask[index+3] == '_':
                                prob4 = ngram_prob(mask[index+1]+mask[index+2]+mask[index+3], char, fourgram_counts_first)
                            else:
                                prob4 = ngram_prob(mask[index+1]+mask[index+2], char, trigram_counts_first)
                        else:
                            prob4 = ngram_prob(mask[index+1], char, bigram_counts_first)
                    else:
                        prob4 = ngram_prob(n, char, unigram_counts)

                # Case 5
                if not mask[index+2] == '_':
                    if not mask[index+1] == '_':
                        if not mask[index-1] == '_':
                            if not mask[index-2] == '_':
                                if not mask[index-3] == '_':
                                    if not mask[index-4] == '_':
                                        prob5 = ngram_prob(mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2], char, sevengram_counts_fifth)
                                    else:
                                        prob5 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2], char, sixgram_counts_fourth)
                                else:
                                    prob5 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1]+mask[index+2], char, fivegram_counts_third)
                            else:
                                prob5 = ngram_prob(mask[index-1]+mask[index+1]+mask[index+2], char, fourgram_counts_second)
                        else:
                            prob5 = ngram_prob(mask[index+1]+mask[index+2], char, trigram_counts_first)
                    else:
                        if not mask[index-1] == '_':
                            if not mask[index-2] == '_':
                                if not mask[index-3] == '_':
                                    if not mask[index-4] == '_':
                                        prob5 = ngram_prob(mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1], char, fivegram_counts_fifth)
                                    else:
                                        prob5 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1], char, fourgram_counts_fourth)
                                else:
                                    prob5 = ngram_prob(mask[index-2]+mask[index-1], char, trigram_counts_third)
                            else:
                                prob5 = ngram_prob(mask[index-1], char, bigram_counts_second)
                        else:
                            prob5 = ngram_prob(n, char, unigram_counts)
                else:
                    if not mask[index+1] == '_':
                        if not mask[index-1] == '_':
                            if not mask[index-2] == '_':
                                if not mask[index-3] == '_':
                                    if not mask[index-4] == '_':
                                        prob5 = ngram_prob(mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1], char, sixgram_counts_fifth)
                                    else:
                                        prob5 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1], char, fivegram_counts_fourth)
                                else:
                                    prob5 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1], char, fourgram_counts_third)
                            else:
                                prob5 = ngram_prob(mask[index-1]+mask[index+1], char, trigram_counts_second)
                        else:
                            prob5 = ngram_prob(mask[index+1], char, bigram_counts_first)
                    else:
                        if not mask[index-1] == '_':
                            if not mask[index-2] == '_':
                                if not mask[index-3] == '_':
                                    if not mask[index-4] == '_':
                                        prob5 = ngram_prob(mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1], char, fivegram_counts_fifth)
                                    else:
                                        prob5 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1], char, fourgram_counts_fourth)
                                else:
                                    prob5 = ngram_prob(mask[index-2]+mask[index-1], char, trigram_counts_third)
                            else:
                                prob5 = ngram_prob(mask[index-1], char, bigram_counts_second)
                        else:
                            prob5 = ngram_prob(n, char, unigram_counts)

                # Case 6
                if not mask[index+1]  == '_':
                    if not mask[index-1] == '_':
                        if not mask[index-2] == '_':
                            if not mask[index-3] == '_':
                                if not mask[index-4] == '_':
                                    if not mask[index-5] == '_':
                                        prob6 = ngram_prob(mask[index-5]+mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1], char, sevengram_counts_sixth)
                                    else:
                                        prob6 = ngram_prob(mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1], char, sixgram_counts_fifth)
                                else:
                                    prob6 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1]+mask[index+1], char, fivegram_counts_fourth)
                            else:
                                prob6 = ngram_prob(mask[index-2]+mask[index-1]+mask[index+1], char, fourgram_counts_third)
                        else:
                            prob6 = ngram_prob(mask[index-1]+mask[index+1], char, trigram_counts_second)
                    else:
                        prob6 = ngram_prob(mask[index+1], char, bigram_counts_first)
                else:
                    if not mask[index-1] == '_':
                        if not mask[index-2] == '_':
                            if not mask[index-3] == '_':
                                if not mask[index-4] == '_':
                                    if not mask[index-5] == '_':
                                        prob6 = ngram_prob(mask[index-5]+mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1], char, sixgram_counts_sixth)
                                    else:
                                        prob6 = ngram_prob(mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1], char, fivegram_counts_fifth)
                                else:
                                    prob6 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1], char, fourgram_counts_fourth)
                            else:
                                prob6 = ngram_prob(mask[index-2]+mask[index-1], char, trigram_counts_third)
                        else:
                            prob6 = ngram_prob(mask[index-1], char, bigram_counts_second)
                    else:
                        prob6 = ngram_prob(n, char, unigram_counts)

                # Case 7
                if not mask[index-1] == '_':
                    if not mask[index-2] == '_':
                        if not mask[index-3] == '_':
                            if not mask[index-4] == '_':
                                if not mask[index-5] == '_':
                                    if not mask[index-6] == '_':
                                        prob7 = ngram_prob(mask[index-6]+mask[index-5]+mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1], char, sevengram_counts_seventh)
                                    else:
                                        prob7 = ngram_prob(mask[index-5]+mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1], char, sixgram_counts_sixth)
                                else:
                                    prob7 = ngram_prob(mask[index-4]+mask[index-3]+mask[index-2]+mask[index-1], char, fivegram_counts_fifth)
                            else:
                                prob7 = ngram_prob(mask[index-3]+mask[index-2]+mask[index-1], char, fourgram_counts_fourth)
                        else:
                            prob7 = ngram_prob(mask[index-2]+mask[index-1], char, trigram_counts_third)
                    else:
                        prob7 = ngram_prob(mask[index-1], char, bigram_counts_second)
                else:
                    prob7 = ngram_prob(n, char, unigram_counts)

                # Choose max prob of fivegram first, second, third, fourth and fifth
                char_prob += max(prob1, prob2, prob3, prob4, prob5, prob6, prob7)

            # The final case is that the character is guessed so we skip this position
            else:
                continue

        sevengram_probs.append(char_prob)

    # Return the character that has the maximum probability
    return available[sevengram_probs.index(max(sevengram_probs))]

# result = test_guesser(sevengram_guesser)
result = api_test(sevengram_guesser, 10)
print("Testing my sevengram guesser using every word in test set")
print("Accuracy: ", result)