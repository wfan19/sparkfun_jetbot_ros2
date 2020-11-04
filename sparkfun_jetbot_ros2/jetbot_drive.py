import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64

from qwiic_scmd import QwiicScmd

import time

class JetbotDrive(Node):
    def __init__(self):
        super().__init__("jetbot_drive")

        self.left_motor_id = 0
        self.right_motor_id = 1

        self.motor_driver = QwiicScmd()
        self.motor_driver.begin()
        time.sleep(.250)
        self.set_motor_power(self.left_motor_id, 0)
        self.set_motor_power(self.right_motor_id, 0)
        self.motor_driver.enable()

        self.left_motor_sub = self.create_subscription(
            Float64, '~/left_motor', self.left_power_callback, 10)
            
        self.right_motor_sub = self.create_subscription(
            Float64, '~/right_motor', self.right_power_callback, 10)

    def stop(self):
        self.set_motor_power(self.left_motor_id, 0)
        self.set_motor_power(self.right_motor_id, 0)

        self.motor_driver.disable()
        self.destroy_node()

    # Sets motor power given a power from -1 to 1
    def set_motor_power(self, motor_id, power):
        self.motor_driver.set_drive(motor_id, 0, self.power_to_signal(power))

    # Scales an input from between -1 and 1 to between -255 to 255
    def power_to_signal(self, power):
        signal_range = 255
        return int(min(max(power * signal_range, -signal_range), signal_range))

    # Callback that takes Float64 message with motor power in range [-1 1]
    # and passes it to the motor driver as a 0-255 signal
    def left_power_callback(self, msg):
        self.set_motor_power(self.left_motor_id, msg.data)
        self.get_logger().info("Left power command: %f" % msg.data)

    def right_power_callback(self, msg):
        self.set_motor_power(self.right_motor_id, msg.data)
        self.get_logger().info("Right power command: %f" % msg.data)

def main(args=None):
    rclpy.init(args=args)

    jetbot_drive = JetbotDrive()
    try:
        rclpy.spin(jetbot_drive)
    except (KeyboardInterrupt):
        jetbot_drive.get_logger().info("Exiting node")

    # We have exited the loop so now we shutdown
    jetbot_drive.stop()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
