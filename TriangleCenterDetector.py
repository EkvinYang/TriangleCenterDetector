import pyautogui
import cv2
import math
from PIL import Image, ImageGrab
import time
import sys
import os

verticies = list()
def calculatePoints(verticies):
    points = list()
    pointA = verticies[0]
    pointB = verticies[1]
    pointC = verticies[2]
    midptAB = ((pointA[0] + pointB[0])/2, (pointA[1] + pointB[1])/2)
    midptBC = ((pointC[0] + pointB[0])/2, (pointC[1] + pointB[1])/2)
    slopeAB = (pointA[1] - pointB[1])/(pointA[0] - pointB[0])
    slopeBC = (pointC[1] - pointB[1])/(pointC[0] - pointB[0])

    #find centroid
    centroid = [int((pointA[0]+pointB[0]+pointC[0])/3), int((pointA[1]+pointB[1]+pointC[1])/3)]
    
    #find circumcenter 
    #m2 is AB m1 is BC 
    circumcenter_x= int((midptBC[1] - midptAB[1] -1/slopeAB * midptAB[0] + 1/slopeBC * midptBC[0]) / (1/slopeBC - 1/slopeAB))
    circumcenter_y = int((-1/slopeAB) * (circumcenter_x - midptAB[0]) + midptAB[1])
    circumcenter = [circumcenter_x, circumcenter_y]
    
    #find incenter
    lengthAB = math.sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)
    lengthBC = math.sqrt((pointB[0] - pointC[0])**2 + (pointB[1] - pointC[1])**2)
    lengthAC = math.sqrt((pointA[0] - pointC[0])**2 + (pointA[1] - pointC[1])**2)

    perimeter = lengthAB + lengthBC + lengthAC

    incenter = [int((lengthBC * pointA[0] + lengthAC * pointB[0] + lengthAB * pointC[0])/perimeter), int((lengthBC * pointA[1] + lengthAC * pointB[1] + lengthAB * pointC[1])/perimeter)]

    #find orthocenter
    orthoX = (1/slopeBC*pointA[0]+pointA[1]-1/slopeAB*pointC[0]-pointC[1])/(1/slopeBC-1/slopeAB)
    orthoY = -1/slopeBC*(orthoX-pointA[0])+pointA[1]
    orthocenter = [int(orthoX), int(orthoY)]

    centroid[1] = round(centroid[1], 3)
    circumcenter[1] = round(circumcenter[1], 3)
    incenter[1] = round(incenter[1], 3)
    orthocenter[1] = round(orthocenter[1], 3)
    centroid[0] = round(centroid[0], 3)
    circumcenter[0] = round(circumcenter[0], 3)
    incenter[0] = round(incenter[0], 3)
    orthocenter[0] = round(orthocenter[0], 3)
    
    points.append(centroid)
    points.append(circumcenter)
    points.append(incenter)
    points.append(orthocenter)
    return points
time.sleep(1)
pyautogui.click(700,850)
print("clicked: " + str(pyautogui.position()))
time.sleep(0.5)
pyautogui.click(1400,1120)
print("clicked: " + str(pyautogui.position()))
time.sleep(5.01)
pyautogui.scroll(-1000)
time.sleep(0.1)
screenshot = ImageGrab.grab(bbox=(1223,968,1713,1453))

current_file_path = os.path.abspath(sys.argv[0])
current_directory = os.path.dirname(current_file_path)
screenshot.save(current_directory + "/TestScreenshots/triangle.png")
image = cv2.imread(current_directory + "/TestScreenshots/triangle.png")


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  
# setting threshold of gray image 
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) 
  
# using a findContours() function 
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

i = 0
# list for storing names of shapes 
for contour in contours: 
    # here we are ignoring first counter because  
    # findcontour function detects whole image as shape 
    if i == 0: 
        i = 1
        continue
    # cv2.approxPloyDP() function to approximate the shape 
    approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True) 
contours = approx
verticies = list()
for i in contours:
    print("vertex: " + str([i[0][0], i[0][1]]))
    verticies.append([i[0][0], i[0][1]])

# cv2.drawMarker(image, centroid, (0, 0, 255), 0, 0, 15, 0)

points = calculatePoints(verticies)
# centroid = points[0]
# circumcenter = points[1]
# incenter = points[2]
# orthocenter = points[3] 
# print("centriod: " + str(centroid))
# print("circumcenter: " + str(circumcenter))
# print("incenter: " + str(incenter))
# print("orthocenter: " + str(orthocenter))

#loop through points and click
for i in points:
    
    pyautogui.click(1223+i[0],968+i[1])
    print("clicked: " + str(pyautogui.position()))
    time.sleep(2.72)
    pyautogui.scroll(-1000)
    time.sleep(0.1)
# cv2.drawContours(image, contours, -1, (0, 255, 0), 10) 
# cv2.imshow('Contours', image) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 