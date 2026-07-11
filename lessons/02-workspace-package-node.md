# Lesson 02 — Workspace, Package & Node

**Goal:** understand how ROS 2 code is organized and run, by building the smallest real package.

## The four ideas

1. **Workspace** — a folder where you develop + build ROS 2 packages. Convention: a `ros2_ws/` with a `src/` inside. You put packages in `src/`; `colcon` builds them into `build/`, `install/`, `log/` (all gitignored).

2. **Package** — the unit of ROS 2 code (one feature/library/set of nodes). Ours is `hello_ros`. Every Python package needs:
   ```
   src/hello_ros/
   ├── package.xml            # manifest: name, deps, build_type
   ├── setup.py               # build + entry_points (executables)
   ├── setup.cfg              # where executables get installed
   ├── resource/hello_ros     # empty marker so ROS indexes the package
   └── hello_ros/             # the actual Python module
       ├── __init__.py        # makes it a Python package (empty)
       └── hello_node.py      # our node
   ```

3. **Executable** — a runnable command produced from a Python function via `entry_points` in `setup.py`:
   ```python
   'console_scripts': ['hello = hello_ros.hello_node:main']
   ```
   → `ros2 run hello_ros hello` runs `hello_node.py::main()`.

4. **Node** — a program built on `rclpy`. Pattern (see `hello_node.py`):
   `rclpy.init()` → create `Node` subclass → `rclpy.spin(node)` (process callbacks/timers) → `destroy_node()` + `rclpy.shutdown()`.

## Colcon — the build tool
`colcon build` reads each package's `package.xml` + `setup.py`, builds them, and produces an `install/` "overlay." You then **source** that overlay so ROS can find your package:
```
build → source install/setup.bash → run
```
Forgetting the `source` step is the #1 beginner error ("package not found").

## ▶ Run on Ubuntu
```bash
# 0) get the latest code
cd <your ROS2_LEARNING>            # e.g. ~/ROS2_LEARNING
git pull

# 1) source ROS 2, go to the workspace
source /opt/ros/jazzy/setup.bash
cd ros2_ws

# 2) build
colcon build
#   (first build also creates build/ install/ log/ — all gitignored)

# 3) source YOUR workspace overlay (so ROS finds hello_ros)
source install/setup.bash

# 4) run the node
ros2 run hello_ros hello
```
**Expected:** `[INFO] [hello_node]: hello_node has started`, then once per second `[INFO] [hello_node]: hello ROS 2 — tick N`.

**Inspect it (second terminal):**
```bash
source /opt/ros/jazzy/setup.bash
source <...>/ros2_ws/install/setup.bash
ros2 node list        # /hello_node
ros2 node info /hello_node
```

## Common errors
- `Package 'hello_ros' not found` → you forgot `source install/setup.bash` (step 3).
- `No executable found` → the `entry_points` name in `setup.py` doesn't match what you `ros2 run`.
- build error about `rclpy` → make sure ROS 2 is sourced (step 1) before `colcon build`.

## Takeaways
- Code lives in **packages** inside a **workspace** `src/`.
- `setup.py` `entry_points` turn functions into **executables**.
- Lifecycle: **build → source → run**.
- A **node** = `rclpy.init` → `Node` → `spin` → `shutdown`.

**Next → Lesson 03: Topics** — make this node *publish*, and write a second node that *subscribes*.
