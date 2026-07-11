# Lesson 01 — The ROS 2 Mental Model

**The one idea:** ROS 2 is a way to build robot software as **many small programs (nodes) that talk over a shared "graph."** You don't write one big program — you write nodes that publish and subscribe.

## Core concepts

| Concept | What it is | Everyday analogy | WareFleet use |
|---|---|---|---|
| **Node** | one program doing one job | one microservice | `agent_node`, fleet manager bridge |
| **Topic** | named channel; **publish/subscribe**; many-to-many; async | a radio station | robot publishes `RobotState`; subscribes `TaskAssignment` |
| **Message** | typed data on a topic | the JSON schema | `Task`, `RobotState` (Lesson 02) |
| **Service** | request → response; synchronous | a function call / REST | used sparingly |
| **Action** | long-running goal + feedback + cancel | "navigate there, tell me when done" | Nav2 `NavigateToPose` (Lesson 06) |
| **Parameter** | a config value a node reads at startup | env var / config file | `robot_id` (Lesson 04) |
| **DDS** | the pub/sub transport underneath | the wiring; auto-discovery | (automatic — no central master) |

**Key mental note:** there is **no master/roscore** in ROS 2. Nodes discover each other automatically via DDS.

## 🔧 For a Go / Java / backend engineer
ROS 2 is essentially a **distributed-microservices + message-bus framework**. Map it to what you know:

| ROS 2 | Java / Spring | Go | ⚠️ leak |
|---|---|---|---|
| Node | a Spring Boot service (1 process, 1 job) | a `package main` binary | it's a process, not a class |
| Topic (pub/sub) | JMS/Kafka topic — or **MQTT (Addverb!)** | network channel + broker | default fire-and-forget, **no persistence/replay** (≈ MQTT QoS 0) |
| Message (`.msg`) | DTO/record; `.msg` ≈ **`.proto`** | `struct`; `.msg` ≈ `.proto` | an IDL that code-gens typed classes |
| Service | gRPC unary / REST endpoint | `net/rpc` handler | synchronous request→response |
| Action | `CompletableFuture` + progress + cancel | goroutine + `context` + progress chan | long job: goal→feedback→result, cancelable |
| Parameter | `@Value` / `application.yml` | flags / env / Viper | per-node startup config |
| DDS | Eureka/Consul discovery + broker | same, peer-to-peer | **decentralized — no master** |
| `ros2` CLI | Actuator / `kubectl` / `kafka-console-consumer` | same | inspect the live system from outside |

## The ROS graph
At runtime, the live set of nodes + the topics/services/actions connecting them = the **ROS graph**. You inspect it from *outside* any node with the `ros2` CLI (`ros2 node`, `ros2 topic`, ...). This is how you debug.

## ▶ Run on Ubuntu (feel pub/sub — no files needed)
Three terminals, each first: `source /opt/ros/jazzy/setup.bash`

```bash
# Terminal A — a publisher
ros2 run demo_nodes_py talker

# Terminal B — a subscriber
ros2 run demo_nodes_py listener

# Terminal C — inspect the live graph
ros2 node list                 # /talker  /listener
ros2 topic list                # /chatter
ros2 topic echo /chatter       # watch the raw messages
ros2 topic info /chatter        # 1 publisher, 1 subscriber
ros2 node info /talker          # what it publishes/subscribes
ros2 topic hz /chatter          # publish rate
```
*(If `demo_nodes_py` is missing: `sudo apt install ros-jazzy-demo-nodes-py`.)*

**Expected:** A prints `Publishing: 'Hello World: N'`; B prints `I heard: ...`; C lets you watch the topic from outside — that's the whole pub/sub model.

## Takeaways
- Build software as nodes, not one monolith.
- Topics = streams (pub/sub); services = calls; actions = long tasks.
- Debug by inspecting the graph with `ros2 ...` from another terminal.

**Next → Lesson 02:** define our own message types (custom messages).
