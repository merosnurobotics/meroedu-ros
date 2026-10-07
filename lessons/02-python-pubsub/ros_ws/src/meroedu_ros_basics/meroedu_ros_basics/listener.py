# Copyright 2016 Open Source Robotics Foundation, Inc.
# Copyright 2026 MERO educational adaptations
# SPDX-License-Identifier: Apache-2.0
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('meroedu_listener')
        self.subscription = self.create_subscription(String, '/meroedu/chatter', self.receive, 10)

    def receive(self, msg):
        self.get_logger().info('RX: '+msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = Listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

if __name__ == '__main__': main()
