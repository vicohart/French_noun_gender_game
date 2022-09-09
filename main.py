from random import sample, choices
from datetime import date
from time import time
import chime
import os

from dbase import get_word_collection, insert_attempt_data, save_game, update_finalized, get_level
from constants import *



def get_correct_answer(gender, options):
    if gender == 'm':
        answer = options[0]
    elif gender == 'f':
        answer = options[1]
    elif gender == '':
        answer = options[2]
    
    return answer


def select_articles(word):
    if word[0] in VOWELS or (word[0] == 'h' and word[1] in VOWELS):
        return VOWEL_ARTICLES, VOWEL_KEYS, VOWEL_FREQUENCIES
    else:
        return CONSONANT_ARTICLES, CONSONANT_KEYS, CONSONANT_FREQUENCIES


def get_options(word):
    articles, article_keys, frequencies = select_articles(word)
    article_choice = choices(article_keys, weights=frequencies, k=1)

    return articles[article_choice[0]]['choices']


def challenge_user(word, options):
    print()
    for article in options:
        print(article, end='   ')
    
    print('\n' + word + '\n')


def get_user_input(options):
    user_input = input().lower().strip()
    if user_input == '/':
        user_input = options[2]
    
    return user_input


def game_routine(level):
    today = str(date.today())
    score = 0 
    print('Current level:', level)
    word_collection = get_word_collection(PLAYER_ID, WORD_COLLECTION_SIZE)
    words_for_game = sample(word_collection, k=WORDS_PER_GAME)
    game_start_time = time()

    for (word_id, word, gender) in words_for_game:
        options = get_options(word)
        answer = get_correct_answer(gender, options)
        challenge_user(word, options)
        start_time = time()
        user_input = get_user_input(options)
        end_time = time()
        answer_time = end_time - start_time
        answer_is_correct = user_input == answer
        os.system('cls')

        if answer_is_correct and answer_time < 7:
            chime.success()
            print('\nTrès bien !')
            score += (17 - answer_time) * (1 + int(word_id) // 1000)
                   
        elif answer_is_correct:
            chime.warning()
            print('\nVous avez mis trop de temps !')
            answer_is_correct = False
                            
        else:
            chime.warning()
            print('\nIncorrect !')

        print(answer, word)
        insert_attempt_data(PLAYER_ID, word_id, answer_is_correct, today)
    
    game_end_time = time()
    duration = game_end_time - game_start_time
        
    return int(score), today, int(duration)

chime.theme('big-sur')

while True:
    level = get_level(PLAYER_ID)
    score, day, duration = game_routine(level)
    print('\nFinal score:', str(score))
    save_game(PLAYER_ID, WORDS_PER_GAME, score, day, duration)
    update_finalized(PLAYER_ID, WORDS_PER_GAME, day)

    print('Voulez-vous rejouer ? oui / non')
    preference = input()

    if preference.lower() in ['oui', 'o']:
        continue
    else:
        break

