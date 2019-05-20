Yet Another Tetris

This is a quick tetris game I made as a challenge to myself to learn Python.

This is based on freeCodeCamp.org's tutorial, however, I've made a few changes to the scoring, physics and rotation system
I've also corrected his clearing line method

The mechanics are heavilly based on the TGM serie
- You have a few frames to "lock" a piece in place, even after a drop
- Wallkick are possible, T spinning should work as well
- Clearing a certain ammount of lines will increase the level, and thus the speed of the game
- The scoring formula is as follow
  Score = ((Level + Lines)/4) x Lines x Combo
- I went witht the nintendo style randomizer instead of the TGM one

S and D for clockwise/anticlockwise rotation
Up arrow for sonic drop
Down arrow to lock piece
Spacebar to hold a piece
