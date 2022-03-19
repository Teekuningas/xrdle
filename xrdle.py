# -*- coding: utf-8 -*-
""" xrdle-moottori. tällä voi pelata itse tai voi 
sitten vaikkapa rakentaa itselleen ratkaisijan!!
"""

import requests
import random
import re


def evaluate(correct, guessed):
    """ arvioi vastauksen ja antaa palautteen..
    """

    # oletuksensa kaikki väärin
    evaluation = ['', '', '', '', '']

    # merkataan oikeat kirjaimet oikeassa paikassa
    for idx in range(len(guessed)):
        if correct[idx] == guessed[idx]:
            evaluation[idx] = '*'

    # merkataan oikeat kirjaimet väärässä paikassa
    for idx in range(len(guessed)):
        # jos kirjain ei ole oikein mutta kirjain on kuitenkin oikeassa vastauksessa
        if guessed[idx] != correct[idx] and guessed[idx] in correct:

            # tätä kirjainta oikeassa vastauksessa n kappaletta
            n_correct = len(list(filter(lambda x: x == guessed[idx], correct)))

            # jo olemassaolevia merkintöjä tälle kirjaimelle
            # (saavat olla oikeita kirjaimia oikeassa paikassa
            # tai tässä samassa loopissa aiemmin merkattuja oikeita 
            # kirjaimia väärässä paikassa)
            n_previous = 0
            for jidx in range(len(guessed)):
                if jidx == idx:
                    continue
                if guessed[jidx] != guessed[idx]:
                    continue
                if evaluation[jidx] == '*' or evaluation[jidx] == '#':
                    n_previous += 1
             
            # jos merkintöjä ei ole vielä tehty liikaa, 
            # tehdään merkinmerkinmerkinmerkintä nyt
            if n_previous < n_correct:
                evaluation[idx] = '#'
    
    return (guessed, evaluation)


def snowflakes_and_moonshine(words, state):
    """ tietokone arvaa sanan. olettaen että oikea sana on 'kissa', 
    tila tulee muodossa:

        [('varis', ['', '#', '', '#', '#']),
         ('koira', ['*', '', '#', '', '*']),
         ...]

    eli siinä on mukana kaikki edelliset arvaukset ja niiden arviot.

    """

    # taikaa..

    return "kissa"


def human_guess(words, state):
    """ ihmisfunktio. tällä voi itse pelata """
    while True:
        answer = input('Anna arvaus: ')
        
        if answer not in words:
            print("Vastaus ei arvattavien sanojen joukossa")
            continue

        break

    return answer


def print_state(state, n_guesses, n_letters):
    """ tulostaa tilan """

    for idx in range(n_guesses):
        try:
            guessed, evaluation = state[idx]
            elems = []
            for jidx in range(len(guessed)):
                if evaluation[jidx] == '*':
                    elems.append(" |*" + guessed[jidx] + "*| ")
                elif evaluation[jidx] == '#':
                    elems.append(" |#" + guessed[jidx] + "#| ")
                else:
                    elems.append(" | " + guessed[jidx] + " | ")
            print("".join(elems))
        except IndexError:
            print(" |   | "*n_letters)

        print("-------"*n_letters)
    print("")


def all_words(n_letters):
    """ muodostaa sanalistan """

    # lataa kirja
    url = 'https://www.cs.helsinki.fi/u/jtakkune/ohjelmat/wunderdog/alastalon_salissa.txt'
    res = requests.get(url)

    # jaa sanoihin
    words = re.split(r'[\n ]', res.text)

    # poista sanoista erikoismerkkejä
    words = map(lambda x: ''.join(filter(str.isalnum, x)), words)

    # poista tyhjät sanat
    words = filter(bool, words)

    # poista vääränmittaiset sanat
    words = filter(lambda x: (len(x) == n_letters), words)

    # pienennä kirjaimet
    words = map(str.lower, words)

    # poista duplikaatit
    words = list(set(words))

    return words


def game(n_guesses, n_letters, guess_fun, words, correct):
    """
    """

    print("Uusi peli alkaa!")
    print("")
    print("Oikea kirjain oikeassa paikassa on ympäröity tähdillä. "
          "Oikea kirjain väärässä paikassa on ympäröity risuaidoilla. "
          "Väärä kirjain on vailla mitään.")
    print("")

    # state sisältää listan arvauskierroksista (niiden arvaukset ja arviot)
    state = []

    for idx in range(n_guesses):

        # tulostaa tilan
        print_state(state, n_guesses, n_letters)

        # pyytää arvauksen arvausfunktiolta
        guessed = guess_fun(words, state)

        # arvaukselle arvio
        evaluation = evaluate(correct, guessed)

        # päivitetään tila
        state = state + [evaluation]

        # testaa onko arvaus täsmälleen oikea ja lopeta
        # jos niin.
        if all(map(lambda x: x == '*', evaluation[1])):
            break

    # tila vielä lopussa 
    print_state(state, n_guesses, n_letters)

    return state


def main():
    """
    """
    # alkuasetukset
    n_games = 1
    n_letters = 5
    n_guesses = 6
    
    # ihminen vai kone

    guess_fun = human_guess
    # guess_fun = snowflakes_and_moonshine

    words = all_words(n_letters)
    correct = random.choice(words)
    # correct = 'kissa'

    results = []

    # pelataan niin monta peliä kun pyydettiin
    for game_idx in range(n_games):
        result = game(n_guesses, n_letters, guess_fun, words, correct)
        results.append(result)

    n_success = 0
    n_tries = 0

    # ja lasketaan vähän tilastoja..
    for result in results:
        if all(map(lambda x: x == '*', result[-1][1])):
            n_tries += len(result)
            n_success += 1

    print("Kaikista {0} pelistä {1} meni läpi!".format(n_games, n_success))
    print("Keskiarvo yritysten lukumäärälle: {0}".format(float(n_tries)/n_games))


if __name__ == '__main__':
    main()

