CS124 - Machine Translation
=======
A simple direct translation program from Spanish to English.


Introduction
=============
MUST TALK ABOUT 5 PROPERTIES of SPANISH

We decided to use Spanish because all 3 of us have at least some knowledge of the language. Spanish is relatively close to English, which was nice for development. However, there are a fw key differences that caused us a few headaches while developing:

Adjective-Noun ordering: 
There is a reversal in adjective-noun clauses in Spanish compared to English. For example,  "La casa verde" is 'directly' translated to "The house green", while the more fluent translation is "The green house".

Verb conjugation:
They are many more variations on a verb in Spanish than English. If we look at "to run" in the present tense, in English we have: I run, you run, he runs, we run, they run. For all tenses except for the 3rd person singular, we use run. In Spanish, there are 4 different words: corro, corres, corre, corremos, corren. Only the 1st person and 3rd person singular are the same.

Verb tenses:
Spanish has many more tenses than English...

Feminine, Masculine
English does not differentiate masculine and feminine words with the word ending. For example, the word "red" comes up differently depending on what the subject is. "The apple is red" --> "La manzana es roja", "The banana is red" --> "El platano es rojo". Luckily we are going in the "easy" direction, converting from gendered nouns to ungendered nouns.


English can form possesives by adding 's, that doesnt exist in Spanish
In spanish, the possesive is of the form: "The house of John", instead of "John's house". This is translated from "La casa de John".


English Adjectives do not have plural forms



Our Dev Set:
============
1
...
10

Our Test Set:
=============
11
...
15


The Output of our system:
========================





***Processing Strategies***
===========================
Lanuage Model(Unigram, Bigram), Tense Rules, Stemming, 
Post Processing Strategy 1:
....
....
Post Processing Strategy 8:


Error Analysis:
===============
We found these errors




Output of Google Translate:
==========================





Comparative Analysis:
====================


