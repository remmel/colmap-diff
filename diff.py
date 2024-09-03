import filecmp
import sqlite3
from pathlib import Path

import numpy as np

from third_party.colmap.scripts.python.read_write_model import read_points3D_binary, read_images_binary, \
    read_cameras_binary


# def check_points(dir_a, dir_b):

# dir_a = Path.home() / 'workspace/dataset/Neural3D/before/flame_steak/colmap_0/sparse/0/'
# dir_b = Path.home() / 'workspace/dataset/Neural3D/after/flame_steak/colmap_0/sparse/0/'


def diff_sparse0bins(colmap_a, colmap_b):
    colmap_num = colmap_a.name
    
    # check extrinsics & intriniscs
    sparse0_a = colmap_a / 'sparse/0'
    sparse0_b = colmap_b / 'sparse/0'

    if not sparse0_a.exists() or not sparse0_b.exists():
        print(f"sparse/0 directory not found not found: {sparse0_a} or {sparse0_b}")
    
    # check extrinsics & intriniscs
    images_a = read_images_binary(sparse0_a / 'images.bin')
    images_b = read_images_binary(sparse0_b / 'images.bin')
    cameras_a = read_cameras_binary(sparse0_a / 'cameras.bin')
    cameras_b = read_cameras_binary(sparse0_b / 'cameras.bin')
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
            all(np.equal(camera_a.params, camera_b.params)),
        ):
            print(f"{image_a.name}: Camera mismatch")
        
            
   # check points
    points3D_a = read_points3D_binary(sparse0_a / 'points3D.bin')
    points3D_b = read_points3D_binary(sparse0_b / 'points3D.bin')

    num_points_a = len(points3D_a)
    num_points_b = len(points3D_b)

    percentage_diff = abs(num_points_b - num_points_a) / num_points_a * 100
    # if (percentage_diff > 1.0):
    if num_points_a != num_points_b:
        print(f"{colmap_num}: space 3D points: {num_points_a} vs {num_points_b} - {percentage_diff:.2f}% difference")
    
    
def diff_manualtxts(colmap_a, colmap_b):    
    # check txt
    camerastxt_a = colmap_a / 'manual/cameras.txt'
    camerastxt_b = colmap_b / 'manual/cameras.txt'
    assert filecmp.cmp(camerastxt_a,camerastxt_b ), 'cameras.txt does not match'
    
    imagestxt_a = colmap_a / 'manual/images.txt'
    imagestxt_b = colmap_b / 'manual/images.txt'
    assert filecmp.cmp(imagestxt_a,imagestxt_b ), f'images.txt does not match, {imagestxt_a} != {imagestxt_b}'


# Compares the images and cameras tables from colmap database    
def diff_sqlite_inputdb(colmap_a, colmap_b):
    images_a = sqlite_select_all_images(colmap_a / 'input.db')
    images_b = sqlite_select_all_images(colmap_b / 'input.db')
    
    if len(images_a)!= len(images_b):
        print(f"sqlite: image count: {len(images_a)} vs {len(images_b)}")
        
    if images_a!= images_b:
        print(f"sqlite: images do not match")
        
    cameras_a = sqlite_select_all_cameras(colmap_a / 'input.db')
    cameras_b = sqlite_select_all_cameras(colmap_b / 'input.db')
    
    if len(cameras_a)!= len(cameras_b):
        print(f"sqlite: camera count: {len(cameras_a)} vs {len(cameras_b)}")
        
    if cameras_a!= cameras_b:
        print(f"sqlite: cameras do not match")
        
    # print(f"sqlite: {colmap_name}")
    
    
def sqlite_select_all_images(inputdb_path):
    conn = sqlite3.connect(inputdb_path)
    c = conn.cursor()
    c.execute("SELECT * FROM images")
    rows = c.fetchall()
    conn.close()
    return rows

def sqlite_select_all_cameras(inputdb_path):
    conn = sqlite3.connect(inputdb_path)
    c = conn.cursor()
    c.execute("SELECT * FROM cameras")
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    
    # n3d
    if False:
        base_dir_a = Path.home() / 'workspace/dataset/Neural3D/before/flame_steak'
        base_dir_b = Path.home() / 'workspace/dataset/Neural3D/after/flame_steak'
        colmap_dirs = sorted(base_dir_a.glob('colmap_*'))
        print(f"Checking {base_dir_a}/colmap_* with after")
        for colmap_dir in colmap_dirs:
            colmap_name = colmap_dir.name
            print(f"Checking {colmap_name}")
            colmap_a = base_dir_a / colmap_name
            colmap_b = base_dir_b / colmap_name
    
            diff_bin(colmap_a, colmap_b)
            diff_txt(colmap_a, colmap_b)
            diff_sqlite(colmap_a, colmap_b)
        
    # immersive dist
    if True:
        base_dir_a = Path.home() / 'workspace/dataset/immersive/before/02_Flames_dist'
        base_dir_b = Path.home() / 'workspace/dataset/immersive/after/02_Flames_dist'
    
        colmap_dirs = sorted(base_dir_a.glob('colmap_*'))
        print(f"Checking {base_dir_a}/colmap_* with after")
        for colmap_dir in colmap_dirs:
            colmap_name = colmap_dir.name
            print(f"Checking {colmap_name}")
            colmap_a = base_dir_a / colmap_name
            colmap_b = base_dir_b / colmap_name
    
            diff_sparse0bins(colmap_a, colmap_b)
            diff_manualtxts(colmap_a, colmap_b)
            diff_sqlite_inputdb(colmap_a, colmap_b)
            
        assert filecmp.cmp(base_dir_a / 'camera_0001.npy', base_dir_b / 'camera_0001.npy' ), 'camera_0001.npy differs'
        assert filecmp.cmp(base_dir_a / 'colmap_0/images/camera_0001.png', base_dir_b / 'colmap_0/images/camera_0001.png'), 'colmap_0/images/camera_0001.png differs'
        