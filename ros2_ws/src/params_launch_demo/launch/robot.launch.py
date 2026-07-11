"""Lesson 06 — launch ONE node with parameters.

A launch file is a Python script that describes which processes to start and
with what config. Analogy: a docker-compose service / a K8s manifest / a
systemd unit — the "deployment descriptor".

Run:  ros2 launch params_launch_demo robot.launch.py
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():          # ROS calls this; must return a LaunchDescription
    return LaunchDescription([
        Node(
            package='params_launch_demo',   # which package
            executable='robot',             # which executable (from setup.py entry_points)
            name='configurable_robot',      # the node's runtime name
            output='screen',                # show its logs in the terminal
            parameters=[{                   # inject parameters (≈ env/config for this service)
                'robot_id': 'robot_A',
                'publish_rate_hz': 2.0,
                'battery_warn': 30,
            }],
        ),
    ])
