import os
from pathlib import Path

import numpy as np

from third_party.colmap.scripts.python.read_write_model import read_points3D_binary, read_images_binary, \
    read_cameras_binary


# def check_points(dir_a, dir_b):

# dir_a = Path.home() / 'workspace/dataset/Neural3D/before/flame_steak/colmap_0/sparse/0/'
# dir_b = Path.home() / 'workspace/dataset/Neural3D/after/flame_steak/colmap_0/sparse/0/'


def check_points(dir_a, dir_b, info):
    # check extrinsics & intriniscs
    images_a = read_images_binary(dir_a / 'images.bin')
    images_b = read_images_binary(dir_b / 'images.bin')
    cameras_a = read_cameras_binary(dir_a / 'cameras.bin')
    cameras_b = read_cameras_binary(dir_b / 'cameras.bin')
    assert len(images_a) == len(images_b), "Number of images in both directories"
    
    images_b_by_name = {img.name: img for img in images_b.values()}

    for image_id_a, image_a in images_a.items():
        # print(f"Image ID: {image_id_a}")
        image_b = images_b_by_name.get(image_a.name)
        if image_b is None:
            print(f"Image not found in the second directory: {image_a.name}")
            continue
            
        if not all(image_a.qvec == image_b.qvec):
            print(f"{image_a.name}: Rotation (quaternion): {image_a.qvec} - {image_b.qvec}")
            
        if not all(image_a.tvec == image_b.tvec):
            print(f"{image_a.name}: Translation: {image_a.tvec} - {image_b.tvec}")    
            
        camera_a = cameras_a[image_a.camera_id]
        camera_b = cameras_b[image_a.camera_id]
        
        assert(image_a.camera_id == image_b.camera_id)
        
        if not (
            camera_a.model == camera_b.model and
            camera_a.width == camera_b.width and
            camera_a.height == camera_b.height and
            np.equal(camera_a.params, camera_b.params),
        ):
            print(f"{image_a.name}: Camera mismatch")
        
            
   # check points
    points3D_a = read_points3D_binary(dir_a / 'points3D.bin')
    points3D_b = read_points3D_binary(dir_b / 'points3D.bin')

    num_points_a = len(points3D_a)
    num_points_b = len(points3D_b)

    percentage_diff = abs(num_points_b - num_points_a) / num_points_a * 100
    if (percentage_diff > 1.0):
        print(f"{info}: space 3D points: {num_points_a} vs {num_points_b} - {percentage_diff:.2f}% difference")

def check_poses(imagesbin_a, imagesbin_b):
    pass

if __name__ == "__main__":
    base_dir_a = Path.home() / 'workspace/dataset/Neural3D/before/flame_steak'
    base_dir_b = Path.home() / 'workspace/dataset/Neural3D/after/flame_steak'
    colmap_dirs = sorted(base_dir_a.glob('colmap_*'))
    
    for colmap_dir in colmap_dirs:
        colmap_name = colmap_dir.name

        dir_a = base_dir_a / colmap_name / 'sparse/0'
        dir_b = base_dir_b / colmap_name / 'sparse/0'

        if dir_a.exists() and dir_b.exists():
            check_points(dir_a, dir_b, colmap_name)
        else:
            print(f"Directory not found: {dir_a} or {dir_b}")
            
            
    # sparse_model_path = Path.home() / 'workspace/dataset/Neural3D/before/flame_steak/colmap_0/sparse/0/images.bin'
    
