# State machine for state management and ego planner trajectory command publish
```
git clone https://github.com/DongnanHu6556/px4_ego.git
cd px4_ego
source /opt/ros/humble/setup.bash
# Source the workspace that provides px4_msgs if it is built separately.
source ~/ws_ros2/install/setup.bash
colcon build
source install/setup.bash
ros2 interface show quadrotor_msgs/msg/PositionCommand
ros2 run px4_ego_py offboard_control_test
```
Run the `source install/setup.bash` command in the **same terminal** used for
`ros2 run`, including after adding or rebuilding `quadrotor_msgs`. An earlier
terminal session may still know about `px4_ego_py` but lack the new message
package on `PYTHONPATH`. Check with:

```
python3 -c 'from quadrotor_msgs.msg import PositionCommand; print(PositionCommand)'
```

The included `quadrotor_msgs` package provides the `PositionCommand` interface
used by [ego-swarm-ros2](https://github.com/DongnanHu6556/ego-swarm-ros2).
When running the planner from a separate workspace, source its `install/setup.bash`
as well, and check that `/drone_0_planning/pos_cmd` has type
`quadrotor_msgs/msg/PositionCommand` with `ros2 topic type`.
The state machine runs in munual control at first. Then we can use keyboard to switch different states:

```
cd px4_ego
python3 mode_key.py 
```
- 't' means "takeoff"
- 'p' means "hover at current position (position mode)"
- 'o' means "switch to offboard mode. (If there is no trajectory command, it will return to position mode)"
- 'l' means "land"
- 'd' means "disarm"
When you input 't', the drone will auto takeoff.
<img width="1830" height="1042" alt="takeoff_screenshot" src="https://github.com/user-attachments/assets/883905a2-4168-4a9b-98cc-df09a062ec74" />
