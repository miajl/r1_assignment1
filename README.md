Research Track 1 Assignment 1
================================
Mia Jane La Rocca
S6344889
miajl

## Assignment Goal
-----------------------------
The goal of this assignment was to command the robot to put all of the golden markers together. In the test scenario there are only golden markers, but the code will still check that the marker is gold to satisfy the assignment requirement. All code in the main loop of the assignment.py file is original. The drive and turn helper functions were taken from the exercise solutions and the find_token and drive_towards functions were modified from the exercise solutions.

## Algorithm and Flowcharts
-----------------------------
The following algorithm was implemented. The helper functions used to find the markers and drive towards the marker are described in the Helper Functions section. The blocks that are in the pile are tracked using a list of their ids.

[flowchart]

## Helper Functions
-----------------------------
The drive and turn helper functions were taken from the exercise examples. These functions take a speed and a duration and command the robot to turn or drive at that speed for the given duration.  The find_token function is modified from the exercise example. The drive_towards function was modified from the exercise example. This function is used to incrementally drive the robot towards its target. If the robot is outside of the angle threshold from the target, the robot turns towards the target. If the robot is within the angle threshold of the target, if drives towards the target. The find_token function has two arguments. The first argument is required and specifies whether to look for tokens that are already in the pile (true) or not in the pile yet (false). The second argument is optional and is used to measure how long the robot has been searching for tokens. The find_token function loops through all of the tokens found in R.see to find the closest golden marker either in or not in the stack depending on the arguments. If find_token does not initially see any tokens that satisfy the stack condition, the function will command the robot to turn and check again. This continues until the timeout is reached. See pseudocode below.  All of the helper functions have doc comments which explain the types of the arguments and the return values.

```
find_token(in_pile, turn_timeout = 0):
    dist = 100
    closest_marker_id = -1
    for token in R.see():
        if (token distance < dist) and (token is gold) and ((token is in pile and in_pile) or (token is not in pile and not(in_pile))):
            dist = token.dist
            rot_y = token.rot_y
            closest_marker_id = token id
    if dist == 100:
        if turn_timeout < turn_timeout_limit:
            turn counter-clockwise for .5 seconds
            return find_token(in_pile, turn_timeout + 0.5)
        return -1, -1, -1
    else:
        return dist, rot_y, closest_marker_id
```

## Run Instructions and Results
-----------------------------
This assignment was completed using python 3. If you do not have it installed, you can use a virtual environment. Change directory to robot-sim. Then run the program with:
```bash
$ python run.py assignment.py
```
When the program is complete "MISSION COMPLETE" is written to the console along with the total number of blocks put together. 
This assignment was completed and tested with python 3.10.12. Here is one of the test results
[TODO test image]

## Possible Improvements
-----------------------------
The biggest weakness in this assignment was that it relies on the marker ids of the blocks. In a real environment it may not be possible to differentiate one marker from another. In this assignment the tradeoff was either having absolute localization or knowing the marker ID, but in the future it may be possible for the robot to keep track of where the markers are as it moves or be able to scan for a location where there are multiple markers together and identify it as the stack rather than having to track the marker ids. 

Another weakness was that the way the robot searches for new markers is inefficient currently it always turns in the counter-clocwise direction. If the robot kept an estimation of the other marker positions, it could better guess whether to turn left to start looking or turn right to start looking for new markers.

Another improvement would be implementing a better control algorithm for the driving. This would make the robot's trajectory to the marker smoother, rather than having the robot stop in place every time the angle error gets too high.