"""EGO Planner for the local PX4 gz_x500_depth SITL simulation."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    advanced = os.path.join(
        get_package_share_directory('ego_planner'),
        'launch', 'advanced_param.launch.py')

    return LaunchDescription([
        Node(package='tf2_ros', executable='static_transform_publisher',
             name='world_to_map', output='screen',
             arguments=['0', '0', '0', '0', '0', '0', 'world', 'map']),
        Node(package='px4_ego_py', executable='px4_ego_bridge',
             name='px4_ego_bridge', output='screen'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(advanced),
            launch_arguments={
                'drone_id': '0',
                'odometry_topic': '/ego/odom',
                'depth_topic': '/ego/depth',
                'cloud_topic': '/lidar_points',
                'flight_type': '1',
                'max_vel': '0.8',
                'max_acc': '1.0',
                'planning_horizon': '7.5',
            }.items()),
        Node(
            package='ego_planner', executable='traj_server',
            name='drone_0_traj_server', output='screen',
            remappings=[
                ('position_cmd', '/drone_0_planning/pos_cmd'),
                ('planning/bspline', '/drone_0_planning/bspline'),
            ],
            parameters=[{'traj_server/time_forward': 1.0}]),
    ])
