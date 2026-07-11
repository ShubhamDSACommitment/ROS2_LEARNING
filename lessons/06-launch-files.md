# Lesson 06 — Launch files

**The idea:** a **launch file** is a script that says *which nodes to start and with what config* — so `ros2 launch` boots your whole system in one command. You never `ros2 run` a dozen nodes by hand.

## 🔧 For a Go / Java engineer
A launch file is the **deployment descriptor**:
| ROS 2 launch | You know it as |
|---|---|
| a `.launch.py` file | `docker-compose.yml` / a K8s manifest / a set of `systemd` units |
| `Node(package=, executable=, ...)` | one service/container definition |
| `parameters=[{...}]` | that service's env/config block |
| `namespace='robot_0'` | a prefix/namespace so instances don't collide |
| `LaunchDescription([...])` | the full compose file (all services) |
| `ros2 launch pkg file.launch.py` | `docker compose up` |

In ROS 2, launch files are **Python** (`launch` + `launch_ros`) — so they can loop, branch, read args (unlike static YAML).

## The two demos (this package)
- `robot.launch.py` → starts **one** `configurable_robot`, params `robot_id=robot_A, rate=2Hz, warn<30%`.
- `fleet.launch.py` → **loops** to start **3 robots**, each in its own **namespace** (`/robot_0`, `/robot_1`, `/robot_2`) with its own params. This is exactly how WareFleet will spawn a fleet.

## ▶ Run on Ubuntu
```bash
cd <your ROS2_LEARNING> && git pull
source /opt/ros/jazzy/setup.bash
cd ros2_ws && colcon build && source install/setup.bash

# one configured robot
ros2 launch params_launch_demo robot.launch.py

# a fleet of three (each namespaced + configured)
ros2 launch params_launch_demo fleet.launch.py
```
**Expected (fleet):** interleaved logs `[robot_0] battery 99%`, `[robot_1] battery 99%`, … and later `LOW BATTERY` warnings. Inspect:
```bash
ros2 node list          # /robot_0/configurable_robot, /robot_1/..., /robot_2/...
ros2 topic list         # /robot_0/robot/status, /robot_1/robot/status, ...
ros2 param get /robot_0/configurable_robot robot_id
```

## 🌍 Real world
A real robot's bringup launch starts drivers + localization + Nav2 + everything, wired with dozens of params — one `ros2 launch`. Nav2's `bringup_launch.py` is the canonical example. Launch files can also **include** other launch files (compose of composes), pass **launch arguments** (`DeclareLaunchArgument`), and set namespaces/remappings.

## Takeaways
- Launch file = deployment descriptor (docker-compose for ROS).
- Python-based → can loop/branch (see `fleet.launch.py`).
- `namespace` keeps multiple instances of the same node from colliding.
- `ros2 launch pkg file.launch.py` = `docker compose up`.

**Next → Lesson 07: Actions** — long-running goals with feedback + cancel (the right tool for "drive to X", vs. a service).
