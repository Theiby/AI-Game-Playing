Overview
This project implements a turn-based strategic board game where an AI (Player 1) competes against a human player (Player 2). The goal is to strategically move and capture opponent pieces on a 7x7 grid, using simple movement and capturing mechanics. The game ends either when all pieces of a player are captured, the maximum number of moves (50) is reached, or specific end conditions are met.

Game Rules
The game is played on a 7x7 grid.
Each player controls specific pieces:
AI controls red triangles (A).
Human controls blue circles (H).
Each turn, a player can make one or two moves depending on the number of pieces they control:
If a player has more than one piece, they must make two moves.
If a player has one piece left, they make one move.
Movement:
A piece can move horizontally or vertically by one square.
A move is valid only if the target square is empty.
Capturing:
A series of consecutive pieces can be captured if they are "sandwiched" between the opponent's pieces or the board edge.
Win Conditions
A player wins if they eliminate all opponent pieces.
The game ends in a draw if:
Both players have no pieces remaining.
Both players are reduced to one piece each.
If the maximum number of moves (50) is reached:
The player with the most remaining pieces wins.
If both have the same number of pieces, it’s a draw.
AI and Algorithms
The AI player uses the Minimax algorithm with Alpha-Beta pruning to make decisions. Below are the core concepts used:

Minimax Algorithm:

The AI simulates all possible moves up to a specific depth (6 in this implementation) to evaluate their potential outcomes.
It selects the move set that maximizes its advantage (or minimizes disadvantage if it's the opponent's turn).
Alpha-Beta Pruning:

This optimization reduces the number of branches the AI explores, making the decision process faster without sacrificing accuracy.
Heuristic Evaluation Function:

The AI evaluates board states using a scoring function that considers:
Piece count: The difference in the number of AI and human pieces.
Potential captures: Moves that could lead to capturing opponent pieces or losing its own pieces.
Sandwich scenarios: Rewards for putting the opponent in a position where they might lose multiple pieces.
Transposition Table:

A caching mechanism is implemented to store previously evaluated board states, reducing redundant computations.
ThreadPoolExecutor:

Parallel computation is used to evaluate multiple move combinations simultaneously, improving AI response time.
Technical Details
Language: Python
Libraries:
tkinter: For graphical user interface (GUI) implementation.
concurrent.futures: For parallel computation in AI move evaluation.
Game Mechanics:
Board is represented as a 2D list.
Each turn involves:
Validating player moves.
Capturing opponent pieces based on the game's rules.
Checking for game-ending conditions.
How to Play
Run the game:
bash
Kopyala
Düzenle
python game.py
The game will start with the AI making the first move.
The human player takes their turn by clicking on their pieces and selecting valid moves.
Follow on-screen instructions and status updates to complete your turn.
The game alternates turns until a winner is declared or a draw is reached.
Future Improvements
Enhance the AI evaluation function for better strategic depth.
Add additional difficulty levels with adjustable Minimax depth.
Include sound effects or animations for a more engaging user experience.
