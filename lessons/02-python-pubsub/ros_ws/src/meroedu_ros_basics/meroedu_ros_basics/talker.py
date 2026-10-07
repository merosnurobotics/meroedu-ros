# Copyright 2016 Open Source Robotics Foundation, Inc.
# Copyright 2026 MERO educational adaptations
# SPDX-License-Identifier: Apache-2.0
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('meroedu_talker')
        self.publisher = self.create_publisher(String, '/meroedu/chatter', 10)
        self.count = 0
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        msg = String()
        msg.data = f'hello MERO {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info('TX: '+msg.data)
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = Talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

if __name__ == '__main__': main()
