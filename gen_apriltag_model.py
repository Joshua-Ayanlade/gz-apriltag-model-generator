#!/usr/bin/env python3
"""Generate a Gazebo (gz-sim) AprilTag model.

Usage:
  ./gen_apriltag_model.py --id 5 --size 0.2 --family tag36h11 \
      --tags-dir ~/apriltag-imgs --out ~/gz_models
"""
import argparse, os
from PIL import Image

SDF = """<?xml version="1.0"?>
<sdf version="1.9">
  <model name="{name}">
    <static>true</static>
    <link name="link">
      <visual name="visual">
        <pose>0 0 0 0 0 0</pose>
        <geometry>
          <box><size>{box} {box} 0.002</size></box>
        </geometry>
        <material>
          <diffuse>1 1 1 1</diffuse>
          <specular>0 0 0 1</specular>
          <pbr>
            <metal>
              <albedo_map>materials/textures/{png}</albedo_map>
              <metalness>0.0</metalness>
              <roughness>1.0</roughness>
            </metal>
          </pbr>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <box><size>{box} {box} 0.002</size></box>
        </geometry>
      </collision>
    </link>
  </model>
</sdf>
"""

CONFIG = """<?xml version="1.0"?>
<model>
  <name>{name}</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <description>AprilTag {family} id {id}, {size} m</description>
</model>
"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--size", type=float, default=0.16, help="black square edge length in metres")
    p.add_argument("--family", default="tag36h11")
    p.add_argument("--tags-dir", required=True, help="path to apriltag-imgs clone")
    p.add_argument("--out", default=".")
    p.add_argument("--px", type=int, default=800, help="texture resolution")
    a = p.parse_args()

    # apriltag-imgs naming: tag36h11 -> tag36_11_00005.png
    fam_file = {"tag36h11": "tag36_11", "tag25h9": "tag25_09",
                "tag16h5": "tag16_05", "tagStandard41h12": "tag41_12",
                "tagCircle21h7": "tag21_07"}[a.family]
    src = os.path.join(a.tags_dir, a.family, f"{fam_file}_{a.id:05d}.png")

    img = Image.open(src).convert("RGB")
    cells = img.size[0]
    box = round(a.size * cells / (cells -2),6)

    name = f"apriltag_{a.family}_{a.id}"
    mdir = os.path.join(a.out, name)
    tex = os.path.join(mdir, "materials", "textures")
    os.makedirs(tex, exist_ok=True)


    png = f"{name}.png"
    img.resize((a.px, a.px), Image.NEAREST).save(os.path.join(tex, png))

    open(os.path.join(mdir, "model.sdf"), "w").write(
        SDF.format(name=name, box=box, png=png))
    open(os.path.join(mdir, "model.config"), "w").write(
        CONFIG.format(name=name, family=a.family, id=a.id, size=a.size))
    
    print(f"Created {mdir}")

if __name__ == "__main__":
    main()