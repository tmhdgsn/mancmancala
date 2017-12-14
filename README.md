# mancmancala

Methods Implemented:
  * MinMax Variants (python and C++) (several heurstics experimented with)
    * AlphaBeta Pruning
    * MTD
  * Monte Carlo Tree Search (python and C++)
  * Actor Critic Reinforcement Learner (python)
  
 ### MinMax
 The minmax algorithm involves looking forward in time to construct a game tree of possible game states.
 The assumption is that your opponent player will always play optimally. 
 We refer to the games agents respectively as *min* and *max*. 
 

Whilst *min* will always look to minimise their score, *max* will always look to maximise theirs.

With a branching factor of 7, its obvious we cannot construct the whole Mancala game tree, so we set a predefined depth that we wish to look ahead and score each of the leaf nodes we reach.

In order to score a given game state, we implement a **heuristic** function. 

Mancala comprises of few rules, but two in particular that we can look to exploit to maximise our score whilst also attempting to reduce the opponents. Based off these rules we can construct heuristics that incentivise us to pick the board  

*Capture Rule*
> If your move results in the last seed being deposited into an empty hole on the opponents side of the board, then you capture all of the seeds in the oppposite hole, plus your original seed.

*Chain Rule* 
> If the last seed deposited on your move lands in your Mancala, it is your turn again. 

We experimented with multiple heuristics listed below, before finally settling on option 4.
  1. *Difference between Mancalas* (Score)
  2. *Offensive Capture*: incentivise choosing boards with more capture opportunites for yourself.
  3. *Defensive Capture*: incentivise moves that reduce  the number of capture opportunies for your opponent.
  4. *Chaining Potential*: incentivise moves that repeat your turn. 
  5. *Hoarding Stategy*: look to pick boards that maximise the number of seeds in the 2 pits closest to our mancala.
     
Final Heuristic 6: 
Having experimented with a few heuristics we designed a final option as a weighted linear combination of our strategies.
Given a game state X, we define:
x1 := difference between mancalas
x2 := number of capturing opportunities for yourself. 
x3 := opponents capturing opportunities 
x4 := num of potential chaining opportunities.
x5 := total hoard 

Since we wish to maximise all but x3, we will have positive weights to encourage such action and a negative weight to reduce the opponents potential to capture. Having experimented to find the optimal weights for their corresponding feature, we settled on the values below. We arrived at these values through repeated simulations of all variants of the weights in the range (0, 2.0) with increments of 0.1

w1 = 1.5, w2 = 1.2, w3 = -1, w4 = 1, w5 = 1

Once the max depth has been reached we propagate the scores back up the paths taken, updating each game state. We now pick the best move based on this propagated score.
  
  #### MinMax (Alpha Beta Pruning)
The AlphaBeta algorithm is simply a layering over the MinMax that helps to increase the maximum depth we can generate our game tree to. It does this by the use of two parameters Alpha and Beta that keep track of the score limits reachable by nodes we have explored. Upon finding a game state that has a score (in the case of min) less than our Beta bound, we *cut* off the appropriate subtree as we know now not to explore it. This gives us vast improvements in the depth reachable by our algorithm, going from a depth of 7 to 15. With our original implementation in python, we rewrote our AlphaBeta MinMax algorithm in C++ for performance gains. As well as this we incorporated iterative deepening. Rather than predefine a depth for each iteration, we simply set a timer and iterate, going deeper on each iteration until the timer runs out.

This lead to us seeing at some parts of the game tree, our algorithm reaching a depth of 21. 
  
  #### MinMax (MTD)
The MTD algorithm is another layering over our Alpha Beta MinMax algorithm that introduces minimal window search. 
For each state of the game tree AlphaBeta works with a wide search window, where alpha and beta are initialised to -Infinity and +Infinity respectively. In this case, we can be certain of a return value within this bound. 

MTD on the otherhand initialises its search using a *minimal search window*, which simply means making a call to AlphaBeta with beta set to our first guess and alpha equal to beta - 1. A small search window will cause pruning to occur more often but may sacrifice information. The MTD algorithm uses the result of AlphaBeta as an upper/lower bound on the minimax value, if its less than our max bound, we set beta to the result else we update alpha to this value. This new guess is then used as the guess in the next call to mpd. 


### Monte Carlo Tree Search
Unlike MinMax, MCTS does not require prior domain knowledge about the game. 
Evident from the name, its combines the idea of monte carlo simulations with our Mancala game tree.

The attributes for each node in the game state tree are:
  * mancala board
  * player_to_move
  * move_played to reach state
  * no_of_visits
  * score

1. **SELECTION**: 
Given the current state of the game we recursively select the optimum child until we reach a state
we have yet to explore. Our policy for child selection will be described below.

2. **EXPANSION**: *provided we have not reached the end of the game.*
Perform one of the avaiable moves, and select that next state.(child) 

3. **SIMULATION**:
From this next state we perform a simulation, randomly picking moves until the mancala game ends.

4. **BACKPROPAGATION**:
With the result of the end game we now traverse back up our taken path updating each game state 

*Selection Policy:* 
At each stage of child selection, we calculate a UCB value:
  = s_{i} + (C * (ln(N) / n_{i}))
  where: 
    s_{i} := average score for game state
    C := Exploration constant
    N := number of visits to parent. 
    n_{i} := number of visits game state.
    


### Actor Critic Reinforcment Learner
