#!/usr/bin/env python3

# generates sentences of the form "I was born A but now I am B", where A is an adjective, B is a noun, and A and B rhyme
# get the `mobypos.txt` and `mobypron.txt` files from the MOBY English language project
# `mobypron.txt` is a copy of `mobyron.unc` in the original project, but re-encoded to UTF-8

# inspired by [this picture](https://i.imgur.com/s1QT6AY.jpg)

nouns, adjectives = [], []
with open("mobypos.txt", "r") as f:
    for line in f:
        word, parts_of_speech = line.split("\\")
        if "A" in parts_of_speech: adjectives.append(word)
        if "N" in parts_of_speech: nouns.append(word)

last_syllable_words, word_last_syllables = {}, {}
with open("mobypron.txt", "r") as f:
    for line in f:
        word, pronounciation = line.split(" ", 1)
        syllables, index = [[]], 0
        for phoneme in pronounciation.strip("/\n").split("/"):
            if phoneme in {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U", "aI", "eI", "Oi", "oU", "AU", "@", "(@)", "[@]", "&"}: # vowel sounds
                index += 1
                syllables.append([phoneme])
            elif phoneme != "": # consonant sound
                syllables[index].append(phoneme)
        if len(syllables[-1]) == 0: del syllables[-1] # delete last blank syllable
        if len(syllables) > 1: last_syllable = (tuple(syllables[-2]), tuple(syllables[-1]))
        else: last_syllable = tuple(syllables[-1])
        if last_syllable not in last_syllable_words: last_syllable_words[last_syllable] = []
        last_syllable_words[last_syllable].append(word)
        word_last_syllables[word] = last_syllable

def get_rhyming_pair(first, second):
    import random
    while True:
        first_word = random.choice(first)
        if first_word not in word_last_syllables: continue # word is in part of speech dictionary, but not the pronounciation dictionary
        rhyming_words = last_syllable_words[word_last_syllables[first_word]]
        for word in rhyming_words:
            if word in second:
                return first_word, word

for i in range(1000): print("I was born {} but now I am {}".format(*get_rhyming_pair(adjectives, nouns)))
