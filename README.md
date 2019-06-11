# Overview

I've created a blackjack game. 
There are no requirements for the game to work

## Installation & Setup

There are no requirements.txt, since there are no imports. 
The only thing that need to be run is, Blackjack.py.
In the project folder there are a test_Blackjack.py. This can be ignored.

### The code

Blackjack.py has 3 classes (Card, Hand, Deck) and 3 main functions (play_game, regularPlay, splitPlay).
The classes are used for creating cards, a deck and dealing cards. 
The functions are where gameplay is handled. 

### Usage

You start with a set amount of money to play for, in this case; 100$.

 When promptet an input, you have to type the words / letters, exactly like the game asks you. An examble of input: 
"do you want to hit or stay? (type hit/stay)", you then either type "hit" or "stay". NOT "HIT" or "Hit". Another examble is: "do you want to split? (Y/N)", you then have to type "Y" (for yes) or "N" (for no).

When you have played a game, there will be a score of how many games you won/lost, and a question if the user wants to play again.
should you choose to not replay, the game will end. If you should choose to play the game again, you will be asked to place a bet, and the game will continue as before.
