# Lesson 09 — RViz2 (visualization)

**The idea:** RViz2 is ROS 2's **3D viewer/debugger**. It subscribes to topics + TF and *draws* them — robot model, laser scans, maps, planned paths, TF frames, markers. It is (mostly) **read-only**: a window into the running ROS graph, not part of the robot's logic.

## 🔧 For a Go / Java engineer
RViz = your **observability dashboard for 3D state** — think Grafana, but for geometry, or a debugger's visualizer. It's just another **subscriber** that renders what other nodes publish. It never *drives* the robot (except the two manual tools below); turning it off changes nothing about how the robot behaves. Same mental model as `ros2 topic echo`, but visual.

## ▶ Try it on Ubuntu — visualize the TF demo from Lesson 08
```bash
source /opt/ros/jazzy/setup.bash
cd <your ROS2_LEARNING>/ros2_ws && source install/setup.bash

ros2 run tf2_demo broadcaster        # terminal A (keep running)
rviz2                                 # terminal B
```
In the RViz window:
1. Set **Fixed Frame** (top-left, Global Options) to **`map`**.
2. Click **Add** (bottom-left) → **By display type** → **TF** → OK.
3. You'll see the `map` and `base_link` frames — watch `base_link` **circle** the map in real time.

That's the whole loop: a node publishes state → RViz draws it. Everything else in RViz is just more display types (LaserScan, Map, Path, RobotModel, MarkerArray).

## 🌍 Real world — RViz + Nav2
RViz is where you actually *use* a navigating robot. With a Nav2 sim running:
```bash
ros2 launch nav2_bringup tb3_simulation_launch.py   # brings up Nav2 + sim robot + RViz
```
In RViz you: click **"2D Pose Estimate"** to tell AMCL where the robot starts, then **"Nav2 Goal"** to send a destination — and watch the **global path** appear, the **costmaps** shade obstacles, and the robot drive while the local plan updates. This is the single best way to *see* everything from Lessons 1–8 working together (nodes + topics + TF + the `NavigateToPose` action).

*(The "2D Pose Estimate" and "Nav2 Goal" buttons are the rare cases where RViz publishes — it sends a pose/goal topic. Otherwise it only reads.)*

## Takeaways
- RViz2 = read-only 3D dashboard; a subscriber that draws the ROS graph.
- Set **Fixed Frame**, then **Add** display types (TF, LaserScan, Map, Path, RobotModel).
- With Nav2: set initial pose + goal in RViz and watch it plan + drive — the capstone view of the whole stack.

**🎉 That completes Level 1.** You now understand nodes, topics, services, actions, parameters, launch, packages/colcon, TF2, and RViz — and how Nav2 composes them. Next: apply it in WareFleet.
