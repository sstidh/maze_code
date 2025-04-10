## MAGNET DETECTION
#magnet checking function
def magnet_detect():
    mag = 0
    force = abs(input.magnetic_force(Dimension.X))
    if force >= 500:
        mag = 1
         # turn headlights green
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
        return mag

## LINE FOLLOWING
#set variables
lwheel = 20
rwheel = 20
error = 0
maxturnspeed = 50

#magnet present
mag = 0

# set starting speed
CutebotPro.pwm_cruise_control(lwheel, rwheel)
basic.pause(50)
 
#turns for line following
def turn_r():
    global lwheel, rwheel, maxturnspeed
    lwheel = lwheel + (abs(error)/3000)*maxturnspeed
    rwheel = rwheel - (abs(error)/3000)*maxturnspeed
     # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
     #delay 0.05 sec
     #delay 0.01 sec
    basic.pause(10)
def turn_l():
    global lwheel, rwheel, maxturnspeed
    lwheel = lwheel - (abs(error)/3000)*maxturnspeed
    rwheel = rwheel + (abs(error)/3000)*maxturnspeed
     # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
     #delay 0.05 sec
     #delay 0.01 sec
    basic.pause(10)    

def follow_line():
    global lwheel, rwheel, error
 
    # get the line offset
    error = CutebotPro.get_offset()
 
    # make the left side of line the center
    # error = error + 1000
 
    # if detects no line
    if abs(error) == 3000:
        lwheel = 0
        rwheel = 0
 
         #turn on both headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)
     # if detects a big line
     #### Intersection ####
     # if detects a big line (error is less than 100)
    if abs(error) < 100:
        if error > 0: # robot is to the left of intersection (make a big right turn)
            error = 3000/error
            turn_r()
            basic.pause(100)
             #yellow light
            CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xffff00)
        elif error < 0: # robot is to the right of intersection (make a big left turn)
            error = 3000/error
            turn_l()
            basic.pause(100)
             #yellow light
            CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xffff00)

     # too far left
    if error > 0:
        turn_r()
         # turn on left headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)
     # too far right
    if error < 0:
        turn_l()
         #turn on right headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)
 
 
     # reset speed and headlights
    CutebotPro.turn_off_all_headlights()
    lwheel = 10
    rwheel = 10
 
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    basic.pause(5)
 
#basic.forever(on_forever)
#Run line follow till magnet detected then stop
while (magnet_detect() == 0):
    follow_line()
 # stop robot
CutebotPro.pwm_cruise_control(0, 0)
basic.pause(100)
CutebotPro.turn_off_all_headlights()



## START MAZE
CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 15.35, CutebotProDistanceUnits.CM)
basic.pause(1000)

#originate maze matrix
N = 5
M = 6
field = []
for j in range(N):
    row = []
    for i in range (M):
        row.append(0)
    field.append(row)

#originate empty path taken
path = []
first_move_done = False
maze_exit = False
magnet_count = 1

#functions for turning and moving forward
def check_distance():
    return CutebotPro.ultrasonic(SonarUnit.CENTIMETERS)

def turn_left():
    CutebotPro.trolley_steering(CutebotProTurn.LEFT_IN_PLACE, 95)
    basic.pause(100)

def turn_right():
    CutebotPro.trolley_steering(CutebotProTurn.RIGHT_IN_PLACE, 95)
    basic.pause(100)

def move_forward():
    CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 30.7, CutebotProDistanceUnits.CM)
    basic.pause(100)

#maze navigation before exit magnet is located 
while magnet_count < 3:
    mag = magnet_detect()
    #magnet found
    if mag == 1:
       magnet_count+=1
       #magnet inside maze located
       if magnet_count == 2:
           path.append(4)
    
    #end mazed navigation
    if magnet_count == 3:
        maze_exit = True
    #continue maze navigation
    else:   
        # Look left
        turn_left()
        left = check_distance()
        basic.pause(100)
        if left > 16:
            move_forward()
            path.append(2)
        else:
        # Face forward again
            turn_right()
            front = check_distance()
            basic.pause(100)
            if front > 16:
                move_forward()
                path.append(1)
            else:
                # Look right
                turn_right()
                right = check_distance()
                basic.pause(100)
                if right > 16:
                    turn_right()
                    move_forward()
                    path.append(3)
                else:
                    # Dead end
                    turn_right()
                    move_forward()
                    path.append(0)

                    #Depth first algorithm
                    for i in range(len(path)):
                        if path[i] == 2:
                            ...
                        elif path[i] == 3:
                            ...





# Output path after reaching end
serial.write_line("Maze path taken:")
for step in path:
    if step == 1:
        serial.write_line("Forward")
    elif step == 2:
        serial.write_line("Left")
    elif step == 3:
        serial.write_line("Right")
    elif step == 0:
        serial.write_line("Backtrack")

