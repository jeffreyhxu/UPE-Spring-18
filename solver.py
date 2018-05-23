import requests
import re
import random
access_token = "JLjje"
url = "http://upe.42069.fun/"

wordlist = []
with open("words.txt") as wordfile:
    for line in wordfile:
        wordlist.append(line.strip().lower())
print("wordlist generated")

def game():
    r = requests.get(url + access_token)
    json = r.json()
    letters_guessed = []
    while True:
        print(json)
        if json['status'] == 'DEAD' or json['status'] == 'FREE':
            break
        state = json['state'].split()
        letters = {}
        for blank in state:
            regstr = ''
            for char in blank:
                if char.isalpha() or char == '\'':
                    regstr += char
                if char == '_':
                    regstr += '.'
            regex = re.compile(regstr+'(\n)?$', re.I)
            these_letters = {} # letters that satisfy this blank
            these_count = 0;   # divided into a proportion
            for word in wordlist:
                if re.match(regex, word):
                    for i in range(0, len(word)):
                        if regstr[i] == '.':
                            these_count += 1
                            char = word[i]
                            if char in these_letters:
                                these_letters[char] += 1
                            else:
                                these_letters[char] = 1
            for tl in these_letters: # these divisions are so if a blank has
                if tl in letters:    # few choices, those choices matter more
                    letters[tl] += these_letters[tl] / these_count
                else:
                    letters[tl] = these_letters[tl] / these_count
        # blanks have all been processed
        # print(letters)
        most = 0
        common = 'e'
        while common in letters_guessed:
            common = random.choice('abcdefghijklmnopqrstuvwxyz')
        for l in letters:
            if letters[l] > most and l not in letters_guessed and l.isalpha():
                most = letters[l]
                common = l
        print("guessing "+common)
        letters_guessed.append(common)
        respond = requests.post(url + access_token,
                                data = {"guess":common})
        json = respond.json()
    # if there was a word that wasn't in the wordlist, add it
    for lyric in json['lyrics'].split():
        lyric = lyric.translate(str.maketrans('', '', '-",;?!.()'))
        if lyric not in wordlist:
            wordlist.append(lyric)
            with open("words.txt", 'w') as file:
                file.write(lyric+'\n')
            print("added word: " + lyric)

def reset():
    r = requests.post(url + access_token + "/reset",
                      data = {"email": "jeffreyhxu@gmail.com"})
    print(r.json())

def findwords(blank):
    regstr = ''
    for char in blank:
        if char.isalpha() or char == '\'':
            regstr += char
        if char == '_':
            regstr += '.'
    regex = re.compile(regstr+'(\n)?$', re.I)
    letters = {}
    these_letters = {} # letters that satisfy this blank
    these_count = 0;   # divided into a proportion
    for word in wordlist:
        if re.match(regex, word):
            for i in range(0, len(word)):
                if regstr[i] == '.':
                    these_count += 1
                    char = word[i]
                    if char in these_letters:
                        these_letters[char] += 1
                    else:
                        these_letters[char] = 1
    for tl in these_letters: # these divisions are so if a blank has
        if tl in letters:    # few choices, those choices matter more
            letters[tl] += these_letters[tl] / these_count
        else:
            letters[tl] = these_letters[tl] / these_count
    print(these_letters)
    

while True:
    game()
