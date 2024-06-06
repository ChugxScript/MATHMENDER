# MATHMENDER
![MAIN_MENU_BG](https://github.com/ChugxScript/MATHMENDER/assets/101156843/4e1f74c4-9d33-4ac9-a437-02bf81354cef)

MathMender is a fun and challenging twist on the classic word game, Scrabble, but with numbers! Instead of creating words, players use numbers to form equations, making it an engaging way to practice and enhance arithmetic skills. The game is designed to be both educational and entertaining for players of all ages.

MathMender uses Ant Conoly Optimization (ACO) Algorithm to find the most optimal solution base on the given equations in the current board state.

_This program serves as a project in subject CS322-M_-_CS321L-M - Artificial Intelligence_

## GAMEPLAY
- The first player starts out by picking 9 tiles - 6 number tiles, 2 operator tiles (addition multiplication subtraction or division) and 1 equal signs.

- Using the chosen tiles, the player makes an equation on the game board. (e.g., 3 + 4 = 7).

- The game board has regular squares as well as power up squares that have **2A, 3A, 2N, and 3N** marked on some squares.
  - **2A** means the **answer** of the equation **gets multiplied by 2**
  - **3A** means the **answer** of the equation **gets multiplied by 3**
  - **2N** means the **points of the tiles** that land on this square **get multiplied by 2**
  - **3N** means the **points of the tiles** that land on this square **get multiplied by 3**

- Note that the equation will be read from **LEFT TO RIGHT** and from **TOP TO BOTTOM** only.

- Once the player build an equation, press ‘**PLAY**’ to check if the equation is valid or not.

- If the equation is valid then its **AI turn** else the game will show an **error message**.

- If the player cannot build an equation, the player can press ‘**PASS**’ to finish the player round.

- There’s a **5 minutes time limit** and when the time run out **the most highest score wins**.

## SCREENSHOTS

![image](https://github.com/ChugxScript/MATHMENDER/assets/101156843/7b089682-3dd7-45e0-ae65-9dca16a8c639)
- Instructions
  - ![image](https://github.com/ChugxScript/MATHMENDER/assets/101156843/26729a98-eb5e-46c9-af90-7424b7cd608f)
- Game board
  - ![image](https://github.com/ChugxScript/MATHMENDER/assets/101156843/a0580ba0-4dca-4c65-89cf-843826b3aad3)
  - ![image](https://github.com/ChugxScript/MATHMENDER/assets/101156843/c3230f81-7637-4cf5-9a28-adbd529c5870)
  - ![image](https://github.com/ChugxScript/MATHMENDER/assets/101156843/b39ad3b0-f090-42bd-b0ca-9eb2f71ec887)
  - ![image](https://github.com/ChugxScript/MATHMENDER/assets/101156843/783613b2-dc1f-4cba-bbde-ed57cc264fb0)
  - ![image](https://github.com/ChugxScript/MATHMENDER/assets/101156843/133abeec-0721-46c2-9e3d-e95be6a7520f)
- WIN
  - ![image](https://github.com/ChugxScript/MATHMENDER/assets/101156843/6faaddc7-b426-4a02-9eb1-7c46e9d29c4c)
- LOSE
  - ![image](https://github.com/ChugxScript/MATHMENDER/assets/101156843/21311447-3ddc-494f-ab7d-d01ab15c20bc)
