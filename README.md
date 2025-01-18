# skillit

A package that lets you chef up new skills for KOS-compatible robots

> ⚠️ **Warning**  
 This package is under development and currently only supports joint playback.

## Installation

```bash
pip install skillit
```

## Setup
```bash
pip install -e ".[dev]"
```

See the [examples](examples) directory for examples of how to use skillit.

To quickly get your robot standing in place, take the following steps:

1. Record a standing position using the record functionality:
```bash
python examples/play_record_example.py record --ip YOUR_ROBOT_IP --skill-name standing
```

2. When prompted, physically move your robot into a stable standing position. The process will be:
   - Press Ctrl+C to start recording
   - Hold the robot steady in the standing position for a few seconds
       - Note that *all* actuators will be disabled, so it will be completely limp
   - Press Ctrl+C again to stop recording

3. Play back the recorded standing position:
```bash
python examples/play_record_example.py play --ip YOUR_ROBOT_IP --file standing.json
```

This will create a basic standing skill that you can use as a foundation for more complex movements. See the [examples](examples) directory for more advanced skill demonstrations.
