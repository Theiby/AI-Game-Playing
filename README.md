# Turn-Based Strategy Game with Minimax AI



## 🎮 Overview

This project implements a turn-based strategic board game where an AI (Player 1) competes against a human player (Player 2). The goal is to strategically move and capture opponent pieces on a 7x7 grid. The game ends when a player's pieces are all captured, a move limit is reached, or specific end-game conditions are met.

---

## 📜 Game Rules

The game is played on a **7x7 grid**.

* **Pieces**: Each player controls specific pieces:
    * **AI (Player 1)** controls red triangles (`▲`).
    * **Human (Player 2)** controls blue circles (`●`).

* **Turns**: Each turn, a player can make one or two moves:
    * If a player has **more than one piece**, they must make **two moves**.
    * If a player has only **one piece** left, they make **one move**.

* **Movement**:
    * A piece can move one square **horizontally or vertically**.
    * A move is only valid if the target square is empty.

* **Capturing**:
    * A line of one or more opponent pieces is captured if they are "sandwiched" between two of the current player's pieces or between a player's piece and the board edge.

---

## 🏆 Win Conditions

* **Victory**: A player wins by capturing all of the opponent's pieces.
* **Draw**: The game ends in a draw if:
    * Both players have no pieces remaining.
    * Both players are reduced to one piece each.
* **Move Limit**: If the maximum number of moves (50) is reached:
    * The player with the most remaining pieces wins.
    * If piece counts are equal, the game is a draw.

---

## 🤖 AI and Algorithms

The AI player uses the **Minimax algorithm with Alpha-Beta pruning** to make decisions.

### Minimax Algorithm
The AI simulates all possible moves up to a specific depth (**6** in this implementation) to evaluate their potential outcomes. It selects the move that maximizes its own advantage.

### Alpha-Beta Pruning
This optimization significantly reduces the number of branches the Minimax algorithm explores, making the AI's decision process much faster without sacrificing the quality of the chosen move.

### Heuristic Evaluation Function
The AI evaluates the "goodness" of a board state using a scoring function that considers:
* **Piece Count**: The difference in the number of AI and human pieces.
* **Potential Captures**: The immediate tactical advantage of moves that capture opponent pieces or the risk of losing its own.
* **Sandwich Scenarios**: Rewards for creating board states that threaten to capture multiple opponent pieces.

### Transposition Table
A caching mechanism is implemented to store the evaluations of previously seen board states. This avoids redundant computations and speeds up the AI's thinking process, especially in the mid-game.

### ThreadPoolExecutor
Parallel computation is used to evaluate multiple move combinations simultaneously, which further improves the AI's response time.

---

## 💻 Technical Details

* **Language**: Python
* **Libraries**:
    * `tkinter`: For the graphical user interface (GUI).
    * `concurrent.futures`: For parallel computation in the AI's move evaluation.

---

## 🚀 How to Play

1.  **Run the Game**:
    ```bash
    python game.py
    ```
2.  **AI's First Move**: The game starts with the AI making the first move.
3.  **Your Turn**: The human player takes their turn by clicking on one of their pieces and then clicking on a valid empty square to move it.
4.  **Follow Instructions**: Follow the on-screen status updates to complete your turn. The game alternates turns until a winner is declared or a draw is reached.

---

## 🔮 Future Improvements

* Enhance the AI's heuristic evaluation function for better strategic depth.
* Add adjustable difficulty levels by changing the Minimax search depth.
* Include sound effects or animations for a more engaging user experience.
