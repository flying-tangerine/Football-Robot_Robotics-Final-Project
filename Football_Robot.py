import time
import cv2 as cv
from Cam import Cam
from CarMove import Move
from PID_controller import PID
from SteeringGear import SteeringGear

class FootballCar():  
    def __init__(self):
        # init Camera
        self.CAM = Cam(cap_id=0, lower_hsv_ball=[14, 83, 113], upper_hsv_ball=[66, 255, 255], 
                       lower_hsv_goal=[109, 99, 27], upper_hsv_goal=[119, 255, 255])
        # init Steering gear
        self.catcher = SteeringGear(PWM_id=["P1","P2"], ANGLE_RANGE=180, gear_STEP=15)
        self.stop_angle = -15
        # init Motor
        self.power_discount = 5
        self.delay_steps = 5
        self.move = Move(power_discount = self.power_discount, delay_steps = self.delay_steps)
        # Params
        self.stop_infront = 7
        self.center_range = 0
        self.min_speed = 1
        self.Orientation_rate = 0.8
        self.FORWARD = True
        self.TURN_RIGHT = True
        # PID
        self.orientation_pid = PID(p=0.9, i=0, d=0.1, expect_value = self.center_range)
        self.motor_pid = PID(p=1, i=0, d=0, expect_value = self.stop_infront)
        
        
    ### Attacker Movement Stratigies
    #   Forward: Control by rear_left, rear_right, front left, front right
    #   Turn Right/Left: Control by front left and front right
    #   E.g. Right (Left Speed > Right Speed) == (Motor speed * 0.8 > Motor speed * 0.2) 
    ###  
    def ball_tracker_Attacker(self, motor_speed, Orientation_speed):
        if self.FORWARD:
            if self.TURN_RIGHT:
                self.move.delay_movement(motor_speed, Orientation_speed * self.Orientation_rate, Orientation_speed * (self.Orientation_rate-1))
            else:
                self.move.delay_movement(motor_speed, Orientation_speed * (self.Orientation_rate-1), Orientation_speed * self.Orientation_rate)
        else:
            if self.TURN_RIGHT:
                self.move.delay_movement(-motor_speed, -Orientation_speed *(self.Orientation_rate-1), -Orientation_speed * self.Orientation_rate)
            else:
                self.move.delay_movement(-motor_speed, -Orientation_speed * self.Orientation_rate, -Orientation_speed * (self.Orientation_rate-1))
    
    ### Defanser Movement Stratigies
    #   Only Forward and Backward
    ###
    def ball_tracker_Defanser(self, motor_speed):
        if self.FORWARD:
            self.move.delay_movement(motor_speed, motor_speed, motor_speed)
        else:
            self.move.delay_movement(-motor_speed, -motor_speed, -motor_speed)

    def ball_catcher(self):
        self.catcher.gear_catch(self.stop_angle)
        return 
    
    def ball_release(self):
        self.catcher.gear_release()
        return 
    
    def ball_target_aim(self):
        # Aim the Target
        while True:
            self.move.car_free_movement(-10,10,-10,10)
            ball_x, goal_x = self.CAM.aim()
            if abs(ball_x - goal_x) > 200:
                self.move.stop()
                break

    ### Track the ball
    #   if ball inside Cam Window => Follow the Car
    #   else rotate Car
    #   stop when reach the stop_infront distance and hold 9 steps.
    ###
    def track_the_ball(self):
        try:
            count_close = 0
            while True:
            # camera
                dist, center = self.CAM.get_ball_info()
                if dist <= self.stop_infront:
                    count_close += 1
                if count_close >= 8:
                    self.move.stop()
                    return              # Early Stop
                if center is None:
                    self.move.car_free_movement(-5,5,-5,5)
                    time.sleep(0.01)
                    self.move.stop()
                    continue
            # pid-control 
                Orientation_speed = - self.orientation_pid.CurrentPower(center)
                motor_speed = - self.motor_pid.CurrentPower(dist)
            
                if motor_speed >= 0:
                    self.FORWARD = True
                else:
                    self.FORWARD = False
                if Orientation_speed >= 0:
                    self.TURN_RIGHT = True
                else:
                    self.TURN_RIGHT = False

                Orientation_speed = abs(Orientation_speed)
                motor_speed = abs(motor_speed)
            # movement  
                self.ball_tracker_Attacker(motor_speed, Orientation_speed)
                # print('Distance: ', dist, 'Center: ', center, '  Forward: ', self.FORWARD,  'TURN_RIGHT: ', self.TURN_RIGHT,   'Motor_Speed: ', motor_speed, 'Orientation_Speed: ', Orientation_speed)
            self.move.stop()
            # print('Distance: ', dist, 'Center: ', center, '  Forward: ', self.FORWARD,  'TURN_RIGHT: ', self.TURN_RIGHT,   'Motor_Speed: ', motor_speed, 'Orientation_Speed: ', Orientation_speed)
        except KeyboardInterrupt:
            # print('Distance: ', dist, 'Center: ', center, '  Forward: ', self.FORWARD,  'TURN_RIGHT: ', self.TURN_RIGHT,   'Motor_Speed: ', motor_speed, 'Orientation_Speed: ', Orientation_speed)
            # print('========= PROCESS <STOP> BY USER =========')
            self.move.stop()

    # TODO: Attacker
    def Attacker():
        return 

    # TODO: Defanse
    def Defanser(self):
        try:
            self.motor_pid.SetExpectedOutput(self.center_range)
            iteration = 0
            while True:
                iteration += 1
                if iteration > 1000:
                    self.move.stop()
                    break
            # camera
                dist, center = self.CAM.get_ball_info()
                if center is None:
                    self.move.stop()
                    continue
            # pid-control 
                motor_speed = - self.motor_pid.CurrentPower(center)
            
                if motor_speed >= 0:
                    self.FORWARD = True
                else:
                    self.FORWARD = False
                motor_speed = abs(motor_speed)

            # movement  
                self.ball_tracker_Defanser(motor_speed)
                # print('Distance: ', dist, 'Center: ', center, '  Forward: ', self.FORWARD,  'TURN_RIGHT: ', self.TURN_RIGHT,   'Motor_Speed: ', motor_speed, 'Orientation_Speed: ', Orientation_speed)
            self.move.stop()
            # print('Distance: ', dist, 'Center: ', center, '  Forward: ', self.FORWARD,  'TURN_RIGHT: ', self.TURN_RIGHT,   'Motor_Speed: ', motor_speed)
        except KeyboardInterrupt:
            # print('Distance: ', dist, 'Center: ', center, '  Forward: ', self.FORWARD,  'TURN_RIGHT: ', self.TURN_RIGHT,   'Motor_Speed: ', motor_speed)
            # print('========= PROCESS <STOP> BY USER =========')
            self.move.stop()
        return
    