#!/usr/bin/env bash
set -eo pipefail
source /opt/ros/humble/setup.bash
source /home/lzk/ego_ws/install/setup.bash
source /home/lzk/px4_ego/install/setup.bash
exec ros2 run px4_ego_py offboard_control_test --ros-args -p initial_mode:=o
