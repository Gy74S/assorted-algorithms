# Assorted Algorithms
A bunch of algorithms that I decided to showcase. If I'm currently working on something at the moment, the most recent commit will be in the dev branch.
<br><br>



<h2>true false practise</h2>
<hr/>
<b>Oct 2019</b></br>
First piece of code I uploaded to github in this previously private repo, held here for SenTimEnTaL vAluE.
<br><br>



<h2>magic_knights_tour</h2>
<hr/>
<b>Aug 2020</b></br>
Generates a path for a knight from any starting point such that it reaches every square on a chess board once, and ensures that if we were to plot the turn that it reached the square on the square of the chess board, the sum of the turns on every row and column of the chess board is equal
<br><br>

*Given a starting point, it uses a recursive backtracking solve involving regular quartes, Warnsdorff's heuristic and quad backtracking to generate a path*
<br><br>



<h2>markov_chain_text</h2>
<hr/>
<b>Sep 2020</b><br>
Reads a text file, and then generates a new piece of text using the same immediate word probabilities of the original text.
<br><br>

*Generates a weighted directed graph (markov chain) from a given text, where each vertex is a word. It points to words that came after it in the text, where the weight is the number of times the word came after it. The text is generated through a series of probablistic state transitions from each vertex.*
<br><br>



<h2>reversi</h2>
<hr/>
<b>Sep 2020</b><br>
A 2 player board game where you aim to have the most squares filled.
<br><br>

*Currently just a greedy solve, with additional predefined weighting for each square of the board. Hoping to implement a minimax algorithm with alpha beta pruning/ further heuristics.*
