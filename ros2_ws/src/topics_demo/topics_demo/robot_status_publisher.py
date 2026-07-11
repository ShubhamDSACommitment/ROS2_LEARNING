"""Lesson 03 — a PUBLISHER (producer).

Think: a robot broadcasting its status heartbeat every second.
Backend analogy: a Kafka/MQTT PRODUCER sending to a topic.
Real-world analogy: a robot's onboard node publishing telemetry that the
fleet manager (and dashboards) consume — exactly WareFleet's RobotState.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String     # a built-in message type (just a text field)


class RobotStatusPublisher(Node):
    def __init__(self):
        super().__init__('robot_status_publisher')

        # create_publisher(msg_type, topic_name, queue_depth)
        #  ≈ KafkaTemplate<String> bound to topic "robot/status"
        #  queue_depth (10) = QoS history depth ≈ the producer buffer:
        #    how many recent msgs to keep if a subscriber is momentarily slow.
        self.pub = self.create_publisher(String, 'robot/status', 10)

        self.count = 0
        self.timer = self.create_timer(1.0, self.publish_status)   # ≈ @Scheduled(fixedRate=1000)
        self.get_logger().info('publishing on topic: robot/status')

    def publish_status(self):
        self.count += 1
        msg = String()                                             # ≈ new DTO
        msg.data = f'robot_1 | heartbeat {self.count} | battery {max(0, 100 - self.count)}%'
        self.pub.publish(msg)                                      # ≈ producer.send(topic, msg)
        self.get_logger().info(f'published: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = RobotStatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
