"""Lesson 07 — an ACTION CLIENT.

The 3-phase async flow (same as an async job API):
  1) send goal        -> POST /jobs
  2) goal accepted?   -> 202 Accepted (or rejected)
  3) feedback stream  -> progress events
  4) result           -> final answer

Usage:  ros2 run actions_demo fib_client        (defaults to order=8)
"""
import sys
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from action_tutorials_interfaces.action import Fibonacci


class FibonacciClient(Node):
    def __init__(self):
        super().__init__('fibonacci_client')
        # ActionClient(node, action_type, action_name)  ≈ a stub for the async job API
        self._client = ActionClient(self, Fibonacci, 'compute_fibonacci')

    def send_goal(self, order):
        self._client.wait_for_server()             # wait until the server exists
        goal = Fibonacci.Goal()
        goal.order = order
        self.get_logger().info(f'sending goal: order={order}')
        # send_goal_async returns a future for the GOAL HANDLE; also register a feedback callback
        send_future = self._client.send_goal_async(goal, feedback_callback=self.on_feedback)
        send_future.add_done_callback(self.on_goal_response)

    def on_feedback(self, msg):                    # ≈ progress event handler (SSE/WebSocket)
        self.get_logger().info(f'feedback: {list(msg.feedback.partial_sequence)}')

    def on_goal_response(self, future):            # phase 2: accepted or rejected?
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('goal REJECTED')
            rclpy.shutdown()
            return
        self.get_logger().info('goal ACCEPTED')
        result_future = goal_handle.get_result_async()   # ask for the final result
        result_future.add_done_callback(self.on_result)

    def on_result(self, future):                   # phase 4: the result
        result = future.result().result
        self.get_logger().info(f'RESULT: {list(result.sequence)}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciClient()
    order = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    node.send_goal(order)
    rclpy.spin(node)                               # spin so callbacks fire; shuts down in on_result


if __name__ == '__main__':
    main()
