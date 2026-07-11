# Lesson 04 — Services (Request / Response)

**The idea:** a **service** is a synchronous **request → response** call. One client asks, one server answers, once. The opposite of a topic (continuous stream).

If topics are Kafka/MQTT, **a service is a gRPC unary call / a REST endpoint**.

## 🔧 For a Go / Java engineer
| ROS 2 | Java / Spring | Go |
|---|---|---|
| service | a gRPC unary method / REST endpoint | an RPC handler |
| service type (`.srv`) | the request+response DTOs / `.proto` | request+response structs |
| `create_service(SetBool, 'set_robot_active', handle)` | `@PostMapping("/set_robot_active")` handler | `http.HandleFunc(...)` / gRPC method |
| the `handle(request, response)` callback | the controller method | the handler func |
| `create_client(SetBool, 'set_robot_active')` | a `WebClient` / gRPC stub | a client |
| `call_async(req)` → future | `CompletableFuture<Resp>` | a result channel |
| `spin_until_future_complete(...)` | `future.get()` (block for the reply) | `<-ch` |
| `wait_for_service(...)` | readiness/health check before calling | dial + wait |

**Key point:** the client call is logically **blocking** — you wait for the answer (via the future). So the server's `handle` must be **quick**. For long jobs (drive across the warehouse), use an **Action** (Lesson 07), not a service.

## The demo (this package)
- `power_server` → advertises **`/set_robot_active`** (`std_srvs/srv/SetBool`); flips an internal `active` flag, returns `success` + `message`.
- `power_client true|false` → calls it and prints the response.

## ▶ Run on Ubuntu
```bash
cd <your ROS2_LEARNING> && git pull
source /opt/ros/jazzy/setup.bash
cd ros2_ws && colcon build && source install/setup.bash

# terminal A — the server (leave running)
ros2 run services_demo power_server

# terminal B — call it
ros2 run services_demo power_client true
ros2 run services_demo power_client false
```
**Expected:** client prints `response: success=True message="robot is now ACTIVE"`; server logs each request.

**Call it with zero client code (the CLI is a universal client):**
```bash
ros2 service list                                  # /set_robot_active
ros2 service type /set_robot_active                # std_srvs/srv/SetBool
ros2 service call /set_robot_active std_srvs/srv/SetBool "{data: true}"
```

## 🌍 Topics vs Services — the decision that matters
| Use a **Topic** when… | Use a **Service** when… |
|---|---|
| continuous stream of data | one-off request that needs an answer |
| many-to-many, fire-and-forget | one-to-one, you want a reply |
| sensor data, `/cmd_vel`, telemetry | config, trigger, query ("enable motors", "clear costmap") |
| high frequency | occasional |

**Real robots** expose services like: `/clear_entirely_global_costmap` (Nav2), reset odometry, set a parameter, enable/disable motors, take a snapshot. Rule of thumb from your world: **topic = a Kafka stream; service = a REST/gRPC call; long job = an Action** (next lesson).

**WareFleet mapping:** mostly topics + MQTT for the continuous fleet state, but a service fits "pause/resume robot N" or "query robot N's status once" — an occasional command that expects an acknowledgement.

## Common errors
- Client hangs on "waiting for service" → server not running, or name/type mismatch.
- `handle` must `return response` — forgetting the return gives an empty/failed reply.

## Takeaways
- Service = synchronous request→response (gRPC/REST), one-to-one.
- Server = `create_service` + a handler; client = `create_client` + `call_async` + wait on the future.
- Keep handlers fast; use **Actions** for long-running goals.

**Next → Lesson 05: Parameters** — a node's config (`@Value`/`application.yml`), set at launch and changeable at runtime.
