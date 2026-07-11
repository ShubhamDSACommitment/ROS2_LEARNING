# Python Notes (for a Go / Java engineer)

I'm learning ROS 2 in **Python (rclpy)** but my background is **Java, Spring, Go**. These notes explain the Python I need — mapped to what I already know — so the language never blocks the robotics.

| Note | What it covers |
|---|---|
| [python-essentials.md](python-essentials.md) | The core Python I use: imports, classes, `self`, `__init__`, inheritance, functions, callbacks, f-strings, exceptions, the `__main__` idiom, lists/dicts — each vs. Java/Go |
| [code-walkthrough.md](code-walkthrough.md) | Our `robot_status_publisher.py`, explained line-by-line — but only the **Python** (not the ROS) |

> Rule of thumb: Python is dynamically typed, uses **indentation instead of braces**, and `self` is just an explicit `this`. Almost everything else maps 1:1 to Java/Go.

## ❓ Why do `rclpy` / `std_msgs` imports show RED in my IDE?
Because the IDE indexes packages **installed in the selected interpreter's environment** (Python's `site-packages` = Java's **classpath**). `rclpy` is **not installed on the Mac** — it lives only in ROS 2 on **Ubuntu** (`/opt/ros/jazzy/...`). So the Mac IDE has nothing to index → red. It's the same as opening a Java project where Maven never downloaded the JARs.

- **On the Mac:** red on ROS imports is *normal and harmless* — the code still runs on Ubuntu. Ignore those specific reds.
- **On Ubuntu (full navigation, like Java):** Settings → Python Interpreter → set `/usr/bin/python3` → open "Show paths for the selected interpreter" → `+` → add `/opt/ros/jazzy/lib/python3.12/site-packages` (verify version via `ls /opt/ros/jazzy/lib`). Now Ctrl+click into `rclpy` works.
  - Simpler: launch the IDE from a shell where `source /opt/ros/jazzy/setup.bash` was run.

**Mental model:** IDE code-intelligence = "index whatever the interpreter can `import`." No install → no index → red.
