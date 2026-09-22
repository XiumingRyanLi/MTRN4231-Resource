#!/usr/bin/env python3
"""Simulates a vision pipeline reporting a detected target's position.

Publishes a PointStamped in the camera_link frame that slowly circles,
standing in for "here is where the object detector found the target in
the camera image, converted to a 3D point in the camera's own frame".
"""
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped


class TargetPublisher(Node):
    def __init__(self):
        super().__init__('target_publisher')
        self.publisher = self.create_publisher(
            PointStamped, '/target_in_camera_frame', 10)
        self.timer = self.create_timer(0.2, self.publish_target)
        self.t = 0.0

    def publish_target(self):
        msg = PointStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_link'

        # A "detected object" 1.5m in front of the camera, drifting in a
        # small circle to simulate a moving target.
        msg.point.x = 1.5
        msg.point.y = 0.3 * math.sin(self.t)
        msg.point.z = 0.3 * math.cos(self.t)
        self.t += 0.05

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TargetPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
