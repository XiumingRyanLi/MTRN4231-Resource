from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    rviz_config = PathJoinSubstitution(
        [FindPackageShare('tf2_demo'), 'rviz', 'tf2_demo.rviz'])

    return LaunchDescription([
        Node(
            package='tf2_demo',
            executable='camera_broadcaster',
            name='camera_broadcaster',
            output='screen',
        ),
        Node(
            package='tf2_demo',
            executable='target_publisher',
            name='target_publisher',
            output='screen',
        ),
        Node(
            package='tf2_demo',
            executable='target_locator',
            name='target_locator',
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen',
        ),
    ])
