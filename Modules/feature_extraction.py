"""
based on: https://meshroom-manual.readthedocs.io/en/latest/feature-documentation/nodes/FeatureExtraction.html
Module for feature extraction operations. Contains functions for SIFT, ORB, or other feature extraction methods.

Feature extraction flowchart: 
-Load an image.
-Compute a Gaussian pyramid of the image.
-Apply the Difference of Gaussians to find scale-space maxima.
-Sample image patches around each keypoint.
-Compute feature descriptors for each patch.

useful link:
https://docs.opencv.org/3.4/db/d27/tutorial_py_table_of_contents_feature2d.html
ORB overview https://docs.opencv.org/3.4/d1/d89/tutorial_py_orb.html
feature detection and matching/classifying project https://www.youtube.com/watch?v=nnH55-zD38I&list=PLMoSUbG1Q_r8jFS04rot-3NzidnV54Z2q&index=23
"""
# Import necessary libraries
import cv2
import numpy as np
import os
# from PyQt5.QtCore import QLibraryInfo
# os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
#     QLibraryInfo.PluginsPath
# )

# Define global constants if needed
# For example, if you have feature extraction parameters:
# FEATURE_EXTRACTOR = cv2.SIFT_create()

# Define module-level functions and classes
def extract_orb_features(filepath, num_features):
    """
    use ORB algorithm to extract features in an image and return a 1 elem dict with features list:image name

    Args:
        filepath (str): path to the image file to be processed
        num_features (int): 
    Returns:
        features (dict): 1 element dict mapping a list of features to the str name of the image
    """
    img = cv2.imread(filepath)

    orb = cv2.ORB.create(nfeatures=num_features)

    keypoints, descriptors = orb.detectAndCompute(img, None)
    if keypoints:
        return keypoints, descriptors
    
    else:
        raise Exception(f"filepath {filepath} failed to generate keypoints")

def descriptors_of_folder(folderpath, num_features=1000, testing=False):
    """
    use feature extraction algorithm to create a list of all descriptors

    Args:
        folderpath (str): relative or absolute path to the folder containing imgs
        num_features (int): number of feature to detect with ORB
        testing (bool): test only a small amount of images for processing time
    """
    folder_descriptors = []
    folder_keypoints = []
    # generate list of paths to all files in folder
    files = os.listdir(folderpath)
    if testing==True: 
        files = files[0:5]
    for file in files:
        keypoints , descriptors = extract_orb_features(os.path.join(folderpath, file), num_features)
        folder_descriptors.append(descriptors)
        folder_keypoints.append(keypoints)
        # print("processing")

    if len(folder_descriptors)!=len(files):
        raise Exception(f"Error in descriptor generation! Number of files {len(files)} does not match number descriptors {len(folder_descriptors)}")
    return folder_keypoints, folder_descriptors
    # loop through paths and apply orb, place feature descriptors into dict descriptor:filename


# You can add more functions or code as needed

# This block allows running the module as a script
if __name__ == "__main__":
    # Example code to test the functions
    folder_path = '/home/rajiv/Github/Py-Photogrammetry/Data'
    # relative_paths = [os.path.relpath(os.path.join(folder_path, item), start=os.getcwd()) for item in os.listdir(folder_path)]

    # image_path = relative_paths[0]

    image = cv2.imread(os.path.join(folder_path, os.listdir(folder_path)[10]))
    dimensions = image.shape
    orb_keypoints, orb_descriptors = descriptors_of_folder(folder_path, 1000, testing=True)

    # test individual image extraction
    # orb_keypoints, orb_descriptors = extract_orb_features(os.path.join(folder_path, os.listdir(folder_path)[0]), 1000)

    # display the keypoints of the first image in the folder
    img_keypoints = cv2.drawKeypoints(image, orb_keypoints[0], None, dimensions, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 

    cv2.namedWindow('keypoints', cv2.WINDOW_NORMAL)
    cv2.imshow('keypoints', img_keypoints)
    cv2.resizeWindow('keypoints', int(dimensions[1]/5), int(dimensions[0]/5))

    cv2.waitKey(0) # wait until keypress
    cv2.destroyAllWindows()

