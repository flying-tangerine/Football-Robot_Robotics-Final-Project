from Football_Robort import FootballCar

if __name__ == '__main__':
    car = FootballCar()
        # car1: Attacker Loop
    for i in range(4):
        i+=1
        car.track_the_ball()
        car.ball_catcher()
        car.ball_target_aim()
        car.ball_release()
        car.move.kick_ball()
        car.move.stop()
