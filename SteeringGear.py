from picar_4wd.pwm import PWM
from picar_4wd.servo import Servo
import time


class SteeringGear():
    def __init__(self, PWM_id, ANGLE_RANGE, gear_STEP):
        self.ANGLE_RANGE = ANGLE_RANGE
        self.max_angle = int(self.ANGLE_RANGE/2)
        self.min_angle = int(-self.ANGLE_RANGE/2)
        self.STEP = gear_STEP
        self.servo1 = Servo(PWM(PWM_id[0]))
        self.servo2 = Servo(PWM(PWM_id[1]))


    def gear_catch(self, stop_angle=0):
        for angle1, angle2 in zip(range(self.max_angle, stop_angle, -self.STEP), range(self.min_angle, -stop_angle, self.STEP)):
            self.servo1.set_angle(angle1)
            self.servo1.set_angle(angle2)
            time.sleep(0.04)

    def gear_release(self):
        self.servo1.set_angle(self.max_angle)
        self.servo2.set_angle(self.min_angle)

    def test(self, stop_angle):
        time1 = time.time()
        self.servo1.set_angle(self.max_angle)
        self.servo2.set_angle(self.min_angle)
        self.gear_catch(self.servo1, self.servo2, stop_angle)
        while True:
            time2 = time.time()
            if time2-time1>=5:
                self.gear_release()
                break

