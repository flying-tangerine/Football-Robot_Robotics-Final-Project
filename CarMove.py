import picar_4wd as fc
import time

class Move():  
    def __init__(self, power_discount, delay_steps):
        self.power_discount = power_discount
        self.delay_steps = delay_steps

    # car_movement(Rear motors, left motor, right motor)
    # power_discount: Preventing too large speed
    def car_movement(self, farward_power, turnleft_power, turnright_power):
        fc.left_front.set_power(turnleft_power/self.power_discount)
        fc.left_rear.set_power(farward_power/self.power_discount)
        fc.right_front.set_power(turnright_power/self.power_discount)
        fc.right_rear.set_power(farward_power/self.power_discount)

    # car_movement(rear-left motor, rear-right motor, front-left motor, front-right motor)
    def car_free_movement(self, rear_left_power, rear_right_power, turnleft_power, turnright_power):
        fc.left_front.set_power(turnleft_power/self.power_discount)
        fc.left_rear.set_power(rear_left_power/self.power_discount)
        fc.right_front.set_power(turnright_power/self.power_discount)
        fc.right_rear.set_power(rear_right_power/self.power_discount)

    def stop(self):
        fc.stop()

    # Smooth movement: The speed will gradually increase from 0 to a predetermined value
    # delay_steps: How many times to a predetermined value
    def delay_movement(self, farward_power, turnleft_power, turnright_power):
        current_power = 0
        current_left = 0
        current_right = 0
        power_increment = farward_power / self.delay_steps
        turn_left_increment = turnleft_power / self.delay_steps
        turn_right_increment = turnright_power / self.delay_steps
        for _ in range(self.delay_steps):
            current_power += power_increment
            current_left += turn_left_increment 
            current_right += turn_right_increment 
            self.car_movement(current_power, current_left, current_right)
        self.car_movement(farward_power, current_left, current_right)

    def kick_ball(self):   
        self.car_movement(-50 * self.power_discount, -50 * self.power_discount, -50 * self.power_discount)
        time.sleep(0.4)
        self.car_movement(1000 * self.power_discount, 1000 * self.power_discount, 1000 * self.power_discount)
        time.sleep(0.5)
        self.car_movement(-50 * self.power_discount,-50 * self.power_discount,-50 * self.power_discount)
        self.stop()