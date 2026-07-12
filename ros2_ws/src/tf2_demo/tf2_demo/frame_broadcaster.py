"""Lesson 08 — a TF2 BROADCASTER.

Publishes the transform map -> base_link as a robot drives in a circle.
TF2 answers "where is frame X relative to frame Y at time T?"; a broadcaster
is what PUBLISHES one edge of that frame tree, timestamped, on /tf.
"""
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class FrameBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.br = TransformBroadcaster(self)          # publishes on /tf
        self.t = 0.0
        self.timer = self.create_timer(0.1, self.tick)  # 10 Hz
        self.get_logger().info('broadcasting map -> base_link')

    def tick(self):
        self.t += 0.1

        tf = TransformStamped()
        tf.header.stamp = self.get_clock().now().to_msg()  # WHEN (time matters in TF)
        tf.header.frame_id = 'map'            # parent frame
        tf.child_frame_id = 'base_link'       # child frame (the robot)

        # position: drive in a 2 m circle
        tf.transform.translation.x = 2.0 * math.cos(self.t)
        tf.transform.translation.y = 2.0 * math.sin(self.t)
        tf.transform.translation.z = 0.0

        # orientation: face along the motion (yaw -> quaternion, z/w only)
        yaw = self.t + math.pi / 2.0
        tf.transform.rotation.z = math.sin(yaw / 2.0)
        tf.transform.rotation.w = math.cos(yaw / 2.0)

        self.br.sendTransform(tf)             # publish this edge of the frame tree


def main(args=None):
    rclpy.init(args=args)
    node = FrameBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
