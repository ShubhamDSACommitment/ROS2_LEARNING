"""Lesson 04 — a SERVICE CLIENT (the caller).

Backend analogy: a gRPC stub call / a RestTemplate/WebClient call.
Usage:
  ros2 run services_demo power_client true      # enable
  ros2 run services_demo power_client false     # disable
"""
import sys
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class PowerClient(Node):
    def __init__(self):
        super().__init__('power_client')

        # create_client(srv_type, service_name)  ≈ building a gRPC stub / a WebClient for an endpoint
        self.cli = self.create_client(SetBool, 'set_robot_active')

        # wait until the server exists (≈ readiness check / service discovery)
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for /set_robot_active ...')

    def send(self, activate: bool):
        req = SetBool.Request()          # build the request object (≈ new Request DTO)
        req.data = activate

        future = self.cli.call_async(req)          # async call -> a Future (≈ CompletableFuture / a channel)
        rclpy.spin_until_future_complete(self, future)  # block until it resolves (≈ future.get() / <-ch)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    node = PowerClient()

    # tiny arg parse: default to enabling
    activate = True
    if len(sys.argv) > 1:
        activate = sys.argv[1].lower() in ('1', 'true', 'on', 'yes')

    resp = node.send(activate)
    node.get_logger().info(
        f'response: success={resp.success} message="{resp.message}"')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
