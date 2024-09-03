#tab#1 - download data

# compare after/before n3d
mkdir -p ~/workspace/dataset/Neural3D
cd ~/workspace/dataset/Neural3D
wget https://github.com/facebookresearch/Neural_3D_Video/releases/download/v1.0/flame_steak.zip
unzip flame_steak.zip -d before/
unzip flame_steak.zip -d after/

# compare after/before immersive_[un]distorted
mkdir -p ~/workspace/dataset/immersive
cd ~/workspace/dataset/immersive
wget https://storage.googleapis.com/deepview_video_raw_data/02_Flames.zip

unzip 02_Flames.zip -d before/
unzip 02_Flames.zip -d after/

#tab#2 - run pre scripts

cd ~/workspace/SpacetimeGaussians
git checkout main
python script/pre_n3d.py --videopath ../dataset/Neural3D/before/flame_steak
git checkout pre-refactor
python script/pre_n3d.py --videopath ../dataset/Neural3D/after/flame_steak

# basic checks
diff before/flame_steak/colmap_0/sparse/0/cameras.bin after/flame_steak/colmap_0/sparse/0/cameras.bin #same, complete check in py
#diff before/flame_steak/colmap_0/sparse/0/images.bin after/flame_steak/colmap_0/sparse/0/images.bin #differ, complete check in py
diff before/flame_steak/colmap_0/manual/cameras.txt after/flame_steak/colmap_0/manual/cameras.txt #same, complete check in py
diff before/flame_steak/colmap_0/manual/images.txt after/flame_steak/colmap_0/manual/images.txt #same, complete check in py
#diff before/flame_steak/colmap_0/input.db after/flame_steak/colmap_0/input.db # differ as sparse cloud slighly diff, complete check in py

# immersive dist
git checkout main
python script/pre_immersive_distorted.py --videopath ../dataset/immersive/before/02_Flames
git checkout pre-refactor
python script/pre_immersive_distorted.py --videopath ../dataset/immersive/after/02_Flames

# basic checks
diff before/02_Flames_dist/camera_0001.npy after/02_Flames_dist/camera_0001.npy #same, complete check in py
diff before/02_Flames_dist/colmap_0/sparse/0/cameras.bin after/02_Flames_dist/colmap_0/sparse/0/cameras.bin #same, complete check in py
#diff before/02_Flames_dist/colmap_0/sparse/0/images.bin after/02_Flames_dist/colmap_0/sparse/0/images.bin #differ, complete check in py
diff before/02_Flames_dist/colmap_0/images/camera_0001.png after/02_Flames_dist/colmap_0/images/camera_0001.png #same

# immersive undist
git checkout main
python script/pre_immersive_undistorted.py --videopath ../dataset/immersive/before/02_Flames
git checkout pre-refactor
python script/pre_immersive_undistorted.py --videopath ../dataset/immersive/after/02_Flames