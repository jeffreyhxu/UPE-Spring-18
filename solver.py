import requests
import re
import random
access_token = "JLjje"

def main():
    wordlist = []
    with open("words.txt") as wordfile:
        for line in wordfile:
            wordlist.append(line.strip().lower())
    print("wordlist generated")
    r = requests.get("http://upe.42069.fun/" + access_token)
    json = r.json()
    letters_guessed = []
    while True:
        print(json)
        if json['status'] == 'DEAD' or json['status'] == 'FREE':
            break
        state = json['state'].split()
        letters = {}
        matches = 0
        lcount = 0
        for blank in state:
            regstr = '^'
            for char in blank:
                if char.isalpha() or char == '\'':
                    regstr += char
                if char == '_':
                    regstr += '.'
            regex = re.compile(regstr+'(\n)?$', re.I)
            for word in wordlist:
                if re.match(regex, word):
                    matches += 1
                    for i in range(0, len(word)):
                        if regstr[i] == '.':
                            lcount += 1
                            char = word[i]
                            if char in letters:
                                letters[char] = letters[char] + 1
                            else:
                                letters[char] = 1
        # blanks have all been processed
        print(letters)
        most = 0
        common = 'e'
        while common in letters_guessed:
            common = random.choice('abcdefghijklmnopqrstuvwxyz')
        for l in letters:
            if letters[l] > most and l not in letters_guessed:
                most = letters[l]
                common = l
                print("logic")
        print("guessing "+common)
        letters_guessed.append(common)
        respond = requests.post("http://upe.42069.fun/" + access_token,
                                data = {"guess":common})
        json = respond.json()
    
main()
