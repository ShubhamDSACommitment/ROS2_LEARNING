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

## 🔧 For a Go / Java engineer
It's your build/runtime story with different names:

| ROS 2 | Java | Go |
|---|---|---|
| workspace (`ros2_ws/src`) | Maven/Gradle multi-module project | repo w/ multiple packages / `go.work` |
| package (`hello_ros`) | a Maven module | a Go module/package |
| `package.xml` | `pom.xml` (manifest + deps) | `go.mod` |
| `setup.py` `entry_points` | `Main-Class` / Gradle `mainClass` | `func main` in `package main` |
| `colcon build` | `mvn install` / `gradle build` | `go build ./...` |
| `source install/setup.bash` | jar on the classpath | binary on `$PATH` |
| `ros2 run hello_ros hello` | `java -jar app.jar` | `./binary` |

And the node lifecycle in `hello_node.py`:
```
class HelloNode(Node)         ≈ a @Component service class / Go service struct
super().__init__('hello_node')≈ spring.application.name — registers the service by name
create_timer(1.0, self.tick)  ≈ @Scheduled(fixedRate=1000) / Go time.Ticker + select loop
get_logger().info(...)        ≈ slf4j logger.info / log.Printf
rclpy.init()                  ≈ bootstrap the framework (build app context)
rclpy.spin(node)              ≈ SpringApplication.run() / http.ListenAndServe — the BLOCKING serve loop
destroy_node(); shutdown()    ≈ graceful shutdown / ctx.cancel()
```
**Key insight:** `spin()` is the event loop. You *register handlers* (timers, subscriptions) in the constructor, then `spin()` hands the thread to ROS to dispatch them — exactly like defining `@KafkaListener`/HTTP routes then calling the blocking `run()`/`ListenAndServe()`. No `spin()` → handlers defined but nothing ever fires.

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
