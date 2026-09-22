# MTRN4231-Resource

Useful teaching resource for MTRN4231.

## Lab 2 — Demo Prep (Transformations & Client-Service)

Prep material for introducing Lab 2: transformations, TF2 trees, and the
client-service relationship.

- `notes/lab2_intro_walkthrough.md` — talking points and live demo script
  for the lab introduction.
- `notes/rviz_debug_checklist.md` — handout for students on debugging TF2
  with `tf2_echo`, `view_frames`, and RViz2.
- `ros2_ws/src/tf2_demo/` — runnable ROS 2 (Humble) package: broadcasts a
  camera mount transform, simulates a detected target in the camera frame,
  and looks up that target relative to the robot's `base_link`. Verified to
  build and run on this machine.

### Run it

```bash
cd ~/mtrn4231/ros2_ws
colcon build --packages-select tf2_demo
source install/setup.bash
ros2 launch tf2_demo tf2_demo.launch.py
```

Opens RViz with the TF tree and both the camera-frame and base_link-frame
target points displayed (red vs. green sphere).
