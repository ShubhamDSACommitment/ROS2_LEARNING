# Code Walkthrough — `robot_status_publisher.py` (the Python only)

Same file from Lesson 03, annotated for **Python syntax** (not the ROS meaning — that's in the lesson note). Read alongside [python-essentials.md](python-essentials.md).

```python
import rclpy                          # (1) import a whole module
from rclpy.node import Node           # (2) import ONE name (the Node class) from a module
from std_msgs.msg import String       # (2) import the String message type


class RobotStatusPublisher(Node):     # (3) define a class that INHERITS Node
                                      #     Java: class RobotStatusPublisher extends Node
    def __init__(self):               # (4) the CONSTRUCTOR. 'self' = this, always 1st param.
        super().__init__('robot_status_publisher')   # (5) call parent (Node) constructor

        self.pub = self.create_publisher(String, 'robot/status', 10)
                                      # (6) self.pub = ...  → assign an INSTANCE FIELD (this.pub)
                                      #     right side calls a method inherited from Node
        self.count = 0                # (6) another instance field, int

        self.timer = self.create_timer(1.0, self.publish_status)
                                      # (7) pass self.publish_status WITHOUT ()  → a callback reference
                                      #     Java: this::publishStatus   Go: p.publishStatus (func value)

        self.get_logger().info('publishing on topic: robot/status')  # (8) method-chaining, like Java

    def publish_status(self):         # (9) a METHOD (self is explicit). ROS calls this every 1.0s.
        self.count += 1               #     += works like Java/Go
        msg = String()                # (10) construct an object → Java: new String()
        msg.data = f'robot_1 | heartbeat {self.count} | battery {max(0, 100 - self.count)}%'
                                      # (11) f-string: {..} is interpolated. max(...) is a built-in.
                                      #      set the .data field on the msg object
        self.pub.publish(msg)         # (12) call a method on our field
        self.get_logger().info(f'published: "{msg.data}"')


def main(args=None):                  # (13) a module-level function; args defaults to None (null)
    rclpy.init(args=args)
    node = RobotStatusPublisher()     # (14) construct our object (no 'new')
    try:                              # (15) try/except/finally == try/catch/finally
        rclpy.spin(node)
    except KeyboardInterrupt:         #      catch Ctrl-C
        pass                          #      'pass' = empty body
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':            # (16) run main() only when this file is executed directly
    main()                            #      == Java public static void main
```

## The Python-only cheat, keyed to the numbers
1–2. **imports** → Java `import`.
3. **`class X(Base)`** → inheritance (`extends`).
4. **`__init__`** → constructor. **`self`** → `this`, but written explicitly everywhere.
5. **`super().__init__(...)`** → parent constructor call.
6. **`self.x = ...`** → instance field assignment.
7. **`self.method`** (no `()`) → a **callback reference**; with `()` it would call immediately (bug).
8. **method chaining** → same as Java.
9. **method** → `def name(self, ...)`.
10. **`String()`** → object construction, no `new`.
11. **f-string** → `f'{expr}'` interpolation (Java `String.format`, Go `fmt.Sprintf`).
12. **`.publish(msg)`** → normal method call.
13. **default arg** `args=None` → optional parameter.
14. construct instance.
15. **try/except/finally** → try/catch/finally; **`pass`** → empty body.
16. **`__main__` guard** → the entry point.

Once these 16 patterns feel natural, every ROS 2 Python node reads the same way — the rest is just which ROS methods you call.
