#!/usr/bin/env python3
"""
Copyright 2021 Owen Bulka

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# Standard Imports
import time

# Local Imports
from electricipy.raspi.motors import servo, stepper, brushless


def stepper_test():
    """"""
    step_pins = [18, 13]
    direction_pins = [3, 27]
    enable_pins = [4, 17]
    microstep_pins = [[15, 14], [24, 23]]
    microsteps = [64, 64]

    motor_manager = stepper.StepperMotorManager.tmc2209_manager(
        step_pins,
        direction_pins,
        enable_pins,
        microstep_pins,
        microsteps,
    )


    motor_manager.move_by_angles_in_times([-700, 700], [6, 6])
    motor_manager.move_by_angles_in_times([700, -700], [6, 6])


def servo_test():
    """"""
    # servo_manager = servo.ServoMotorManager.sg90_manager([19])
    servo_manager = servo.ServoMotorManager.hk15148b_manager([19])

    try:
        while True:
            servo_manager[0].min()
            time.sleep(2)
            servo_manager[0].mid()
            time.sleep(2)
            # servo_manager[0].min()
            # time.sleep(2)
            # servo_manager[0].mid()
            # time.sleep(2)

    except KeyboardInterrupt:
        print("Program stopped")


def esc_test():
    """"""
    esc = brushless.ElectronicSpeedController(19)
    esc.arm()
    esc.run_at_pulse_width_for_time(1000, 1)


def main():
    """ Script to test development """
    start_time = time.time()

    esc_test()

    print("--- %s seconds ---" % (time.time() - start_time))

    # motor.step(10)


if __name__ == "__main__":
    main()
