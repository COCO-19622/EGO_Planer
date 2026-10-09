#!/usr/bin/env bash
set -euo pipefail

systemctl --user stop \
  px4-ego-rviz.service \
  px4-ego-control.service \
  px4-ego-planner.service \
  px4-ego-sim.service

echo 'PX4 EGO services stopped.'
