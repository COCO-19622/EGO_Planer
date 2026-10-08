#!/usr/bin/env bash
set -eo pipefail
source /opt/ros/humble/setup.bash
source /home/lzk/ego_ws/install/setup.bash
export DISPLAY=:0
exec ros2 launch ego_planner rviz.launch.py
