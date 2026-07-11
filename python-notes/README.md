# Python Notes (for a Go / Java engineer)

I'm learning ROS 2 in **Python (rclpy)** but my background is **Java, Spring, Go**. These notes explain the Python I need — mapped to what I already know — so the language never blocks the robotics.

| Note | What it covers |
|---|---|
| [python-essentials.md](python-essentials.md) | The core Python I use: imports, classes, `self`, `__init__`, inheritance, functions, callbacks, f-strings, exceptions, the `__main__` idiom, lists/dicts — each vs. Java/Go |
| [code-walkthrough.md](code-walkthrough.md) | Our `robot_status_publisher.py`, explained line-by-line — but only the **Python** (not the ROS) |

> Rule of thumb: Python is dynamically typed, uses **indentation instead of braces**, and `self` is just an explicit `this`. Almost everything else maps 1:1 to Java/Go.
