#!/usr/bin/env bash
set -eo pipefail
source /opt/ros/humble/setup.bash
source /home/lzk/px4_ros_uxrce_dds_ws/install/setup.bash
source /home/lzk/ego_ws/install/setup.bash
source /home/lzk/px4_ego/install/setup.bash
export DISPLAY=:0
cd /home/lzk/PX4-Autopilot
exec ros2 launch /home/lzk/PX4-Autopilot/launch/px4_sitl_ros2.launch.py
