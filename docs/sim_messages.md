# Option G: one body state and one action input

`sim_msgs.WorldState` is one complete acquisition. Its `SampleHeader` and
`model_revision` apply to every nested record. It contains:

- `BodyState[] bodies`: every described body/frame with `pose: Pose`, `twist: Twist` and `acceleration: Accel`.
- `JointState joint_truth`: named scalar positions, velocities and available efforts.
- `CborObservation[] cbor_observations`: all current optional entity properties in the export.

Each snapshot replaces the previous snapshot. A missing extension does not retain
its earlier value. Stationary bodies remain present. The message contains neither
sensor measurements nor a native solver checkpoint. Array-count fields are wire
metadata and must agree with the arrays they describe.

Positions use metres, angles radians, right-handed world axes with Z up. Poses are
world-from-body with XYZW unit quaternions. Linear/angular velocity and linear/angular
acceleration are in world axes at the named frame origin. Linear acceleration
includes free fall; an IMU computes sensor-frame specific force from acceleration
minus configured gravity. Body IDs identify rigid frames; joint IDs identify scalar DOFs.

One BodyState replaces the overlapping BodyPose/BodyMotion records. Gravity is
fixed scene configuration, delivered to the IMU at startup, never repeated in the
WorldState payload. Every body exports all kinematic fields. BodyState, WorldState, ActionCommand and both CBOR types have new
wire fingerprints relative to F; there is no mixed-codec compatibility.

## Acquisition identity

`common_msgs.SampleHeader` contains `clock_id`, `epoch`, `time_ns`, `source_id`,
`sequence`, and `frame_id`. `time_ns` is acquisition time in the named clock,
never publication or receipt time. Simulation has a unique clock ID per run,
starts at zero, and uses epoch zero for one blueprint run. A fresh episode uses
`dimos restart`; in-place episode reset is not exposed by SimModule. Sequence is
monotonic within a source; retransmission preserves it. Nested physical records
share this acquisition. The nested `joint_truth.header` retains std_msgs.Header
and encodes the same acquisition time as the outer header. Ordinary sensor and TF
messages retain their upstream std_msgs.Header definitions and fingerprints.
Their source is selected by blueprint stream wiring, rather than a new wire field.

Compare times only within one run clock. A restarted blueprint creates new
module instances, sensor histories and controller bindings. Commands addressed
to an old run clock are rejected. Generated codecs preserve int64 values, including
values above JavaScript's safe integer range (TypeScript uses bigint).

## Optional properties

`CborObservation` contains `entity_id`, `key`, `value_length`, and `value`.
The entity ID is a resolved body/joint name or `world`; `(entity_id, key)` must
be unique in the snapshot. The key identifies the property and its agreed payload
format. `value` encodes exactly one CBOR value; there is no separate schema field.

Unknown optional keys may be ignored without losing typed physical fields.
A consumer requiring an extension must check its key, payload and availability; CBOR
encoding alone does not establish units or semantics. Extensions carry data,
not commands, entity discovery, controller readiness or clock signals. Each
backend's `read_cbor_observations()` supplies its current values; the MuJoCo backend
has no optional properties to report and returns an empty list.

## One action input

`actions: In[control_msgs.ActionCommand]` accepts:

```text
header: common_msgs.SampleHeader
based_on_time_ns: int64
apply_at_ns: int64
valid_until_ns: int64
joint_commands_length: int32
joint_commands: control_msgs.JointCommand[]
cbor_commands_length: int32
cbor_commands: control_msgs.CborCommand[]
```

At least one entry is required. The whole batch uses one source, sequence, clock,
epoch and time window. `based_on_time_ns` identifies the measurement used to choose
it. `apply_at_ns` is the earliest application time; `valid_until_ns` is exclusive.
A backend validates all entries before changing state. Unknown CBOR operations
reject the whole action; they cannot be silently ignored like optional observations.
An accepted source/sequence is not executed again in the same epoch.

Each `JointCommand` names a joint and specifies desired position/velocity, kp, kd
and feedforward effort:

```text
tau = kp * (q_des - q) + kd * (dq_des - dq) + feedforward
```

Targets persist until expiry, when SimModule holds those joints. A registered
controller must answer its exact current measurement boundary with its full joint
set. CBOR-only actions cannot satisfy that motor-control boundary.

`CborCommand` has `entity_id: string`, `key: string`,
`value_length: int32`, `value: byte[]`. It carries exactly one CBOR item, addressed
to a known body/joint or `world`; `(entity_id,key)` is unique within the action.
The addressed key defines operation semantics, payload format and effect lifetime. Execution is once at
acceptance, not every physics step; expiry does **not** undo CBOR effects. No wrench
command is defined. The included MuJoCo backend implements joint targets and rejects
all CBOR commands; a backend can implement specific operations through `apply_action`
without changing SimModule. There is no generic execution or operation registry.

`control_msgs.JointCommand` now names the six-field PD/feedforward record approved
for G. This is name parity with ROS terminology, not the upstream ROS message
layout; bindings using that upstream layout must not be mixed with these codecs.

Independent sensor modules read WorldState and produce `sensor_msgs.Imu`,
`JointState`, `Image`/`CameraInfo`, and `PointCloud2`. Execution status is available
through SimModule's `status()` RPC. This revision restores the existing sensor/TF
wire contracts; SampleHeader remains specific to WorldState and ActionCommand.

## Verification

```sh
nix develop --command bash generate.sh
python -m unittest discover -s tests -v
deno test --allow-read tests/test_sim_messages.ts
```

Python/TypeScript use shared wire fixtures for full state, large clock values,
optional extensions, joint targets, CBOR commands and action validity. Generation also checks Rust.
DimOS tests cover physical meaning, complete snapshot replacement, reset,
control timing and independently acquired sensor outputs.
