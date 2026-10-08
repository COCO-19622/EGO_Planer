# ego-swarm-ros2

**Local PX4 simulation on this machine:** PX4/Gazebo, the planner, controller,
and RViz run as user services. Use the RViz window opened by
`px4-ego-rviz.service`. Do not run the manual simulation, planner, controller,
or RViz commands below at the same time as those services.

The repository comes from https://github.com/legubiao/ego-swarm-ros2, I revised the "qos" in grid_map.cpp and add my own ego planner launch files.
```
mkdir -p ego_ws/src
cd ego_ws/src
git clone https://github.com/DongnanHu6556/ego-swarm-ros2.git
cd ..
colcon build
```
Then you can launch the planner:
```
source install/setup.bash
ros2 launch ego_planner single_uav_gazebo.launch.py
```
Before the autonomous navigation, the drone need to takeoff and switch to offboard mode in gazebo. For specific steps, please follow the repository https://github.com/DongnanHu6556/ego-planner-ros2-sim/tree/main.

Launch rviz:
```
source install/setup.bash
ros2 launch ego_planner rviz.launch.py 
```
Use "2D Goal Pose" to publish the target.

For the local `gz_x500_depth` PX4 SITL launch (`~/PX4-Autopilot/launch/px4_sitl_ros2.launch.py`),
use the PX4-specific planner launch instead of `single_uav_gazebo.launch.py`:

```bash
source /opt/ros/humble/setup.bash
source ~/ego_ws/install/setup.bash
source ~/px4_ego/install/setup.bash
ros2 launch ego_planner px4_sitl_ego.launch.py
```

This starts the PX4 odometry/depth bridge, EGO planner, and trajectory server.
Start RViz separately with `ros2 launch ego_planner rviz.launch.py`. Take off
before selecting a goal; the planner treats the ground as an obstacle. The
offboard controller must be running and `/mode_key` set to `o` for the aircraft
to follow the planned trajectory. Check `/ego/odom`, `/ego/depth`,
`/drone_0_planning/bspline`, and `/drone_0_planning/pos_cmd` if it does not move.

On this machine, PX4/Gazebo, the planner, offboard controller, and RViz are
installed as user services. They continue running when a terminal closes and
start with the user manager. Do not start another
`offboard_control_test` process; it now accepts only one instance.

```bash
systemctl --user status px4-ego-sim px4-ego-planner px4-ego-control px4-ego-rviz
systemctl --user restart px4-ego-sim px4-ego-planner px4-ego-control px4-ego-rviz
journalctl --user -u px4-ego-sim -u px4-ego-planner -u px4-ego-control -n 50 --no-pager
```

After restarting PX4, take off and select offboard tracking mode before
publishing a new RViz goal. When the controller service restarts by itself, it
waits in offboard tracking mode but holds its current position until a fresh
planning command arrives. Old trajectory commands expire.
<img width="1831" height="958" alt="Screenshot 2026-01-01 21:21:05" src="https://github.com/user-attachments/assets/6903858b-2572-4f49-891b-d7d6409104e6" />
