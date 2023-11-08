"""
based on: https://meshroom-manual.readthedocs.io/en/latest/feature-documentation/nodes/DepthMap.html
Module for depth map computation and filtering.


Depth Map Flowchart:

Retrieve depth values for pixels.
Use methods like Block Matching, Semi-Global Matching (SGM), or ADCensus.
Apply filtering to ensure depth consistency.

Depth Map Filter:
Isolate and correct areas of inconsistent depth.

useful links:
Stereo Camera Depth Estimation With OpenCV - https://learnopencv.com/depth-perception-using-stereo-camera-python-c/

stereo commands: block matching, https://docs.opencv.org/3.4/d2/d7f/namespacecv_1_1stereo.html
stereo camera depth - https://docs.opencv.org/3.4/dd/d53/tutorial_py_depthmap.html

https://albertarmea.com/post/opencv-stereo-camera/
"""
import cv2
import numpy as np
import os

# Define global constants if needed
# For example, if you have feature extraction parameters:
# FEATURE_EXTRACTOR = cv2.SIFT_create()

# Define module-level functions and classes
def depth_between_images(img1, img2, numDisparities=128, blocksize=21):
    """
    take in 2 close images and output a depth map
    
    Args:
        arg1: (Description of arg1)
        arg2: (Description of arg2)

    Returns:
        (Description of what the function returns)
    """
    # Implementation of the function
    # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # img2 = cv2.imread(img2, cv2.COLOR_BGR2GRAY)
    stereo = cv2.StereoBM_create(numDisparities=numDisparities, blockSize=blocksize)
    stereo.setMinDisparity(4)
    stereo.setNumDisparities(128)
    stereo.setBlockSize(21)
    stereo.setSpeckleRange(16)
    stereo.setSpeckleWindowSize(45)

    disparity = stereo.compute(img1,img2)
    disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    return disparity



# You can add any module-level code here if necessary

# This block allows running the module as a script
if __name__ == "__main__":
    
    folder_path = '/home/rajiv/Github/Py-Photogrammetry/Data'
    files = os.listdir(folder_path)
    filenames = [os.path.splitext(file)[0]+".JPG" for file in files]
    print([(idx, filename) for idx, filename in enumerate(filenames)])

    test_file_id, match_file_id = (10, 20)
    img1 = cv2.imread(os.path.join(folder_path, os.path.normpath(filenames[test_file_id])), 0)
    img2 = cv2.imread(os.path.join(folder_path, os.path.normpath(filenames[match_file_id])), 0)

    depth_map = depth_between_images(img1, img2)
    # show matched image
    DEPTH_VISUALIZATION_SCALE = 2048
    cv2.namedWindow('depth_map', cv2.WINDOW_NORMAL)
    cv2.imshow('depth_map', depth_map / DEPTH_VISUALIZATION_SCALE)
    cv2.resizeWindow('depth_map', int(depth_map.shape[1]/5), int(depth_map.shape[0]/5))

    # show matched image
    cv2.namedWindow('match', cv2.WINDOW_NORMAL)
    cv2.imshow('match', img1)
    cv2.resizeWindow('match', int(img1.shape[1]/5), int(img1.shape[0]/5))


    cv2.waitKey(0) # wait until keypress
    cv2.destroyAllWindows()


