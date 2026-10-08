#!/usr/bin/env bash
set -eo pipefail
source /opt/ros/humble/setup.bash
source /home/lzk/ego_ws/install/setup.bash
source /home/lzk/px4_ego/install/setup.bash
exec ros2 launch ego_planner px4_sitl_ego.launch.py
