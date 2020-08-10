## functions
* cv2.boundingRect
* cv2.adaptiveThreshold
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
