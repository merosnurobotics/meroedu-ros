# SPDX-License-Identifier: Apache-2.0
"""Illustrative pose for learning messages and RViz; no sensor or localization."""
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

class PosePublisher(Node):
    def __init__(self):
        super().__init__('meroedu_pose_example')
        self.pub = self.create_publisher(PoseStamped, '/meroedu/pose', 10)
        self.timer = self.create_timer(0.1, self.send)

    def send(self):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.pose.position.x = 1.0
        msg.pose.position.y = 0.5
        msg.pose.orientation.z = math.sin(math.pi / 8)
        msg.pose.orientation.w = math.cos(math.pi / 8)
        self.pub.publish(msg)

def main():
    rclpy.init(); node = PosePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

if __name__ == '__main__': main()
