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

# Define global constants if needed
# For example, if you have feature extraction parameters:
# FEATURE_EXTRACTOR = cv2.SIFT_create()

# Define module-level functions and classes
def function1(arg1, arg2):
    """
    Description: (A brief description of what this function does.)

    Args:
        arg1: (Description of arg1)
        arg2: (Description of arg2)

    Returns:
        (Description of what the function returns)
    """
    # Implementation of the function
    pass

def extract_sift_features(image_path):
    """
    Extract SIFT features and descriptors from an image.

    Args:
        image_path (str): Path to the input image.

    Returns:
        keypoints (list): List of SIFT keypoints.
        descriptors (numpy.ndarray): SIFT descriptors.
    """
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Create a SIFT feature extractor
    sift = cv2.SIFT_create()

    # Detect keypoints and compute descriptors
    keypoints, descriptors = sift.detectAndCompute(image, None)

    return keypoints, descriptors

def extract_orb_features(image_path):
    """
    Extract ORB features and descriptors from an image.

    Args:
        image_path (str): Path to the input image.

    Returns:
        keypoints (list): List of ORB keypoints.
        descriptors (numpy.ndarray): ORB descriptors.
    """
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Create an ORB feature extractor
    orb = cv2.ORB_create()

    # Detect keypoints and compute descriptors
    keypoints, descriptors = orb.detectAndCompute(image, None)

    return keypoints, descriptors

# You can add more functions or code as needed

# This block allows running the module as a script
if __name__ == "__main__":
    # Example code to test the functions
    image_path = "sample_image.jpg"
    sift_keypoints, sift_descriptors = extract_sift_features(image_path)
    orb_keypoints, orb_descriptors = extract_orb_features(image_path)

    # Process and use the extracted features and descriptors as needed

