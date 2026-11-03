# Simulation scene and action messages

`sim_msgs` is independent of the experimental `world_msgs` change stream.
These generated messages define encoding, not change suppression or a simulator.

`Observations` identifies one run, model revision, reset epoch and simulation tick.
`sim_time` is simulation seconds; `ts` is Unix publication seconds. Epochs increase
on reset/placement; ticks restart at zero. A new simulator process gets a new run
ID and requires rebinding its description. Compare `(epoch, tick)` only within
that bound run/model. Wall timestamps are not ordering or synchronization proofs.

An entity ID identifies a body/frame in the resolved model, not a whole articulated
robot or an actuator. `POSE` is an absolute world-from-body pose, with XYZ metres
and unit XYZW quaternion in a right-handed, Z-up world. `frame_id` is `world` in
V1. The payload is the existing generated `geometry_msgs.Pose` encoding including
its fingerprint. Articulated robots publish each link's pose. Readers do not need
joint coordinates or simulator checkpoints to place geometry.

`complete=true` requires exactly one pose for every declared body, including
stationary bodies. A reader can start with any such sample and recover from a
dropped sample with the next one. Validate the whole batch before replacing state;
reject duplicate/missing/unknown body poses, nonfinite values and invalid rotations.
`complete=false` reserves subset semantics: absence means no observation, never
removal. The initial DimOS reader rejects subsets rather than treating them as a
complete world. Entity creation/removal requires a new model description/revision.

`CBOR` is an optional extension with a producer-owned versioned `schema` identifier.
It cannot replace required poses. Unknown optional observation kinds can be skipped
using their payload length. Future standardized kinds get new identifiers; do not
change the meaning of an existing kind. Changing the outer LCM schema still changes
its fingerprint; nested payloads make new kinds possible without changing that schema.

`Actions` is separate from observation and scene editing. Its initial `JOINT_COMMAND`
payload is generated `JointCommand`: named arrays of desired position, velocity,
kp, kd and feedforward effort. The backend applies
`tau = kp*(position-q) + kd*(velocity-dq) + effort` each physics tick, subject to model
limits. Zero gains give direct effort. These fields are not measured JointState.
Unknown action kinds reject the entire batch. Validate all entries before changing
any actuator. TTL is simulation seconds; `tick=-1` requests unpaced control, otherwise
the action answers a particular feedback tick. These stamps do not implement safety,
authorization or expiry by themselves; the owner enforces them.

Robot joint/IMU feedback uses the existing `control_msgs.ControlValues` contract,
bound to the same run and model outside the message. Camera/lidar outputs remain
ordinary sensor messages. The scene observations are not images or point clouds.

Cross-language checks: `python -m unittest discover -s tests -v` and
`deno test --allow-read tests/test_sim_messages.ts`. Both consume the same golden
wire fixtures, including an epoch larger than JavaScript's safe integer range.
