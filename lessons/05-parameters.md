# Lesson 05 — Parameters (node config)

**The idea:** a **parameter** is a named config value a node owns. You **declare** it (with a default), **read** it, and it can be set at launch, from a YAML file, from the CLI, or changed at runtime.

## 🔧 For a Go / Java engineer
| ROS 2 | Java / Spring | Go |
|---|---|---|
| parameter | `@Value` property | flag / Viper config key |
| `declare_parameter('robot_id', 'robot_0')` | `@Value("${robot_id:robot_0}")` | `flag.String("robot_id", "robot_0", ...)` |
| `get_parameter('robot_id').value` | inject the field | `viper.GetString("robot_id")` |
| a param YAML file | `application.yml` | a config file |
| `ros2 param set ... at runtime` | Actuator refresh / dynamic config | live reload |

Each parameter is **scoped to one node** — like each microservice having its own `application.yml`.

## In the code (`configurable_robot.py`)
```python
self.declare_parameter('publish_rate_hz', 1.0)      # declare with default
rate = self.get_parameter('publish_rate_hz').value  # read
```
Common params on real nodes: frame ids, topic names, rates, thresholds, file paths. **Nav2 has hundreds** of params in big YAML files.

## Four ways to set a parameter
1. **Default** — in `declare_parameter(...)`.
2. **CLI override:** `ros2 run params_launch_demo robot --ros-args -p robot_id:=cli_bot -p publish_rate_hz:=5.0`
3. **Launch file:** `parameters=[{'robot_id': 'robot_A'}]` (Lesson 06).
4. **YAML file:** `--ros-args --params-file my_params.yaml` (like pointing to `application.yml`).

## Inspect / change at runtime
```bash
ros2 param list                                   # all params of running nodes
ros2 param get /configurable_robot robot_id
ros2 param set /configurable_robot battery_warn 50   # change live
```

## Takeaways
- Parameters = per-node config (`@Value`/`application.yml`).
- `declare` (with default) → `get(...).value`.
- Set via default / CLI / launch / YAML; inspect+change with `ros2 param`.

**See Lesson 06 (Launch files)** for the cleanest way to set params for many nodes at once.
