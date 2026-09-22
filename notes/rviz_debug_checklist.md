# RViz2 / TF2 Debug Checklist

Give this to students as the standard sequence for "why isn't my transform
working / is my transform even right."

## 1. Is the frame actually being broadcast?

```bash
ros2 run tf2_ros tf2_echo <source_frame> <target_frame>
# e.g.
ros2 run tf2_ros tf2_echo base_link camera_link
```

- If it prints a translation/rotation repeatedly → the transform exists and
  is live.
- If it hangs with "Could not find a connection" → nothing is publishing
  that edge of the tree yet (node not running, wrong frame name/typo, or
  wrong `frame_id`/`child_frame_id` in the broadcaster).

## 2. Does the whole tree make sense?

```bash
ros2 run tf2_tools view_frames
```

- Generates `frames.pdf` showing every frame and how recently each was
  updated. Use this to catch: disconnected frames (two separate trees that
  never join — usually a typo in a parent frame name), or a frame that
  hasn't updated in a long time (a node has died or stopped publishing).

## 3. Visual check in RViz2

- Add the **TF** display, set **Fixed Frame** (top of Global Options) to a
  stable frame (usually `base_link` or `odom`), enable **Show Names** and
  **Show Axes**.
- Confirm the frame you care about (e.g. `camera_link`) appears where you
  physically expect it, and its axes point the way you expect (red=X,
  green=Y, blue=Z). A camera frame's Z axis pointing out the lens (or X,
  depending on convention — check the sensor's REP) is the most common
  "my transform is wrong" catch.
- If you're debugging a detected target: add a **PointStamped** (or
  **Marker**) display on the topic in the source frame, and a second one on
  the topic after transforming into the target frame. They must correspond
  to the same physical point in the world — if the transformed point looks
  wrong in RViz relative to the robot model, the transform (or its
  timestamp) is wrong before you even look at code.

## 4. Timing issues

- `ExtrapolationException` almost always means you asked for a transform at
  a timestamp tf2 doesn't have data for yet/anymore. Fixes, in order of
  preference:
  - Use `rclpy.time.Time()` (i.e. "latest available") instead of a specific
    stamp, if latency doesn't matter for your use case.
  - Add a short timeout to `buffer.transform(...)` / `buffer.lookup_transform(...)`
    so it waits briefly for the frame to catch up.
  - Check your sensor node isn't stamping messages with the wrong clock
    (sim time vs wall time is the classic gotcha — check `use_sim_time`).

## 5. Sanity-check against ground truth

- If you know the physical mounting offset (like the camera in the
  `tf2_demo` package: 0.3m forward, 0.4m up, 20° tilt), pick a target at a
  known real-world position and confirm the transformed coordinates in
  `base_link` are physically plausible before trusting the pipeline for
  anything downstream (like commanding motion).

## Quick reference

| Symptom | Likely cause |
|---|---|
| `tf2_echo` hangs / "unknown frame" | Broadcaster not running, or frame name typo |
| Two frame trees in `view_frames` output | Parent frame name mismatch somewhere |
| `LookupException` | Frame simply doesn't exist / never published |
| `ConnectivityException` | Frame exists but tree has no path between the two frames requested |
| `ExtrapolationException` | Asked for a time tf2 doesn't have data for |
| RViz frame axes point the "wrong way" | Rotation set backwards, or convention mismatch (check REP-103/105) |
