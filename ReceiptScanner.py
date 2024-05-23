import pytesseract # type: ignore
import imutils # type: ignore
from imutils.perspective import four_point_transform # type: ignore
import argparse
import numpy as np # type: ignore
import os
import cv2 # type: ignore
import re

# How to run the script with the image: "python ReceiptScanner.py -i Receipt10.jpg"
# How to run the script with the image and debug: "python ReceiptScanner.py -i Receipt10.jpg -d 1"

    
def imageprocess(chosenImage):
    orig = cv2.imread(chosenImage)
    image = orig.copy()
    image = imutils.resize(image, width=500)
    ratio = orig.shape[1] / float(image.shape[1])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
    edged = cv2.Canny(blurred, 75, 200)
    
    # find contours in the edge map and sort them by size in descending
    # order
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Minimum contour area threshold
    MIN_CONTOUR_AREA = 1000

    # Filter out smaller contours
    cnts = [c for c in cnts if cv2.contourArea(c) > MIN_CONTOUR_AREA]

    # Sort the remaining contours by size in descending order
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)  

    # initialize a contour that corresponds to the receipt outline
    receiptCnt = None

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we can
        # assume we have found the outline of the receipt
        if len(approx) == 4:
            receiptCnt = approx
            break
        
    # if the receipt contour is empty then our script could not find the
    # outline and we should be notified
    if receiptCnt is None:
        raise Exception(("Could not find receipt outline. "
            "Try debugging your edge detection and contour steps."))

    # apply a four-point perspective transform to the *original* image to
    # obtain a top-down bird's-eye view of the receipt
    receipt = four_point_transform(orig, receiptCnt.reshape(4, 2) * ratio)

    # show transformed image
    cv2.imshow("Receipt Transform", imutils.resize(receipt, width=500))

    print("Process completed")

    # apply OCR to the receipt image by assuming column data, ensuring
    # the text is *concatenated across the row* (additionally, for your
    # own images you may need to apply additional processing to cleanup
    # the image, including resizing, thresholding, etc.)
    options = "--psm 6"
    text = pytesseract.image_to_string(
        cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB),
        config=options)
    # show the raw output of the OCR process
    print("[INFO] raw output:")
    print("==================")
    print(text)
    print("\n")

def main():
    imageInput = input("Name of image file: ")
    imageprocess(imageInput)
    
if __name__ == "__main__":
    main()

