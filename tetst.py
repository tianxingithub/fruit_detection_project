import cv2

pp = 'E:/Python/_WorkProject/fruit_detection_project/test/1.png'
img = cv2.imread(pp)
cv2.imshow('img',img)
cv2.waitKey(1)