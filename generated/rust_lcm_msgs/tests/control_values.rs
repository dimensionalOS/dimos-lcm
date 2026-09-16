use lcm_msgs::dimos_control_msgs::ControlValues;

#[test]
fn control_values_matches_python_wire_fixture() {
    // Same Python-generated golden bytes as the Python and TypeScript tests.
    let hex = concat!(
        "31b3ec9631ab499f00000003636300405ee000000000001000000000000003",
        "100000000000000400000001000000010000000e626173652f6c696e6561725f78003fe0000000000000"
    );
    let payload: Vec<u8> = (0..hex.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
        .collect();
    let expected = ControlValues {
        source: "cc".into(),
        source_ts: 123.5,
        epoch: (1_i64 << 60) + 3,
        sequence: (1_i64 << 60) + 4,
        interface_names: vec!["base/linear_x".into()],
        values: vec![0.5],
    };

    assert_eq!(ControlValues::decode(&payload).unwrap(), expected);
    assert_eq!(expected.encode(), payload);
}

#[test]
fn empty_control_values_round_trip() {
    let expected = ControlValues::default();
    assert_eq!(ControlValues::decode(&expected.encode()).unwrap(), expected);
}

#[test]
fn truncated_control_values_are_rejected() {
    let mut payload = ControlValues::default().encode();
    payload.pop();
    assert!(ControlValues::decode(&payload).is_err());
}
