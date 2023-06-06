
import cv2 as cv
import numpy as np

class Cam():  # create class Car, which derives all the modules
    def __init__(self, cap_id, lower_hsv_ball, upper_hsv_ball, lower_hsv_goal, upper_hsv_goal): # two objects
        self.cap = cv.VideoCapture(cap_id)
        self.screen_width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        self.screen_height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.min_area = 500
        self.ball_HSV = [lower_hsv_ball, upper_hsv_ball]
        self.goal_HSV = [lower_hsv_goal, upper_hsv_goal]

    def morphological_operation(self, frame):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))  
        dst = cv.morphologyEx(frame, cv.MORPH_CLOSE, kernel) 
        return dst

    # TODO: to tennies ball
    def area_to_distance(self, area):
        area /= 1.5e4
        if area > 0.16:
            return 42.54 * (area ** (-0.4168)) - 22.15 + 5
        else:
            return 57.13 * (area ** (-0.3572)) - 40.43
    
    # Deviation of the x-center of the tennis ball from the x-center of the screen/car
    def center_bias(self, object_center):
        if object_center is None:
            return None
        return object_center - self.screen_width/2
    
    # Detects the largest continuous area of a specific color on the screen, 
    # Return area and xy-center
    def color_detect(self, frame, object):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) 
        mask = cv.inRange(hsv, lowerb=np.array(object[0]), upperb=np.array(object[1])) 
        ret, thresh = cv.threshold(mask, 40, 255, cv.THRESH_BINARY) 
        scr1 = self.morphological_operation(thresh)
        contours, heriachy1 = cv.findContours(scr1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  
        max_area = 0
        max_contour = contours
        if len(contours) > 0:
            max_contour = max(contours, key=cv.contourArea)
            max_area = cv.contourArea(max_contour)
        else:
            max_area = 0
        if max_area > self.min_area:
            (x, y), radius = cv.minEnclosingCircle(max_contour)
            return max_area, x, y
        else:
            return 0, None, None
        
    def aim(self): # input
        ret, frame = self.cap.read()
        if not ret:
            print('========= NO <FRAME> RETURN =========')
            return None, None
        ball_area, ball_x, ball_y = self.color_detect(frame, self.ball_HSV)
        goal_area, goal_x, goal_y = self.color_detect(frame, self.goal_HSV)
        return  ball_x, goal_x

    def get_ball_info(self):
        ret, frame = self.cap.read()
        if not ret:
            print('========= NO <FRAME> RETURN =========')
            return None, None
        ball_area, ball_x, ball_y = self.color_detect(frame, self.ball_HSV)
        if ball_area > self.min_area:
            ball_dist = self.area_to_distance(ball_area)
        else:
            ball_dist = 0
        ball_center = self.center_bias(ball_x)
        if ball_center is None:
            print('========= NO <CENTER> RETURN =========')
            return None, None
        return ball_dist, ball_center

