"""Lesson 06 — launch a FLEET: 3 robots, each in its own namespace with its own params.

This is the real power of launch files, and a direct preview of WareFleet:
one command boots N configured robots. You would NEVER `ros2 run` them by hand.

Run:  ros2 launch params_launch_demo fleet.launch.py
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    nodes = []
    for i in range(3):
        rid = f'robot_{i}'
        nodes.append(Node(
            package='params_launch_demo',
            executable='robot',
            namespace=rid,               # namespacing → each robot's topics live under /robot_0, /robot_1, ...
            name='configurable_robot',
            output='screen',
            parameters=[{
                'robot_id': rid,
                'publish_rate_hz': 1.0,
                'battery_warn': 20,
            }],
        ))
    return LaunchDescription(nodes)      # a list of Nodes = start them all together
