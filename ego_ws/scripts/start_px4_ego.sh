#!/usr/bin/env bash
set -euo pipefail

systemctl --user start px4-ego-sim.service
systemctl --user start px4-ego-planner.service
systemctl --user start px4-ego-control.service
systemctl --user start px4-ego-rviz.service

systemctl --user --no-pager --plain list-units \
  px4-ego-sim.service \
  px4-ego-planner.service \
  px4-ego-control.service \
  px4-ego-rviz.service
