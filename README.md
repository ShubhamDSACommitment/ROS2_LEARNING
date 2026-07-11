# ROS2_LEARNING

My hands-on sandbox for learning **ROS 2 Jazzy** (Ubuntu 24.04), the fundamentals I need for the [WareFleet](https://github.com/ShubhamDSACommitment/warefleet) project — multi-robot warehouse fleet orchestration.

> Learning method: I **author + understand** each lesson (with notes here), then **run + verify on my Ubuntu machine**. Each lesson note ends with the exact commands to run and what to expect.

## Level 1 — Foundation (required)

The building blocks I must understand before building WareFleet. Each lesson = one repo commit + a "run on Ubuntu" check. Language: **Python (rclpy)**.

| # | Lesson | Covers | Status |
|---|---|---|---|
| 01 | [Mental model](lessons/01-mental-model.md) | nodes · topics · services · actions · parameters · DDS · the graph | ✅ |
| 02 | [Workspace, package & node](lessons/02-workspace-package-node.md) | **workspace · package structure · colcon · executables · Nodes** | ✅ |
| 03 | [Topics](lessons/03-topics.md) | publisher + subscriber | ✅ |
| 04 | Services | server + client | ⏳ |
| 05 | Parameters | node configuration | ⏳ |
| 06 | Launch files | start many nodes at once | ⏳ |
| 07 | Actions | long-running goals (Nav2 `NavigateToPose`) | ⏳ |
| 08 | TF2 (basics) | coordinate frames / transforms | ⏳ |
| 09 | RViz | visualize the robot & data | ⏳ |

**Skipped for now** (not needed yet): lifecycle nodes, components, QoS deep-dives, rosbag.

> Foundation first. Once Level 1 is solid, we apply it in the [WareFleet](https://github.com/ShubhamDSACommitment/warefleet) project.

## Python notes (no prior Python experience)
Since I come from Java/Go, [`python-notes/`](python-notes/) explains the Python we use, mapped to what I already know:
- [python-essentials.md](python-notes/python-essentials.md) — classes, `self`, imports, callbacks, f-strings… vs Java/Go
- [code-walkthrough.md](python-notes/code-walkthrough.md) — a node explained line-by-line (Python only)

## Layout
```
lessons/        # one markdown note per concept (theory + run-on-Ubuntu commands)
ros2_ws/        # colcon workspace with the example packages we build (added per lesson)
```

## How to run a lesson (on Ubuntu 24.04 / ROS 2 Jazzy)
```bash
source /opt/ros/jazzy/setup.bash
# then follow the "Run on Ubuntu" block in each lesson note
```
