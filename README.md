Yet Another Tetris

This is a quick tetris game I made as a challenge to myself to learn Python.

This is heavilly based on freeCodeCamp.org's tutorial, however, I've made a few changes to the scoring and rotation system

The mechanics are heavilly based on the TGM serie
- You have a few frames to "lock" a piece in place, even after a drop
- Clearing a certain ammount of lines will increase the level, and thus the speed of the game
- The scoring formula is as follow
  Score = ((Level + Lines)/4) x Lines x Combo
- TGM randomizer (should prevent the same piece from spawning too many times in a row, but contrary to the Nintendo
style of randomizer, you have no guarantee of seeing a certain piece within 12 draw)

S and D for clockwise/anticlockwise rotation
Up key for sonic drop
Spacebar to hold a piece
