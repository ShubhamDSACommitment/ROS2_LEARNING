"""Lesson 07 — an ACTION SERVER (long-running job with feedback + result).

We use the Fibonacci action as a stand-in for any long task ("compute N terms,
one per second"). A real robot uses the SAME pattern for NavigateToPose:
  goal = target pose, feedback = distance remaining, result = success/failure.

Action type (action_tutorials_interfaces/action/Fibonacci):
  Goal    : int32 order
  Feedback: int32[] partial_sequence
  Result  : int32[] sequence
"""
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from action_tutorials_interfaces.action import Fibonacci


class FibonacciServer(Node):
    def __init__(self):
        super().__init__('fibonacci_server')
        # ActionServer(node, action_type, action_name, execute_callback)
        self._server = ActionServer(
            self, Fibonacci, 'compute_fibonacci', self.execute)
        self.get_logger().info('action server ready: compute_fibonacci')

    def execute(self, goal_handle):
        order = goal_handle.request.order          # the GOAL (the request/job)
        self.get_logger().info(f'goal accepted: order={order}')

        seq = [0, 1]
        feedback = Fibonacci.Feedback()

        for i in range(1, order):
            # cooperative cancellation check (≈ ctx.Done() / future.isCancelled())
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('goal CANCELED')
                return Fibonacci.Result()

            seq.append(seq[i] + seq[i - 1])
            feedback.partial_sequence = seq
            goal_handle.publish_feedback(feedback)  # stream PROGRESS (≈ SSE / progress channel)
            self.get_logger().info(f'feedback: {seq}')
            time.sleep(1.0)                         # simulate slow work

        goal_handle.succeed()                       # mark success
        result = Fibonacci.Result()
        result.sequence = seq
        self.get_logger().info(f'result: {seq}')
        return result                               # the RESULT (final return)


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
    # NOTE: with the default single-threaded executor, the time.sleep() blocks
    # the executor, so a cancel sent mid-sleep is only seen at the next loop.
    # For instantly-responsive cancel you'd use a MultiThreadedExecutor +
    # callback groups (advanced — not needed to learn the pattern).


if __name__ == '__main__':
    main()
