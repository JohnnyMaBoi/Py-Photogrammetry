"""
Module for image matching operations. It may include vocabulary tree construction, image descriptor generation, and comparison.


Image Matching Flowchart:

MESHROOM
Generate image descriptors using the vocabulary tree approach.
Build image descriptors based on feature descriptors.
Create image descriptors using the tree structure.
Compare image descriptors to find similar images.

THIS IMPLEMENTATION
Start with a list of feature descriptors 
Iterate through list and for each descriptor compute match with all other descriptors, keep best match
For repeat matches, pick highest corresponding and then re-select the other match

Useful Links:
feature detection and matching/classifying project https://www.youtube.com/watch?v=nnH55-zD38I&list=PLMoSUbG1Q_r8jFS04rot-3NzidnV54Z2q&index=23
https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
"""

# Import necessary libraries
import cv2
import numpy as np
import os
import sys
from feature_extraction import descriptors_of_folder

# Define global constants if needed
# For example, if you have feature extraction parameters:
# FEATURE_EXTRACTOR = cv2.SIFT_create()

def return_best_match(descriptors, idx, idx_to_exclude=None):
    """
    Index of best descriptor match for an image based on a list of descriptors

    Args:
        descriptors (list): list of image descriptors from keypoint identification like ORB or SLAM
        idx (int): index of the item to be checked. Will be excluded from matches automatically.
        idx_to_exclude (optional int): for re-matching points without an image which has a better match

    Returns:
        match_idx, confidence (tuple int, float): 
    """
    thresh = 15
    original_descriptor = descriptors[idx]
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matchList = []
    finalVal = -1
    # loop through each image descriptor
    for index, des in enumerate(descriptors): 
        if index == idx:
            matchList.append(0)
        else:
            matches = bf.knnMatch(des, original_descriptor, k=2)
            # matches = bf.match(des, original_descriptor)
            good = []
            for m, n in matches:
                if m.distance < .6*n.distance:
                    good.append([m])
            matchList.append(len(good)) #record successes for each image in matchlist
    #print(matchList)
    if len(matchList) != 0:
        print("This is how many feature matches each image had for your input image \n")
        print([(idx, match) for idx, match in enumerate(matchList)])
        if max(matchList) > thresh:
            match_idx = matchList.index(max(matchList))
            print(f"match with {max(matchList)} selected")
            return match_idx
        else: 
            print(f"max match too low! {max(matchList)} threshold {thresh}")
    else:
        print("failed")



# You can add any module-level code here if necessary

# This block allows running the module as a script
if __name__ == "__main__":
    
    test_file_id = 10
    folder_path = '/home/rajiv/Github/Py-Photogrammetry/Data'
    files = os.listdir(folder_path)
    filenames = [os.path.splitext(file)[0]+".JPG" for file in files]
    print("This is which index maps to which filename \n")
    print([(idx, filename) for idx, filename in enumerate(filenames)])

    orb_keypoints, orb_descriptors = descriptors_of_folder(folder_path, 1000, testing=False)

    img2 = cv2.imread(os.path.join(folder_path, os.path.normpath(filenames[test_file_id])))

    id = return_best_match(orb_descriptors, test_file_id)
    if id != -1:
        print(f"ID of match is {id}")
    
    # load matched image
    match = cv2.imread(os.path.join(folder_path, os.path.normpath(filenames[id])))
    # show original image
    # cv2.namedWindow('img2', cv2.WINDOW_NORMAL)
    # cv2.imshow('img2', img2)
    # cv2.resizeWindow('img2', int(img2.shape[1]/5), int(img2.shape[0]/5))

    # show matched image
    # cv2.namedWindow('match', cv2.WINDOW_NORMAL)
    # cv2.imshow('match', match)
    # cv2.resizeWindow('match', int(match.shape[1]/5), int(match.shape[0]/5))

    # redo matching for best pair once
    bf2 = cv2.BFMatcher(cv2.NORM_HAMMING)
    # Match descriptors.
    matches = bf2.knnMatch(orb_descriptors[test_file_id], orb_descriptors[id], k=2)

    img3 = cv2.drawMatchesKnn(img2,orb_keypoints[test_file_id],match,orb_keypoints[id],matches[:10],None,matchColor=None, singlePointColor=None,matchesMask=None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)#
    cv2.namedWindow('comparison', cv2.WINDOW_NORMAL)
    cv2.imshow('comparison', img3)
    cv2.resizeWindow('comparison', int(img3.shape[1]/5), int(img3.shape[0]/5))
    cv2.waitKey(0)
    cv2.destroyAllWindows
