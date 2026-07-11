"""Lesson 03 — a SUBSCRIBER (consumer).

Think: the fleet manager / a dashboard listening to every robot's status.
Backend analogy: a Kafka @KafkaListener / MQTT subscriber — a handler that
fires for each incoming message. It does NOT know or care who published.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StatusMonitor(Node):
    def __init__(self):
        super().__init__('status_monitor')

        # create_subscription(msg_type, topic_name, callback, queue_depth)
        #  ≈ @KafkaListener(topics="robot/status")   /   MQTT subscribe(...)
        #  self.on_status is the message handler ROS calls for each message.
        self.sub = self.create_subscription(
            String, 'robot/status', self.on_status, 10)
        self.get_logger().info('listening on topic: robot/status')

    def on_status(self, msg: String):        # ≈ the @KafkaListener handler method
        self.get_logger().info(f'received: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = StatusMonitor()
    try:
        rclpy.spin(node)      # spin = the consumer poll loop (blocks, dispatches callbacks)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
