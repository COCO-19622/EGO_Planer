"""Convert PX4 NED/FRD odometry and Gazebo depth for EGO Planner."""

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from nav_msgs.msg import Odometry
from px4_msgs.msg import VehicleOdometry
from sensor_msgs.msg import Image


def multiply(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    )


class Px4EgoBridge(Node):
    def __init__(self):
        super().__init__('px4_ego_bridge')
        self.odom_pub = self.create_publisher(Odometry, '/ego/odom', 10)
        self.depth_pub = self.create_publisher(Image, '/ego/depth', 10)
        self.latest_odom = None
        self.create_subscription(
            VehicleOdometry, '/fmu/out/vehicle_odometry',
            self.on_odometry, qos_profile_sensor_data)
        self.create_subscription(
            Image, '/depth_camera', self.on_depth, 10)

    def on_odometry(self, source):
        if source.pose_frame != VehicleOdometry.POSE_FRAME_NED:
            self.get_logger().warn('PX4 odometry is not NED; cannot convert it', throttle_duration_sec=5.0)
            return
        values = list(source.position) + list(source.q) + list(source.velocity)
        if not all(math.isfinite(x) for x in values):
            return

        odom = Odometry()
        odom.header.stamp = self.get_clock().now().to_msg()
        odom.header.frame_id = 'world'
        odom.child_frame_id = 'base_link'
        # NED (north, east, down) to ENU (east, north, up).
        odom.pose.pose.position.x = float(source.position[1])
        odom.pose.pose.position.y = float(source.position[0])
        odom.pose.pose.position.z = -float(source.position[2])

        # Body FRD to FLU, followed by world NED to ENU.
        half = math.sqrt(0.5)
        q = multiply((0.0, half, half, 0.0), source.q)
        q = multiply(q, (0.0, 1.0, 0.0, 0.0))
        norm = math.sqrt(sum(v * v for v in q))
        odom.pose.pose.orientation.w = float(q[0] / norm)
        odom.pose.pose.orientation.x = float(q[1] / norm)
        odom.pose.pose.orientation.y = float(q[2] / norm)
        odom.pose.pose.orientation.z = float(q[3] / norm)

        if source.velocity_frame == VehicleOdometry.VELOCITY_FRAME_NED:
            odom.twist.twist.linear.x = float(source.velocity[1])
            odom.twist.twist.linear.y = float(source.velocity[0])
            odom.twist.twist.linear.z = -float(source.velocity[2])
        elif source.velocity_frame == VehicleOdometry.VELOCITY_FRAME_BODY_FRD:
            odom.twist.twist.linear.x = float(source.velocity[0])
            odom.twist.twist.linear.y = -float(source.velocity[1])
            odom.twist.twist.linear.z = -float(source.velocity[2])
        else:
            self.get_logger().warn('Unsupported PX4 velocity frame', throttle_duration_sec=5.0)
            return

        self.latest_odom = odom
        self.odom_pub.publish(odom)

    def on_depth(self, source):
        if self.latest_odom is None:
            return
        # Stamp the image and odometry together for EGO's approximate synchronizer.
        stamp = self.get_clock().now().to_msg()
        depth = Image()
        depth.header = source.header
        depth.header.stamp = stamp
        depth.header.frame_id = 'camera_depth_optical_frame'
        depth.height = source.height
        depth.width = source.width
        depth.encoding = source.encoding
        depth.is_bigendian = source.is_bigendian
        depth.step = source.step
        depth.data = source.data
        odom = self.latest_odom
        odom.header.stamp = stamp
        self.odom_pub.publish(odom)
        self.depth_pub.publish(depth)


def main(args=None):
    rclpy.init(args=args)
    node = Px4EgoBridge()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
