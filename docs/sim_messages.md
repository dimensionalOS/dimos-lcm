# Physical truth, measurements and commands

All quantities use SI units and right-handed axes. World Z is up. A pose is
world-from-body, XYZ metres and an XYZW unit quaternion. A body ID names a rigid
frame in the resolved model. A joint ID names a scalar degree of freedom; these
are different identifiers. A model revision identifies the static scene.

## Acquisition identity

`common_msgs.SampleHeader` contains `clock_id`, `epoch`, `time_ns`, `source_id`,
`sequence`, and `frame_id`. `time_ns` is acquisition time in the named clock,
never publication or receipt time. Simulation uses a unique clock ID per run,
starts at zero, and increments epoch on reset/placement. Hardware may use the
`unix` clock; an empty clock denotes unknown time. A zero time in a named clock
is valid. Sequence is monotonic within a source/epoch; retransmission preserves it.

Compare timestamps only within the same clock and epoch. Receivers reject older
epochs; a new clock requires an explicit new binding. Interpolation and histories
must never cross reset boundaries. Generated codecs preserve integers as int64
(Python int / TypeScript bigint); the application enforces ordering and meaning.

## Contracts

| Message | Contents | Meaning |
|---|---|---|
| `sim_msgs.BodyPoses` | header, model_revision, BodyPose[] | One complete absolute pose for each declared rigid frame, including stationary frames, at one acquisition. Any sample is independently usable. No deltas, joint coordinates, sensor readings or solver checkpoint. |
| `sim_msgs.BodyMotion` | header with frame_id, pose_world, world linear/angular velocity, world linear acceleration, gravity_world | Kinematic truth **at that frame's origin**. Linear acceleration includes free fall; it is not accelerometer specific force. |
| `sensor_msgs.JointState` | header, name[], position[], velocity[], effort[] | On joint_truth: selected physical coordinates. On joint_state: an encoder's measurements; unavailable effort is empty. The topic/source distinguishes truth from measurement. |
| `sensor_msgs.Imu` | header, orientation, angular velocity, linear acceleration, covariances | Sensor-frame gyro and specific force `R_world_sensorᵀ (a_world - gravity_world)`; orientation availability follows the covariance flag. Produced by an IMU model, never the physics module. |
| `sensor_msgs.Image`, `CameraInfo`, `PointCloud2` | acquisition header and existing payload fields | Sensor acquisition. Rolling cloud header is scan-start time; per-point offsets describe the ray times. |
| `geometry_msgs.TransformStamped` | acquisition header, child ID, transform | Transform at acquisition time; TF must share the clock/epoch of sensor data. |
| `control_msgs.JointCommand` | header, based_on_time_ns, apply_at_ns, valid_until_ns, JointTarget[] | Explicit desired position, velocity, kp, kd, feedforward per named joint. Atomic validation; no measured state masquerading as commands. |
| `control_msgs.BodyWrench` | header, body_id, apply_at_ns, valid_until_ns, world force/torque/application point | Physical force and torque at a specified world point, held for the indicated simulation interval. |
| `sim_msgs.SimulationClock` | header, dt_ns, status, detail | Owner timing/status. Does not establish reliable delivery of other streams. |

Joint control applies `tau = kp*(q_des-q) + kd*(dq_des-dq) + feedforward`
on every physics tick, subject to model limits. Zero gains mean direct effort.
Commands are accepted only for their clock/epoch and valid interval. A configured
synchronous controller must answer its exact acquisition boundary. Expiry holds
current position; a controller deadline fault pauses physics until explicit reset.

`BodyPoses` readers validate revision, completeness, duplicate IDs, finite numbers
and unit rotations before applying a sample. Missing transport samples do not
require replay: the next complete sample replaces the scene. Sensor histories
still detect gaps because rolling acquisition cannot invent missed motion.

There is no `Frame`, `WorldState`, `Observations`/`Actions` byte envelope or
`ControlValues` conversion in this contract. Old unrelated messages in the repo
are not removed. These schemas deliberately change the affected sensor/TF wire
fingerprints: all publishers, consumers and Desktop must use the companion revision.

## Verification

```sh
nix develop --command bash generate.sh
python -m unittest discover -s tests -v
deno test --allow-read tests/test_sim_messages.ts
```

Python/TypeScript share wire fixtures, including integers beyond JavaScript's safe
number range. Generation also validates the Rust crate. The DimOS tests separately
verify physical meaning, acquisition timing, control expiry and reset behavior.
