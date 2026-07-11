"""Lesson 02 — my first ROS 2 node.

A node is just a program built on rclpy. This one starts up, then logs a
message once per second using a timer. No topics yet (that's Lesson 03) —
the point here is: how do I create, run, and inspect a node?
"""
import rclpy                     # the ROS 2 Python client library
from rclpy.node import Node      # base class every node inherits from


class HelloNode(Node):
    def __init__(self):
        # give the node its name (this is what shows up in `ros2 node list`)
        super().__init__('hello_node')

        self.count = 0
        # create_timer(period_seconds, callback) -> ROS calls self.tick() every 1.0s
        self.timer = self.create_timer(1.0, self.tick)

        # get_logger() is ROS 2's logging — shows up with the node name + level
        self.get_logger().info('hello_node has started')

    def tick(self):
        self.count += 1
        self.get_logger().info(f'hello ROS 2 — tick {self.count}')


def main(args=None):
    rclpy.init(args=args)        # 1) start up ROS 2
    node = HelloNode()           # 2) create the node
    try:
        rclpy.spin(node)         # 3) hand control to ROS: process timers/callbacks until Ctrl-C
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()      # 4) clean shutdown
        rclpy.shutdown()


if __name__ == '__main__':
    main()
