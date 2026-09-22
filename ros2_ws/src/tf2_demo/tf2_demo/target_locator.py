#!/usr/bin/env python3
"""Looks up a target detected in the camera frame relative to the robot.

This is the payoff of the TF2 tree: a target's position is only known in
camera_link (where the vision node saw it), but to drive the robot toward
it we need that position in base_link. tf2_ros does the lookup for us
instead of us hand-composing rotation matrices.
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
import tf2_geometry_msgs  # noqa: F401  (registers PointStamped transform support)


class TargetLocator(Node):
    def __init__(self):
        super().__init__('target_locator')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.subscription = self.create_subscription(
            PointStamped, '/target_in_camera_frame', self.on_target, 10)
        self.publisher = self.create_publisher(
            PointStamped, '/target_in_base_link', 10)

    def on_target(self, msg: PointStamped):
        try:
            target_in_base = self.tf_buffer.transform(
                msg, 'base_link', timeout=rclpy.duration.Duration(seconds=0.2))
        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().warn(f'TF lookup failed: {e}')
            return

        self.publisher.publish(target_in_base)
        self.get_logger().info(
            'Target relative to robot base_link: '
            f'x={target_in_base.point.x:.2f} '
            f'y={target_in_base.point.y:.2f} '
            f'z={target_in_base.point.z:.2f}',
            throttle_duration_sec=1.0,
        )


def main(args=None):
    rclpy.init(args=args)
    node = TargetLocator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
