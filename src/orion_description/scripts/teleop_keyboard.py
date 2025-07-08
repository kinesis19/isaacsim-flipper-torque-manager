#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import sys, select, termios, tty

MSG = """
---------------------------
Keyboard Teleop for Cygnus
---------------------------
        w
    a       d
        s (or x)

w/s : forward/backward
a/d : left/right turn

space : EMERGENCY STOP

CTRL-C to quit
---------------------------
"""

move_bindings = {
    'w': (1.0, 1.0),
    's': (-1.0, -1.0),
    'a': (-0.5, 0.5),
    'd': (0.5, -0.5),
    'x': (-1.0, -1.0),
}

class TeleopKeyboardNode(Node):
    def __init__(self):
        super().__init__('teleop_keyboard_node')
        self.settings = termios.tcgetattr(sys.stdin)

        self.vel_pub = self.create_publisher(Float64MultiArray, '/track_velocity_controller/commands', 10)

        self.speed = 2.0
        self.turn = 1.5
        
        print(MSG)
        self.run_teleop()

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run_teleop(self):
        while True:
            key = self.get_key()
            if key in move_bindings.keys():
                left_ratio = move_bindings[key][0]
                right_ratio = move_bindings[key][1]
                
                left_vel = self.turn * left_ratio if 'a' in key or 'd' in key else self.speed * left_ratio
                right_vel = self.turn * right_ratio if 'a' in key or 'd' in key else self.speed * right_ratio

                vel_cmd = Float64MultiArray()
                vel_cmd.data = [left_vel, left_vel, right_vel, right_vel]
                self.vel_pub.publish(vel_cmd)

            elif key == ' ':
                vel_cmd = Float64MultiArray()
                vel_cmd.data = [0.0, 0.0, 0.0, 0.0]
                self.vel_pub.publish(vel_cmd)

            elif (key == '\x03'):
                break

def main(args=None):
    rclpy.init(args=args)
    teleop_node = TeleopKeyboardNode()

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, teleop_node.settings)
    teleop_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()