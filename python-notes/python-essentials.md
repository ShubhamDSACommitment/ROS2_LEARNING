# Python Essentials — for a Java / Go engineer

Only the Python we actually use in ROS 2. Each section: the Python, then "you already know this as."

---

## 0. The two things that feel weird coming from Java/Go
1. **No braces — indentation defines blocks.** The colon `:` starts a block; the indentation (4 spaces) *is* the `{ }`.
   ```python
   def main():
       if x > 0:
           print("positive")   # this line is "inside" the if because it's indented
   ```
2. **Dynamically typed.** You don't declare types. `x = 5` then `x = "hi"` is legal. Type hints (`msg: String`) are *optional documentation*, not enforced like Java/Go.

---

## 1. Files, modules, packages
- A `.py` file = a **module** (≈ a Java class file / a Go file).
- A folder with an `__init__.py` = a **package** (≈ a Java package / Go package). `__init__.py` is usually empty; it just marks "this folder is importable."
- We saw this: `hello_ros/` folder + `__init__.py` = the importable package; `hello_node.py` = a module in it.

## 2. Imports
```python
import rclpy                      # import whole module      → Java: import rclpy.*  / Go: import "rclpy"
from rclpy.node import Node       # import one name          → Java: import rclpy.node.Node
from std_msgs.msg import String   # import a type
```
`from X import Y` pulls `Y` into scope so you write `Node`, not `rclpy.node.Node`.

## 3. Variables & `None`
```python
count = 0            # no type, no 'var'/'int'
name = "robot_1"
result = None        # None ≈ Java null / Go nil
```

## 4. Functions
```python
def main(args=None):          # 'def' = function. args has a DEFAULT value (None).
    return 42                 # optional
```
- **Default arguments:** `args=None` means callers can omit it → `main()` or `main(x)`. (Java: method overloading; Go: no equivalent, you'd pass explicitly.)
- **Keyword arguments:** you can call `create_timer(1.0, callback)` or by name. Common in Python libs.

## 5. Classes, `__init__`, `self`
```python
class RobotStatusPublisher(Node):        # class ... (Node) = inherits Node  (Java: extends, Go: embeds)
    def __init__(self):                  # __init__ = the CONSTRUCTOR
        super().__init__('name')         # call parent constructor (Java: super(...))
        self.count = 0                   # self.count = an instance field (Java: this.count)

    def tick(self):                      # a METHOD — note 'self' is EXPLICIT (Java 'this' is implicit)
        self.count += 1
```
- **`self`** = Java `this` / Go receiver — but you must write it as the **first parameter of every method** and to access every field/method (`self.count`, `self.tick()`).
- **`__init__`** = the constructor (the `__x__` "dunder" names are Python's built-in hooks).
- No `new` keyword — you construct by calling the class (below).

## 6. Creating objects (no `new`)
```python
node = RobotStatusPublisher()   # Java: new RobotStatusPublisher()
msg = String()                  # Java: new String()  → then set fields:
msg.data = "hello"
```

## 7. Passing functions (callbacks) — important for ROS
```python
self.create_timer(1.0, self.publish_status)   # pass the METHOD ITSELF, no ()
```
`self.publish_status` (no parentheses) is a **reference** to the method; ROS calls it later.
- Java: a method reference `this::publishStatus`.
- Go: passing a func value `f := p.publishStatus`.
- With `()` it would *call it now* and pass the result — a common bug.

## 8. f-strings (string formatting)
```python
msg.data = f'heartbeat {self.count} battery {100 - n}%'
```
The `f'...'` lets you embed `{expressions}` inline.
- Java: `String.format("heartbeat %d", count)` or text blocks.
- Go: `fmt.Sprintf("heartbeat %d", count)`.

## 9. Exceptions
```python
try:
    rclpy.spin(node)
except KeyboardInterrupt:   # catch a specific exception   (Java: catch, Go: no exceptions)
    pass                    # 'pass' = do nothing / empty body
finally:
    node.destroy_node()     # always runs (Java finally)
```
`pass` is the empty statement (Java `{}` / Go empty block). Go has no exceptions (uses error returns), so this is more Java-like.

## 10. The `if __name__ == '__main__':` idiom
```python
def main(args=None):
    ...

if __name__ == '__main__':   # "if this file is run directly (not imported)"
    main()
```
≈ Java `public static void main(String[] args)` — the entry point when the file is executed directly. (When imported as a module, this block does NOT run.)

## 11. Docstrings & comments
```python
"""This triple-quoted string at the top of a file/function is a DOCSTRING (auto-docs)."""
# this is a normal comment  → Java/Go: //
```

## 12. Lists & dicts (we use these in scenarios/configs)
```python
robots = ["robot_1", "robot_2"]      # list      → Java List / Go slice []string
robots.append("robot_3")
pose = {"x": 1.0, "y": 2.0}          # dict      → Java Map / Go map[string]float64
print(pose["x"])
for r in robots:                     # for-each  → Java for(:), Go for range
    print(r)
```

## 13. pip & virtual environments (just enough)
- `pip` = Python's package manager (≈ Maven/Gradle deps / `go get`).
- On Ubuntu 24.04, global `pip` is blocked — use apt packages or a **venv** (`python3 -m venv .venv`). For ROS, we mostly rely on ROS-provided packages + apt, so you rarely need pip.

---

## The 10-second summary
- Indentation = braces. `:` starts a block.
- `self` = explicit `this`, first param of every method.
- `__init__` = constructor; construct with `ClassName()` (no `new`).
- Pass `self.method` (no `()`) to hand off a callback.
- `f'{x}'` = string interpolation.
- `if __name__ == '__main__': main()` = the entry point.
