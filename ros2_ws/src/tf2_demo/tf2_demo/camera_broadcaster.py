#!/usr/bin/env python3
"""Broadcasts the static transform from the robot's base_link to its camera_link.

This represents a camera mounted 0.3m forward and 0.4m up from the robot's
base, tilted down 20 degrees to look at the ground in front of the robot.
"""
import math

import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class CameraBroadcaster(Node):
    def __init__(self):
        super().__init__('camera_broadcaster')
        self.broadcaster = StaticTransformBroadcaster(self)
        self.broadcast_camera_transform()

    def broadcast_camera_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'camera_link'

        # Camera mount offset relative to base_link
        t.transform.translation.x = 0.3
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.4

        # Tilt the camera down 20 degrees (pitch) about the Y axis
        pitch = math.radians(20.0)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = math.sin(pitch / 2.0)
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = math.cos(pitch / 2.0)

        self.broadcaster.sendTransform(t)
        self.get_logger().info(
            'Published static transform base_link -> camera_link')


def main(args=None):
    rclpy.init(args=args)
    node = CameraBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
