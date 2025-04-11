## MAGNET DETECTION
#magnet checking function
def magnet_detect():
    mag = 0
    force = abs(input.magnetic_force(Dimension.X))
    if force >= 500:
        mag = 1
         # turn headlights green
        CutebotPro.color_light(RGBLight.RGBL, 0x00ff00)
        CutebotPro.color_light(RGBLight.RGBR, 0x00ff00)
    return mag

## DIRECTION CORRECTION FUNCTIONS
def straighten_to_line():
    #keep counter to break while loop
    count = 0

    CutebotPro.pwm_cruise_control(20, 20)
    basic.pause(50)

    # turn on headlights(pink = 247, 25, 236)
    CutebotPro.single_headlights(RGBLight.RGBL, 247, 25, 236)
    CutebotPro.single_headlights(RGBLight.RGBR, 247, 25, 236)
    #keep turning till we are straight
    while(abs(CutebotPro.get_offset()) > 0 and count < 10):
        # update count of while loop iterations
        count = count + 1
        #get offset
        error = CutebotPro.get_offset()
        # set turn speed
        speed = 30 + (error/3000)*70
        # turn right
        if error > 0:
            #turn on right headlight(blue = 51, 255, 252)
            CutebotPro.single_headlights(RGBLight.RGBR, 51, 255, 252)
            CutebotPro.pwm_cruise_control(speed, -1*speed)
            basic.pause(30)
            # turn off headlights
            CutebotPro.turn_off_all_headlights()
        # turn left
        if error < 0:
            #turn on left headlight(blue = 51, 255, 252)
            CutebotPro.single_headlights(RGBLight.RGBL, 51, 255, 252)
            CutebotPro.pwm_cruise_control(-1*speed, speed)
            basic.pause(30)
            # turn off headlights
            CutebotPro.turn_off_all_headlights()

        CutebotPro.pwm_cruise_control(0, 0)
        basic.pause(20)

    # turn off headlights
    CutebotPro.turn_off_all_headlights()

def detect_line():
    # get the line tracking offset
    error = CutebotPro.get_offset()
    line = 0
    # detects black line
    if abs(error) < 3000:
        CutebotPro.pwm_cruise_control(0, 0)
        straighten_to_line()
        line = 1
    return line

## LINE FOLLOWING
#set variables
lwheel = 20
rwheel = 20
error = 0
maxturnspeed = 50

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
        CutebotPro.color_light(RGBLight.RGBL, 0xff0000)
        CutebotPro.color_light(RGBLight.RGBR, 0xff0000)
     # if detects a big line
     #### Intersection ####
     # if detects a big line (error is less than 100)
    if abs(error) < 100:
        if error > 0: # robot is to the left of intersection (make a big right turn)
            error = 3000/error
            turn_r()
            basic.pause(100)
             #yellow light
            CutebotPro.color_light(RGBLight.RGBL, 0xffff00)
        elif error < 0: # robot is to the right of intersection (make a big left turn)
            error = 3000/error
            turn_l()
            basic.pause(100)
             #yellow light
            CutebotPro.color_light(RGBLight.RGBR, 0xffff00)

     # too far left
    if error > 0:
        turn_r()
         # turn on left headlight (red)
        CutebotPro.color_light(RGBLight.RGBL, 0xff0000)
     # too far right
    if error < 0:
        turn_l()
         #turn on right headlight (red)
        CutebotPro.color_light(RGBLight.RGBR, 0xff0000)
 
 
    # reset speed and headlights
    CutebotPro.turn_off_all_headlights()
    lwheel = 10
    rwheel = 10
 
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    basic.pause(5)
 

#Run line follow till magnet detected then stop

#while (magnet_detect() == 0):
    #follow_line()
 # stop robot
CutebotPro.pwm_cruise_control(0, 0)
basic.pause(100)
CutebotPro.turn_off_all_headlights()


## START MAZE
CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 15.35, CutebotProDistanceUnits.CM)
basic.pause(1000)

#originate maze matrix and depth first search variables
#N = 5
#M = 6
#field = []
#for j in range(N):
    #row = []
    #for i in range(M):
        #row.append(0)
    #field.append(row)

grid_type: List[number] = [] #Java script, defines array as an integer array
intersection: List[number] = []


#originate empty path taken
path: List[number] = [] 
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
    CutebotPro.pwm_cruise_control(10, 10)
    line_found = 0
    while line_found == 0:
        line_found = detect_line()
    CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 15.35, CutebotProDistanceUnits.CM)
    basic.pause(100)

#move_forward()


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
        # Look forward
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

            

## TRANSMISSION
def on_button_pressed_a():
    basic.pause(1000)
    for i in range(len(path)):
        radio.send_value("step", path[i])
        basic.pause(700)  # Small delay for good transmission
input.on_button_pressed(Button.A, on_button_pressed_a)
radio.set_group(1)



