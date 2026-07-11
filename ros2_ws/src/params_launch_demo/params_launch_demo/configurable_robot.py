"""Lesson 05 — a node configured by PARAMETERS.

Parameters = a node's config values (like Spring @Value / application.yml,
or Go flags/Viper). You DECLARE them (with defaults), then READ them.
They can be set at launch, from a YAML file, from the CLI, or changed at runtime.

This robot publishes its (draining) battery on 'robot/status' at a configurable
rate, and warns when battery drops below a configurable threshold.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ConfigurableRobot(Node):
    def __init__(self):
        super().__init__('configurable_robot')

        # declare_parameter(name, default)  ≈ @Value("${robot_id:robot_0}")
        self.declare_parameter('robot_id', 'robot_0')
        self.declare_parameter('publish_rate_hz', 1.0)
        self.declare_parameter('battery_warn', 20)

        # read the values  ≈ config.getString("robot_id")
        self.robot_id = self.get_parameter('robot_id').value
        rate = self.get_parameter('publish_rate_hz').value
        self.battery_warn = self.get_parameter('battery_warn').value

        self.battery = 100
        self.pub = self.create_publisher(String, 'robot/status', 10)
        period = 1.0 / rate if rate and rate > 0 else 1.0
        self.timer = self.create_timer(period, self.tick)

        self.get_logger().info(
            f'[{self.robot_id}] started | rate={rate}Hz | warn<{self.battery_warn}%')

    def tick(self):
        self.battery = max(0, self.battery - 1)
        msg = String()
        msg.data = f'{self.robot_id} | battery {self.battery}%'
        self.pub.publish(msg)
        if self.battery <= self.battery_warn:
            self.get_logger().warn(f'[{self.robot_id}] LOW BATTERY {self.battery}%')
        else:
            self.get_logger().info(f'[{self.robot_id}] battery {self.battery}%')


def main(args=None):
    rclpy.init(args=args)
    node = ConfigurableRobot()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
