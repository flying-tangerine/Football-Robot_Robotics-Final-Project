
class PID(object):
    def __init__(self, p, i, d, expect_value):
        self.p = p
        self.i = i
        self.d = d
        self.last_error = 0
        self.accmulate = 0
        self.expect_value = expect_value
        self.current_error = 0
        
    def CurrentPower(self, current_value):
        self.current_error = self.expect_value - current_value
        self.last_error = self.current_error
        self.accmulate = self.accmulate + self.current_error
        return self.p * self.current_error + self.i * self.accmulate + self.d * (self.current_error - self.last_error)

