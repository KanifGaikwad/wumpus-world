# wumpus-world

## Implement a Wumpus World Agent 
There is an agent who can move in n × n grid
(one step at a time). Cells can have wampus, pit, Gold, or nothing. Smell around the wumpus and breeze around
the pit. The agent will be killed if he enters the wampus cell. The agent can kill a wampus if he shoots an arrow
(provided the wampus is in the adjacent cell faced by the agent). The objective of the agent is to get the Gold (not
to kill wumpus). Following are the rules.
1. Let number of pit be p where p ≥ 0 as per the setting of environment. The agent did not know the value of p.
2. Let number of wumpus be w where w ≥ 0 as per the setting of environment. The agent did not know the
value of w.
3. Let number of arrow be m where m ≥ w as per the setting of environment. The agent can see the value of m.
4. Agent can move in a cell adjacent to its current location (one cell only). Only horizontal and vertical movement
is allowed. No diagonal movement. Any attempt to get down the n×n grid (corner moves) gives him a bump,
and he remains in the same cell.
5. Cost of actions
Attempt to move up, down, left, right -1
Shoot arrow -10
Grab Gold 150
6. Agent is always in cell (1,1) at the beginning. No pit or wumpus in the cell (1,1)
7. Agent dies if it enters a cell of live wumpus (Game over). Dead wumpus disappears. Wampus screams after
being hit by an arrow, and the same can be heard by the agent using the sensor.
8. Agent entering in pit gets stuck. This is again Game over.
9. There is only one gold.
10. Environment is static.
11. Agent can move using GO up/down/left/right
12. Agent can focus arrow by SHOOT up/down/left/right
