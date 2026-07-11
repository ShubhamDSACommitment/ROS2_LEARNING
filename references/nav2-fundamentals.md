# Nav2 Fundamentals

**What it is:** Nav2 (Navigation2) is the ROS 2 **navigation stack** — the batteries-included system that takes a mobile robot from **A to B autonomously**, planning a route and avoiding obstacles. You don't write navigation from scratch; you configure Nav2 and call it.

**The big realization:** Nav2 is **everything you learned in Level 1, composed** — a set of **nodes** (L2) wired by **topics** (L3) + **services** (L4), configured by **parameters** (L5), started by a **launch file** (L6), and driven through an **action** (L7).

## How you talk to it: actions
- `NavigateToPose` — go to a single goal pose. **Goal** = pose (x,y,θ); **Feedback** = distance remaining / ETA; **Result** = success/failure.
- `NavigateThroughPoses`, `FollowWaypoints` — multi-point routes.
This is exactly the action pattern from Lesson 07.

## What Nav2 needs (inputs)
| Input | From | Topic / form |
|---|---|---|
| a **map** | static file or SLAM | `/map` (occupancy grid) |
| the robot's **pose** on the map | localization (**AMCL**) | `/amcl_pose`, TF `map→odom` |
| **sensor** data | LiDAR driver | `/scan` (`LaserScan`) |
| a **TF tree** | robot_state_publisher + odom | `map→odom→base_link→sensors` (Lesson 08) |
| a **goal** | you / the fleet manager | the `NavigateToPose` action |
| **velocity** out | Nav2 → base | `/cmd_vel` (`Twist`) |

## Core components (each is a node/"server")
```
        goal pose (action)
              │
      ┌───────▼─────────┐
      │  BT Navigator   │  ← the "brain": a Behavior Tree that orchestrates everything,
      └───┬─────────┬───┘    and runs recoveries when stuck
          │         │
   ┌──────▼───┐ ┌───▼────────┐
   │ Planner  │ │ Controller │
   │ server   │ │ server     │
   │ (global  │ │ (local     │
   │  route:  │ │  follow +  │
   │  A*/Smac)│ │  avoid:    │
   └────┬─────┘ │  DWB/MPPI) │
        │       └────┬───────┘
   global costmap  local costmap      ← map + inflated obstacle "danger" zones
        │              │
        └───► /cmd_vel ─┴──► base drives the wheels
```
- **Map server** — serves the static `/map`.
- **AMCL** — localizes the robot on the map (particle filter).
- **Costmaps** (global + local) — the map annotated with obstacle inflation; planning avoids high-cost cells.
- **Planner server** — computes the global path (the "GPS route": A*/Dijkstra/Smac).
- **Controller server** — follows the path while dodging dynamic obstacles (the "steering": DWB/MPPI).
- **Behavior Tree navigator** — the state machine that calls planner→controller and, when stuck, triggers **recovery behaviors** (spin, back up, wait, clear costmap).
- **Recoveries / smoother / collision monitor / velocity smoother** — supporting servers.

## The flow (one navigation)
goal pose → BT Navigator → Planner computes a path on the global costmap → Controller follows it, reacting to the local costmap → publishes `/cmd_vel` → base moves → **feedback** (distance remaining) streams back → **result** success/failure. If stuck → recovery behavior → retry.

## 🔧 For a Go / Java engineer
Nav2 = a **microservices system for navigation**. You call it like an **async job API** (submit a goal pose → stream progress → get result). Internally it's a **pipeline** (planner → controller) with a **state machine** (the behavior tree) orchestrating and handling failures — very much a workflow-engine pattern. Its config is one big `application.yml` (the Nav2 params YAML, often hundreds of keys).

## Services it exposes (occasional commands)
`/clear_entirely_global_costmap`, `/clear_entirely_local_costmap`, lifecycle transitions, etc. — one-off commands (Lesson 04), not streams.

## Try it (later, with RViz — Lesson 09)
```bash
ros2 launch nav2_bringup tb3_simulation_launch.py    # brings up Nav2 + a sim robot + RViz
# in RViz: set a "2D Pose Estimate", then "Nav2 Goal" — watch it plan + drive
```

## WareFleet mapping
Each robot runs **its own Nav2 stack**. The **fleet manager** decides *where* each robot goes and hands the pose to the robot's agent, which calls `NavigateToPose`. Nav2 handles the *single-robot* "how do I get there safely"; WareFleet adds the *fleet* layer on top (who goes where, and multi-robot deconfliction). We deliberately **do not** reinvent Nav2 — it's the per-robot autonomy we build the fleet logic around.

## One-line summary
> Nav2 = configure-don't-code single-robot autonomy, exposed as an action, built from nodes+topics+services+params+launch — i.e., all of Level 1 assembled into a real system.
