"""Lesson 08 — a TF2 LISTENER.

Looks up where 'base_link' is relative to 'map' and logs it. A listener does
NOT subscribe to the broadcaster directly — it queries the TF buffer, which
composes the whole frame chain for you (map->odom->base_link->...).
"""
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class FrameListener(Node):
    def __init__(self):
        super().__init__('tf_listener')
        self.buffer = Buffer()                                 # the time-stamped transform cache
        self.listener = TransformListener(self.buffer, self)   # fills the buffer from /tf
        self.timer = self.create_timer(1.0, self.tick)

    def tick(self):
        try:
            # lookup_transform(target_frame, source_frame, time)
            #  "give me source expressed in target, at this time"
            #  rclpy.time.Time() (=0) means "latest available"
            t = self.buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
            x = t.transform.translation.x
            y = t.transform.translation.y
            self.get_logger().info(f'base_link is at map ({x:+.2f}, {y:+.2f})')
        except TransformException as e:
            self.get_logger().info(f'waiting for transform map->base_link: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
