"""Lesson 04 — a SERVICE SERVER (the endpoint).

Think: a robot that exposes an "enable/disable me" command.
Backend analogy: a gRPC service method / a @PostMapping REST endpoint.
Real-world: robots expose services like "enable motors", "clear costmap",
"reset odometry" — one-off commands that return an answer (not streams).

Service type: std_srvs/srv/SetBool
  Request : bool data
  Response: bool success, string message
"""
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class RobotPowerServer(Node):
    def __init__(self):
        super().__init__('robot_power_server')
        self.active = False

        # create_service(srv_type, service_name, callback)
        #  ≈ registering an endpoint: @PostMapping("/set_robot_active")
        #    / gRPC service method / http.HandleFunc("/set_robot_active", handle)
        self.srv = self.create_service(SetBool, 'set_robot_active', self.handle)
        self.get_logger().info('service ready: /set_robot_active (SetBool)')

    def handle(self, request, response):     # ≈ the controller/handler method
        # 'request' and 'response' are the typed objects ROS hands you.
        self.active = request.data
        response.success = True
        response.message = f'robot is now {"ACTIVE" if self.active else "IDLE"}'
        self.get_logger().info(
            f'request: data={request.data} -> "{response.message}"')
        return response                       # ≈ return the ResponseEntity / gRPC reply


def main(args=None):
    rclpy.init(args=args)
    node = RobotPowerServer()
    try:
        rclpy.spin(node)      # spin = serve requests until Ctrl-C (like a running HTTP server)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
