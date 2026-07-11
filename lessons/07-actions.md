# Lesson 07 — Actions (long-running goals)

**The idea:** an **action** is for a task that takes a while and where you want **live progress** and the ability to **cancel**. Three parts: **Goal** (the request), **Feedback** (progress stream), **Result** (final answer).

Topic = stream. Service = quick call. **Action = long job.**

## 🔧 For a Go / Java engineer
| ROS 2 action | Java | Go |
|---|---|---|
| the action | gRPC **server-streaming** call / an async job API | goroutine + `context` + progress chan + result |
| Goal | the job submission (`POST /jobs`) | the job struct |
| Feedback | progress events (SSE / WebSocket) | `progressCh <- p` |
| Result | the final return | `resultCh <- r` / return |
| cancel | `future.cancel()` | `ctx.cancel()` |
| accepted/rejected | `202 Accepted` vs `409` | server decides |

The client flow is the same shape as an **async REST job**: submit → get accepted → stream progress → fetch result.

## The demo (this package)
- `fib_server` → action **`compute_fibonacci`**: computes N terms, publishing one per second as feedback, then the full result. (Stand-in for any long task.)
- `fib_client [order]` → sends a goal, prints feedback as it streams, then the result.

## ▶ Run on Ubuntu
```bash
# one-time: the Fibonacci action type
sudo apt install ros-jazzy-action-tutorials-interfaces

cd <your ROS2_LEARNING> && git pull
source /opt/ros/jazzy/setup.bash
cd ros2_ws && colcon build && source install/setup.bash

ros2 run actions_demo fib_server        # terminal A
ros2 run actions_demo fib_client 8      # terminal B
```
**Expected:** B prints `goal ACCEPTED`, then `feedback: [0,1,1]`, `[0,1,1,2]`, … once per second, then `RESULT: [...]`.

**Use the CLI as a client (no code):**
```bash
ros2 action list
ros2 action info /compute_fibonacci
ros2 action send_goal /compute_fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 8}" --feedback
```

## 🌍 Real world — this IS how Nav2 works
`NavigateToPose` (Nav2's main interface) is an action:
- **Goal** = target pose (x, y, θ)
- **Feedback** = distance remaining / current pose / estimated time
- **Result** = succeeded / failed
That's why "drive to X" is an action, not a service: it takes time, you want progress, and you must be able to cancel/preempt. See [../references/nav2-fundamentals.md](../references/nav2-fundamentals.md).

**WareFleet:** the fleet manager assigns a robot a destination → the robot's agent calls `NavigateToPose` on its Nav2 → feedback tells the manager how far along it is → on failure, recover or reassign.

## Note on cancel + threading
With the default single-threaded executor, a blocking `time.sleep` in the server's `execute` delays cancel handling. For instantly responsive cancel, use a `MultiThreadedExecutor` + callback groups (advanced — not needed to learn the pattern).

## Takeaways
- Action = long job with Goal → Feedback (stream) → Result, cancelable.
- Server: `ActionServer(..., execute_cb)`; client: `ActionClient` → `send_goal_async` (+ feedback cb) → goal handle → `get_result_async`.
- Nav2's `NavigateToPose` is exactly this pattern.

**Next → Lesson 08: TF2** (coordinate frames) and **Lesson 09: RViz** (visualize it all) to finish the Level 1 foundation.
