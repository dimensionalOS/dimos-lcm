# Option E: complete physical state and typed commands

`sim_msgs.WorldState` is one complete acquisition. Its `SampleHeader` and
`model_revision` apply to every nested record. It contains:

- `BodyPose[] body_poses`: every described rigid body's absolute world pose.
- `BodyMotion[] body_motion`: motion at every configured frame origin.
- `JointTruth joint_truth`: named scalar positions, velocities and available efforts.
- `CborExtension[] extensions`: all current optional entity properties in the export.

Each snapshot replaces the previous snapshot. A missing extension does not retain
its earlier value. Stationary bodies remain present. The message contains neither
sensor measurements nor a native solver checkpoint. Array-count fields are wire
metadata and must agree with the arrays they describe.

Positions use metres, angles radians, right-handed world axes with Z up. Poses are
world-from-body with XYZW unit quaternions. Linear/angular velocity and linear
acceleration are in world axes at the named frame origin. Linear acceleration
includes free fall; an IMU computes sensor-frame specific force from acceleration
minus gravity. Body IDs identify rigid frames; joint IDs identify scalar DOFs.

## Acquisition identity

`common_msgs.SampleHeader` contains `clock_id`, `epoch`, `time_ns`, `source_id`,
`sequence`, and `frame_id`. `time_ns` is acquisition time in the named clock,
never publication or receipt time. Simulation has a unique clock ID per run,
starts at zero, and increments epoch on reset/placement. Sequence is monotonic
within a source/epoch; retransmission preserves it. Nested physical records share
this one header. Ordinary sensor messages carry their own acquisition header.

Compare times only within a clock and epoch. Old-epoch data cannot satisfy a
post-reset control boundary. Generated codecs preserve int64 values, including
values above JavaScript's safe integer range (TypeScript uses bigint).

## Optional properties

`CborExtension` contains `entity_id`, `key`, `schema`, `value_length`, and `value`.
The entity ID is a resolved body/joint name or `world`; `(entity_id, key)` must
be unique in the snapshot. `schema` is a versioned property contract, such as
`example.thermal.v1`. `value` encodes exactly one CBOR value conforming to it.

Unknown optional schemas may be ignored without losing typed physical fields.
A consumer requiring an extension must check its schema and availability; CBOR
encoding alone does not establish units or semantics. Extensions carry data,
not commands, entity discovery, controller readiness or clock signals. Each
backend's `read_extensions()` supplies its current values; the MuJoCo backend
has no optional properties to report and returns an empty list.

## Commands and measurements

`control_msgs.JointCommand` carries acquisition identity, `based_on_time_ns`,
`apply_at_ns`, `valid_until_ns`, and `JointTarget[]`. Each target names a joint
and specifies desired position/velocity, kp, kd and feedforward effort:

```text
tau = kp * (q_des - q) + kd * (dq_des - dq) + feedforward
```

`control_msgs.BodyWrench` carries acquisition identity, body ID, validity times,
and world-axis force/torque/application point. These remain separate typed
commands. There is no generic action batch in Option E.

Independent sensor modules read WorldState and produce `sensor_msgs.Imu`,
`JointState`, `Image`/`CameraInfo`, and `PointCloud2`. `SimulationClock` is a
separate execution-status message. Sensor/TF acquisition headers introduced by
this draft require matching publisher/consumer codecs; this revision does not
change those sensor message fingerprints again.

## Verification

```sh
nix develop --command bash generate.sh
python -m unittest discover -s tests -v
deno test --allow-read tests/test_sim_messages.ts
```

Python/TypeScript use shared wire fixtures for full state, large clock values,
optional extensions, and joint command validity. Generation also checks Rust.
DimOS tests cover physical meaning, complete snapshot replacement, reset,
control timing and independently acquired sensor outputs.
