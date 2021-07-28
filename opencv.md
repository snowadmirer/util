## functions

* cv2.boundingRect
* cv2.adaptiveThreshold
* cv2.convexHull
* cv2.floodFill
* cv2.findContours
* cv2.drawContours
* cv2.contourArea
* cv2.polylines

## cv2.boundingRect
```python
x, y, w, h = cv2.boundingRect(points)
```
The function calculates and returns the minimal up-right bounding rectangle for the specified point set.

## cv2.adaptiveThreshold
```python
dst = cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C)
dst = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
dst = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
```
## cv2.convexHull
```python
hull_points = cv2.convexHull(points)
```
## cv2.floodFill
```python
fill = image.copy()
mask = cv2.copyMakeBorder(image, 1, 1, 1, 1, borderType=cv2.BORDER_CONSTANT, value=255)
cv2.floodFill(fill, mask, seedPoint=(0,0), newVal=255)
image |= ~fill
```
## cv2.polylines
```python
# cv2.polylines(img, pts, isClosed, color[, thickness[, lineType[, shift]]]) → None
points = np.array([[910, 650], [206, 650], [458, 500], [696, 500]])
cv2.polylines(img, [points], 1, (255, 0, 255))
```

## cv2.putText
```python
#img = cv.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
```

## cv2.drawContours
```
cv2.drawContours(image, contours, contourIdx, color, thickness=None, lineType=None, hierarchy=None, maxLevel=None, offset=None)
img=cv2.drawContours(img,contours,-1,(0,255,0),5)
```

##

##  cv2.fillPoly
```python
area1 = np.array([[250, 200], [300, 100], [750, 800], [100, 1000]])
area2 = np.array([[1000, 200], [1500, 200], [1500, 400], [1000, 400]])

cv2.fillPoly(img, [area1, area2], (255, 255, 255))
```
