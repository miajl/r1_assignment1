from __future__ import print_function

import time
from sr.robot import *

#constants
a_th = 0.5 # angular distance to determine whether to turn towards the object or drive straight
d_th_grab = 0.4 # distance from block to grab
d_th_drop = 0.6 # distance from pile to drop a block
turn_timeout_limit = 25 # how long to turn while looking for tokens if the robot doesn't see any in front of it


R = Robot() 
holding_block = False # whether the robot is holding a block
blocks_in_pile = list(); # List that tracks 

current_block = -1 # Block that the robot is either driving towards or holding onto
mission_complete = False

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token(in_pile, turn_timeout = 0):
    """
    Function to find the closest relevant token

    Parameters:
        in_pile (bool): whether to look for tokens in the pile (true) or not in the pile (false)
        turn_timout (float): time already spent looking for the token

    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist = 100
    tmp_marker = -1
    for token in R.see():
        # only consider relevant blocks
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and (in_pile == (token.info.code in blocks_in_pile)):
            dist = token.dist
            rot_y = token.rot_y
            tmp_marker = token.info.code
    if dist == 100:
        #try turning to find new blocks if there aren't any visible right now
        if turn_timeout < turn_timeout_limit:
            print("TOKEN NOT FOUND looking for " + str(turn_timeout_limit - turn_timeout) + " more seconds")
            turn(5, 0.5)
            return find_token(in_pile, turn_timeout + 0.5)
        
        print("TOKEN NOT FOUND timeout reached")
        return -1, -1, -1
    else:
        return dist, rot_y, tmp_marker

def drive_towards(rot_y):
    """
    Function to drive the direction of a token.

    Parameters:
        rot_y (float): angle between the robot and the token

    Returns:
        none
    """
    # if the robot is facing the token, go forward
    if -a_th <= rot_y <= a_th: 
        drive(10, 0.5)
    # if the robot is not facing the token, turn in the direction of the token
    elif rot_y < -a_th:  
        turn(-2, 0.1)
    elif rot_y > a_th:
        turn(+2, 0.1)
    return

#mark a single block as being in the pile
dist, rot_y, current_block = find_token(False)
blocks_in_pile.append(current_block)


while not mission_complete:
    if not holding_block:
        #find the closest token not in the pile
        dist, rot_y, current_block = find_token(False)
        #if there are no tokens not in the pile, mission is complete
        if dist == -1: 
            mission_complete = True
        else:
            drive_towards(rot_y)
            if dist < d_th_grab:
                print("Grabbed block")
                #only proceed to next step if grab was successful
                holding_block = R.grab()
    else: #holding the block
        #find nearest token in the pile
        dist, rot_y, _ = find_token(True)
        #if the pile cannot be found then exit the mission
        if dist == -1:
            mission_complete = True
        drive_towards(rot_y)
        if dist < d_th_drop:
            R.release()
            #add current block to list of blocks in the pile
            blocks_in_pile.append(current_block)
            #back up so the robot does not hit the pile when it is turning
            drive(-10, 2)
            holding_block = False

print("MISSION COMPLETE: stacked " + str(len(blocks_in_pile)) + " blocks")
    
