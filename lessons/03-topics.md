# Lesson 03 — Topics (Publish / Subscribe)

**The idea:** a **topic** is a named channel. A **publisher** sends messages to it; any number of **subscribers** receive them. Publisher and subscriber are **decoupled** — neither knows the other exists. Async, many-to-many, fire-and-forget.

If you've used Kafka or MQTT, you already know this model.

## 🔧 For a Go / Java engineer
| ROS 2 | Java / Spring | Go |
|---|---|---|
| topic (`robot/status`) | Kafka/MQTT topic | broker topic / channel |
| `create_publisher(String, 'robot/status', 10)` | `KafkaTemplate<String>` for a topic | a producer |
| `pub.publish(msg)` | `producer.send(topic, msg)` / MQTT `publish()` | `producer.Publish(...)` |
| `create_subscription(String, 'robot/status', cb, 10)` | `@KafkaListener(topics="robot/status")` | consumer + handler |
| the callback `on_status(msg)` | the `@KafkaListener` handler method | the message handler func |
| queue_depth `10` (QoS history) | producer/consumer buffer; QoS ≈ Kafka acks / MQTT QoS | channel buffer size |
| decoupling (pub doesn't know subs) | same — that's the point of a broker | same |

**Leak to remember:** ROS topics default to *no persistence/replay* (like MQTT QoS 0). A subscriber only gets messages published *while it's running* — there's no Kafka-style offset/replay unless you configure "transient local" QoS.

## The demo (this package)
- `robot_status_publisher.py` → publishes `robot_1 | heartbeat N | battery %` on **`robot/status`** at 1 Hz (the producer).
- `status_monitor.py` → subscribes to `robot/status`, logs each message (the consumer — like the fleet manager).

## ▶ Run on Ubuntu
```bash
cd <your ROS2_LEARNING> && git pull
source /opt/ros/jazzy/setup.bash
cd ros2_ws && colcon build && source install/setup.bash

# terminal A — producer
ros2 run topics_demo status_pub
# terminal B — consumer
ros2 run topics_demo status_monitor
```
**Expected:** A logs `published: "robot_1 | heartbeat 1 ..."`; B logs `received: "..."` in lockstep.

**Inspect from outside (terminal C) — this is the real superpower:**
```bash
ros2 topic list                    # /robot/status
ros2 topic echo /robot/status      # watch messages live (like kafka-console-consumer)
ros2 topic info /robot/status -v   # publishers, subscribers, QoS
ros2 topic hz /robot/status        # publish rate (~1 Hz)
# you can even publish by hand (no code):
ros2 topic pub /robot/status std_msgs/String '{data: "manual test"}'
```

## 🌍 What a REAL node looks like (not the toy)
On an actual robot, **dozens of nodes run at once**, wired entirely by topics. A typical mobile robot:

```
[lidar_driver] --/scan-->            [nav2]  --/cmd_vel-->  [base_controller] --> wheels
[camera]       --/image-->             ^                         ^
[imu]          --/imu-->               |                         |
[localization] --/amcl_pose-----------/         (subscribes /scan, /amcl_pose; publishes /cmd_vel)
```
- **Hardware driver nodes** publish sensor data (`/scan` = `sensor_msgs/LaserScan`, `/image`, `/imu`).
- **Perception/localization nodes** consume sensors, publish estimates (`/amcl_pose`).
- **Planning/control nodes** (Nav2) consume those, publish velocity commands (`/cmd_vel` = `geometry_msgs/Twist`).
- **Base/motor node** subscribes `/cmd_vel`, drives the wheels.

So topics are the **wiring diagram** of the robot. A real node differs from our toy by:
- **typed, structured messages** (`LaserScan`, `Twist`) not `String`;
- **tuned QoS** (sensor data uses "best effort" like UDP; commands use "reliable");
- **multiple pubs/subs** in one node, plus parameters, error handling, and lifecycle.

Our `robot_status_publisher` is exactly the shape of a real **telemetry** node — and it maps directly to **WareFleet**: each robot's agent publishes `RobotState` (position, battery, status); the fleet manager subscribes to all of them (and we also bridge to MQTT — the same pub/sub idea on your Addverb-style bus).

## ❓ How is a topic "created"?
You never explicitly create it. A topic exists the moment a node references its name in a publisher/subscriber:
```python
self.create_publisher(String, 'robot/status', 10)   # the string 'robot/status' IS the topic
```
DDS auto-advertises + discovers it — there is no `admin.createTopic()`. This is like **MQTT** (implicit topics), *unlike* **Kafka** (pre-created partitions). Consequences:
1. **Name is the contract** — publisher & subscriber must use the *identical* string or they never connect (silent, no error).
2. **Type must match** (`String` both sides).
3. **QoS must be compatible** (the `10` / reliability settings).

## Common errors
- B receives nothing → topic name mismatch (must be identical string) or B started after A finished (no replay by default).
- `colcon build` can't find `std_msgs` → ROS 2 not sourced before building.

## Takeaways
- Topic = broker channel; publisher = producer; subscriber = consumer + handler.
- `spin()` on the subscriber = the consumer poll loop.
- Real robots are **graphs of nodes wired by topics** — inspect any wire with `ros2 topic echo`.

**Next → Lesson 04: Services** — synchronous request/response (a gRPC/REST call), for "do X now and answer me," vs. topics' continuous streams.
