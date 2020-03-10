#读写中文图片路径
img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
cv2.imencode('.jpg', img)[1].tofile(save_path)
