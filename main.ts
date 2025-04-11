let mag: number;
let left: number;
let front: number;
let right: number;
// # MAGNET DETECTION
// magnet checking function
function magnet_detect(): number {
    let mag = 0
    let force = Math.abs(input.magneticForce(Dimension.X))
    if (force >= 500) {
        mag = 1
        //  turn headlights green
        CutebotPro.colorLight(RGBLight.RGBL, 0x00ff00)
        CutebotPro.colorLight(RGBLight.RGBR, 0x00ff00)
    }
    
    return mag
}

// # BACKGROUND MUSIC
function missionImpossibleMusic(bpm: number) {
    music.play(music.stringPlayable("G4 G4 - G4 G4 G4 Bb4 Bb4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("C5 C5 G4 G4 - G4 G4 G4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("Fb4 Fb4 F4 F4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("G4 G4 - G4 G4 G4 Bb4 Bb4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("C5 C5 G4 G4 - G4 G4 G4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("Fb4 Fb4 F4 F4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("A6 G6 D5 D5 D5 D5 D5 D5 - -", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("A6 G6 Db5 Db5 Db5 Db5 Db5 Db5 - -", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("A6 G6 C5 C5 C5 C5 C5 C5 - -", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("Bb4 C5 - -", bpm), music.PlaybackMode.UntilDone)
}

control.inBackground(function onIn_background() {
    missionImpossibleMusic(350)
    
})
// # DIRECTION CORRECTION FUNCTIONS
function straighten_to_line() {
    let error: number;
    let speed: number;
    // keep counter to break while loop
    let count = 0
    CutebotPro.pwmCruiseControl(20, 20)
    basic.pause(50)
    //  turn on headlights(pink = 247, 25, 236)
    CutebotPro.singleHeadlights(RGBLight.RGBL, 247, 25, 236)
    CutebotPro.singleHeadlights(RGBLight.RGBR, 247, 25, 236)
    // keep turning till we are straight
    while (Math.abs(CutebotPro.getOffset()) > 0 && count < 10) {
        //  update count of while loop iterations
        count = count + 1
        // get offset
        error = CutebotPro.getOffset()
        //  set turn speed
        speed = 30 + error / 3000 * 70
        //  turn right
        if (error > 0) {
            // turn on right headlight(blue = 51, 255, 252)
            CutebotPro.singleHeadlights(RGBLight.RGBR, 51, 255, 252)
            CutebotPro.pwmCruiseControl(speed, -1 * speed)
            basic.pause(30)
            //  turn off headlights
            CutebotPro.turnOffAllHeadlights()
        }
        
        //  turn left
        if (error < 0) {
            // turn on left headlight(blue = 51, 255, 252)
            CutebotPro.singleHeadlights(RGBLight.RGBL, 51, 255, 252)
            CutebotPro.pwmCruiseControl(-1 * speed, speed)
            basic.pause(30)
            //  turn off headlights
            CutebotPro.turnOffAllHeadlights()
        }
        
        CutebotPro.pwmCruiseControl(0, 0)
        basic.pause(20)
    }
    //  turn off headlights
    CutebotPro.turnOffAllHeadlights()
}

function detect_line(): number {
    //  get the line tracking offset
    let error = CutebotPro.getOffset()
    let line = 0
    //  detects black line
    if (Math.abs(error) < 3000) {
        CutebotPro.pwmCruiseControl(0, 0)
        straighten_to_line()
        line = 1
    }
    
    return line
}

// # LINE FOLLOWING
// set variables
let lwheel = 20
let rwheel = 20
let error = 0
let maxturnspeed = 50
//  set starting speed
CutebotPro.pwmCruiseControl(lwheel, rwheel)
basic.pause(50)
// turns for line following
function turn_r() {
    
    lwheel = lwheel + Math.abs(error) / 3000 * maxturnspeed
    rwheel = rwheel - Math.abs(error) / 3000 * maxturnspeed
    //  Set the change
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    // delay 0.05 sec
    // delay 0.01 sec
    basic.pause(10)
}

function turn_l() {
    
    lwheel = lwheel - Math.abs(error) / 3000 * maxturnspeed
    rwheel = rwheel + Math.abs(error) / 3000 * maxturnspeed
    //  Set the change
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    // delay 0.05 sec
    // delay 0.01 sec
    basic.pause(10)
}

function follow_line() {
    
    //  get the line offset
    error = CutebotPro.getOffset()
    //  make the left side of line the center
    //  error = error + 1000
    //  if detects no line
    if (Math.abs(error) == 3000) {
        lwheel = 0
        rwheel = 0
        // turn on both headlight (red)
        CutebotPro.colorLight(RGBLight.RGBL, 0xff0000)
        CutebotPro.colorLight(RGBLight.RGBR, 0xff0000)
    }
    
    //  if detects a big line
    // ### Intersection ####
    //  if detects a big line (error is less than 100)
    if (Math.abs(error) < 100) {
        if (error > 0) {
            //  robot is to the left of intersection (make a big right turn)
            error = 3000 / error
            turn_r()
            basic.pause(100)
            // yellow light
            CutebotPro.colorLight(RGBLight.RGBL, 0xffff00)
        } else if (error < 0) {
            //  robot is to the right of intersection (make a big left turn)
            error = 3000 / error
            turn_l()
            basic.pause(100)
            // yellow light
            CutebotPro.colorLight(RGBLight.RGBR, 0xffff00)
        }
        
    }
    
    //  too far left
    if (error > 0) {
        turn_r()
        //  turn on left headlight (red)
        CutebotPro.colorLight(RGBLight.RGBL, 0xff0000)
    }
    
    //  too far right
    if (error < 0) {
        turn_l()
        // turn on right headlight (red)
        CutebotPro.colorLight(RGBLight.RGBR, 0xff0000)
    }
    
    //  reset speed and headlights
    CutebotPro.turnOffAllHeadlights()
    lwheel = 10
    rwheel = 10
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    basic.pause(5)
}

// Run line follow till magnet detected then stop
// while (magnet_detect() == 0):
// follow_line()
//  stop robot
CutebotPro.pwmCruiseControl(0, 0)
basic.pause(100)
CutebotPro.turnOffAllHeadlights()
// # START MAZE
CutebotPro.distanceRunning(CutebotProOrientation.Advance, 15.35, CutebotProDistanceUnits.Cm)
basic.pause(1000)
// originate maze matrix and depth first search variables
// N = 5
// M = 6
// field = []
// for j in range(N):
// row = []
// for i in range(M):
// row.append(0)
// field.append(row)
let grid_type : number[] = []
// Java script, defines array as an integer array
let intersection : number[] = []
// originate empty path taken
let path : number[] = []
let first_move_done = false
let maze_exit = false
let magnet_count = 1
// functions for turning and moving forward
function check_distance(): number {
    return CutebotPro.ultrasonic(SonarUnit.Centimeters)
}

function turn_left() {
    CutebotPro.trolleySteering(CutebotProTurn.LeftInPlace, 95)
    basic.pause(100)
}

function turn_right() {
    CutebotPro.trolleySteering(CutebotProTurn.RightInPlace, 95)
    basic.pause(100)
}

function move_forward() {
    CutebotPro.pwmCruiseControl(10, 10)
    let line_found = 0
    while (line_found == 0) {
        line_found = detect_line()
    }
    CutebotPro.distanceRunning(CutebotProOrientation.Advance, 15.35, CutebotProDistanceUnits.Cm)
    basic.pause(100)
}

// move_forward()
// maze navigation before exit magnet is located 
while (magnet_count < 3) {
    mag = magnet_detect()
    // magnet found
    if (mag == 1) {
        magnet_count += 1
        // magnet inside maze located
        if (magnet_count == 2) {
            path.push(4)
        }
        
    }
    
    // end mazed navigation
    if (magnet_count == 3) {
        maze_exit = true
    } else {
        // continue maze navigation
        //  Look left
        turn_left()
        left = check_distance()
        basic.pause(100)
        if (left > 16) {
            move_forward()
            path.push(2)
        } else {
            //  Look forward
            turn_right()
            front = check_distance()
            basic.pause(100)
            if (front > 16) {
                move_forward()
                path.push(1)
            } else {
                //  Look right
                turn_right()
                right = check_distance()
                basic.pause(100)
                if (right > 16) {
                    turn_right()
                    move_forward()
                    path.push(3)
                } else {
                    //  Dead end
                    turn_right()
                    move_forward()
                    path.push(0)
                }
                
            }
            
        }
        
    }
    
}
// # TRANSMISSION
//  Small delay for good transmission
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    basic.pause(1000)
    for (let i = 0; i < path.length; i++) {
        radio.sendValue("step", path[i])
        basic.pause(700)
    }
})
radio.setGroup(1)
// # CELEBRATE
function total(bpm: number) {
    CutebotPro.pwmCruiseControl(0, 100)
    CutebotPro.colorLight(RGBLight.RGBL, 0xff0000)
    CutebotPro.colorLight(RGBLight.RGBR, 0x7f00ff)
    music.play(music.stringPlayable("C", bpm), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(RGBLight.RGBL, 0xff8000)
    CutebotPro.colorLight(RGBLight.RGBR, 0x007fff)
    music.play(music.stringPlayable("C", bpm), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(RGBLight.RGBL, 0xffff00)
    CutebotPro.colorLight(RGBLight.RGBR, 0x00ff00)
    music.play(music.stringPlayable("C", bpm), music.PlaybackMode.UntilDone)
    CutebotPro.pwmCruiseControl(100, 0)
    CutebotPro.colorLight(RGBLight.RGBL, 0x00ff00)
    CutebotPro.colorLight(RGBLight.RGBR, 0xffff00)
    music.play(music.stringPlayable("C", bpm * 2), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(RGBLight.RGBL, 0x00ffff)
    CutebotPro.colorLight(RGBLight.RGBR, 0xff8000)
    music.play(music.stringPlayable("C5", bpm * 2), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(RGBLight.RGBL, 0x007fff)
    CutebotPro.colorLight(RGBLight.RGBR, 0xff0000)
    music.play(music.stringPlayable("F", bpm), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(RGBLight.RGBL, 0x7f00ff)
    CutebotPro.colorLight(RGBLight.RGBR, 0xff00ff)
    music.play(music.stringPlayable("F", bpm), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(RGBLight.RGBL, 0xff00ff)
    CutebotPro.colorLight(RGBLight.RGBR, 0x00ff00)
    CutebotPro.pwmCruiseControl(0, 100)
    music.play(music.stringPlayable("E", bpm * 2), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(RGBLight.RGBL, 0x00ff00)
    CutebotPro.colorLight(RGBLight.RGBR, 0xff00ff)
    CutebotPro.pwmCruiseControl(100, 0)
    music.play(music.stringPlayable("A", bpm * 2), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(RGBLight.RGBL, 0xff00ff)
    CutebotPro.colorLight(RGBLight.RGBR, 0x00ff00)
    CutebotPro.pwmCruiseControl(0, 100)
    music.play(music.stringPlayable("E", bpm * 2), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(RGBLight.RGBL, 0x00ff00)
    CutebotPro.colorLight(RGBLight.RGBR, 0xff00ff)
    CutebotPro.pwmCruiseControl(100, 0)
    music.play(music.stringPlayable("A", bpm * 2), music.PlaybackMode.UntilDone)
}

total(130)
