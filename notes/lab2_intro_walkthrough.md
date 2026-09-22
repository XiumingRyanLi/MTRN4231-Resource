# Lab 2 Intro Walkthrough — Transformations, Services, and TF2

Context: this lab covers transformations and the client-service relationship.
Use the `tf2_demo` package (`../ros2_ws/src/tf2_demo`) as the live demo.
Run it with:

```bash
cd ~/mtrn4231/ros2_ws
colcon build --packages-select tf2_demo
source install/setup.bash
ros2 launch tf2_demo tf2_demo.launch.py
```

This brings up three nodes and RViz:

- `camera_broadcaster` — publishes a **static** transform `base_link -> camera_link`
  (camera mounted 0.3m forward, 0.4m up, tilted 20° down).
- `target_publisher` — simulates a vision pipeline: publishes a `PointStamped`
  in `camera_link`, drifting in a small circle (stand-in for "the object
  detector found something at this pixel, and we've converted it to a 3D
  point in the camera's own frame").
- `target_locator` — the actual point of the demo. It uses a `tf2_ros.Buffer`
  + `TransformListener` to transform that point into `base_link`, and
  republishes it. No manual matrix math.

## Why we care about TF2 (say this at a user level)

- Every sensor and every part of the robot has its own natural reference
  frame. A camera reports "the target is at this pixel / this point in front
  of my lens." A gripper needs "how far do I move my joints." Those are
  different frames.
- TF2 keeps a **tree** of frames (`base_link -> camera_link`, and normally
  also `base_link -> arm links -> end effector`, `odom -> base_link`, etc.),
  each edge being a transform that can be static (bolted-on hardware) or
  dynamic (a moving joint, or robot odometry).
- Because it's a tree, you never hand-chain transforms yourself. Ask tf2 for
  "camera_link -> base_link" (or any frame to any frame) and it walks the
  tree and composes it for you, including at a specific timestamp. This is
  the point to hammer: **you ask a question ("where is X relative to Y right
  now?"), you don't compute the answer**.
- This is also *why* client-service fits in the same lab: looking up a
  transform is conceptually a request/response (or request-a-buffer-then-
  query) pattern, and later they'll build actual `client<->service` calls to
  ask another node to do work (e.g. "plan a path to this pose").

## Live demo script

1. **Launch** `tf2_demo.launch.py`. Point out three terminals worth of nodes
   and RViz opening with a TF display already on.
2. In RViz, open the **TF** display's frame list and show `base_link` and
   `camera_link`. Rotate the view — the camera frame's axes visibly point
   forward-and-down, matching the 20° tilt.
3. Point out the **red** sphere (`Target (camera_link frame)`) circling in
   front of the camera — "this is what the camera sees, in its own frame."
4. Point out the **green** sphere (`Target (base_link frame)`) — same
   physical point, but now expressed relative to the robot's base. It sits
   further out and slightly higher, because the lookup accounted for the
   camera's mounting offset and tilt automatically.
5. Open a terminal and `ros2 topic echo /target_in_base_link` — read a value
   off, and cross-check it against where the green sphere sits in RViz.
   This is the "trust but verify" moment: **the number a node reports should
   always match what you can see in the frame viewer.**
6. Open `tf2_demo/target_locator.py` and show the ~5 lines that do the
   actual work: `Buffer()`, `TransformListener()`, and
   `self.tf_buffer.transform(msg, 'base_link')`. Contrast with how many
   lines of trig it would take to do this by hand for a real arm.
7. Mention `ros2 run tf2_tools view_frames` and `ros2 run rviz2 rviz2` with
   the **TFrame** display as the two standard debugging entry points for
   their own lab work (see the debug checklist).

## Bridge to the client-service part of the lab

Frame the tf2 lookup as "asking a question and getting an answer" the same
way a service call is "asking a question and getting an answer" — the
listener isn't computing the transform itself, it's asking the tf2 buffer
(which is fed by whichever node broadcasts each transform) for the answer.
That's the same request/response mental model they'll use for
`rclpy`/`rclcpp` service clients later in the lab.
