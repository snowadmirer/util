#读写中文图片路径
import cv2
from PIL import Image
img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
cv2.imencode('.jpg', img)[1].tofile(save_path)

def download_image(img_src, save_path):
     response = requests.get(img_src)
     image = Image.open(BytesIO(response.content))
     image.save(save_path)

def rgba2rgb(image:np.array)->np.array:
    rgb = image[:,:,:3]
    a = image[:,:,3]
    bg = np.zeros_like(rgb) + 255
    rgb = Image.fromarray(rgb)
    a = Image.fromarray(a)
    bg = Image.fromarray(bg)
    bg.paste(rgb, mask=a)
    image = np.asarray(bg)
    return image
