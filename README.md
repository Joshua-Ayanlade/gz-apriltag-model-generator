# gz-apriltag-model-generator

Generate Gazebo (gz-sim) AprilTag models for **ROS 2 Jazzy** from the command line. Pick the tag ID, family and size as arguments, and the script creates the full model folder (`model.sdf`, `model.config` and the texture) ready to drop into a world file.


## Features

- Generates `model.sdf`, `model.config` and a sharp, upscaled texture PNG
- Tag ID, family, physical size and texture resolution set via arguments
- `--size` is the **black square edge length**, so you can use the same value directly in `apriltag_ros`
- The board size (including the white margin) is computed automatically from the tag image

## Requirements

- ROS 2 Jazzy with Gazebo Harmonic (gz-sim 8)
- Python 3
- Pillow
- The [apriltag-imgs](https://github.com/Joshua-Ayanlade/gz-apriltag-model-generator/apriltag-imgs) tag images


## Installation

```bash
# 1. Get this repose
git clone https://github.com/Joshua-Ayanlade/gz-apriltag-model-generator.git

# 2. Install Pillow
pip install pillow

# 3. Make the script executable
chmod +x gen_apriltag_model.py
```

If `pip install` complains about an externally managed environment, use `sudo apt install python3-pil` or a virtual environment.

## Usage

```bash
./gen_apriltag_model.py --id 5 --size 0.16 --tags-dir ~/apriltag-imgs --out ~/gz_models
```

This creates:

```
~/gz_models/apriltag_tag36h11_5/
├── model.config
├── model.sdf
└── materials/
    └── textures/
        └── apriltag_tag36h11_5.png
```

### Arguments

| Argument     | Required | Default    | Description                                                              |
|--------------|----------|------------|--------------------------------------------------------------------------|
| `--id`       | yes      |            | Tag ID                                                                   |
| `--size`     | no       | `0.16`     | Edge length of the **black square** in metres                            |
| `--family`   | no       | `tag36h11` | Tag family: `tag36h11`, `tag25h9`, `tag16h5`, `tagStandard41h12`, `tagCircle21h7` |
| `--tags-dir` | yes      |            | Path to the cloned `apriltag-imgs` repository                            |
| `--out`      | no       | `.`        | Directory where the model folder is created                              |
| `--px`       | no       | `800`      | Texture resolution in pixels                                             |

### A note on sizes

The PNGs in `apriltag-imgs` include a one-cell white margin around the black square. For `tag36h11` the image is 10x10 cells and the black square is 8x8 cells. The script therefore makes the Gazebo box larger than the value you pass:

```
box size = size x cells / (cells - 2)
```

Example: `--size 0.16` produces a 0.2 m box with a 0.16 m black square. The script prints both values when it finishes.

## Using the model in Gazebo

Make Gazebo find your models:

```bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/gz_models
```

Add it to a world file:

```xml
<include>
  <uri>model://apriltag_tag36h11_5</uri>
  <name>tag5</name>
  <pose>2 0 0.5 1.5708 0 -1.5708</pose>
</include>
```

Or spawn it at runtime:

```bash
ros2 run ros_gz_sim create \
  -file ~/gz_models/apriltag_tag36h11_5/model.sdf \
  -name tag5 -x 2 -y 0 -z 0.5 -R 1.5708 -Y -1.5708
```

The tag is a flat box, so check in the Gazebo GUI that the pattern faces the direction you expect and is not mirrored. Adjust the pose rotation if needed.

## Detecting the tag with ROS 2

```bash
sudo apt install ros-jazzy-apriltag-ros
```

Example parameters (use the same `--size` value you generated the model with):

```yaml
apriltag:
  ros__parameters:
    image_transport: raw
    family: 36h11
    size: 0.16        # black square edge in metres
    max_hamming: 0
```

## Troubleshooting

- **Model not found in Gazebo**: check that `GZ_SIM_RESOURCE_PATH` includes the folder that contains the model folders (the `--out` directory), not the model folder itself.
- **Texture missing or the tag is white**: confirm that `materials/textures/<name>.png` exists and that the `albedo_map` path in `model.sdf` matches it.
- **`FileNotFoundError` for the tag image**: check `--tags-dir` points to the cloned `apriltag-imgs` folder and that the ID exists for the chosen family.
- **Distances are about 25% too large**: `size` in `apriltag_ros` must be the black square edge, not the whole board.

## Credits

- Tag images: [AprilRobotics/apriltag-imgs](https://github.com/AprilRobotics/apriltag-imgs)
- Detection: [apriltag_ros](https://github.com/christianrauch/apriltag_ros)

## License

Choose a license (for example MIT) and add a `LICENSE` file. Note that `apriltag-imgs` has its own license, so check it before redistributing any tag images in your repo.
