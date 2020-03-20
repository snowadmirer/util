from PIL import Image, ImageFont, ImageDraw

def get_rotation_mat(image_size, angle, target_size=None, crop=True):
    width, height = image_size
    rotation_mat = cv2.getRotationMatrix2D((width/2.,height/2.),angle,1)
    if target_size:
        new_width, new_height = target_size
    elif crop:
        new_height = height
        new_width = width
    else:
        new_height =int(width*fabs(sin(radians(angle)))+height*fabs(cos(radians(angle))))
        new_width =int(height*fabs(sin(radians(angle)))+width*fabs(cos(radians(angle))))

    rotation_mat[0,2] +=(new_width - width)/2 #重点在这步，目前不懂为什么加这步
    rotation_mat[1,2] +=(new_height - height)/2 #重点在这步
    return rotation_mat


def rotate_image(image, angle, target_size=None, crop=True):
    height, width = image.shape[:2]
    rotation_mat = cv2.getRotationMatrix2D((width/2.,height/2.),angle,1)
    if target_size:
        new_width, new_height = target_size
    elif crop:
        new_height = height
        new_width = width
    else:
        new_height =int(width*fabs(sin(radians(angle)))+height*fabs(cos(radians(angle))))
        new_width =int(height*fabs(sin(radians(angle)))+width*fabs(cos(radians(angle))))

    rotation_mat[0,2] +=(new_width - width)/2 #重点在这步，目前不懂为什么加这步
    rotation_mat[1,2] +=(new_height - height)/2 #重点在这步

    rotated_image = cv2.warpAffine(image, rotation_mat, (new_width, new_height),borderValue=(255,255,255))
    return rotated_image, rotation_mat

def get_word_box(font, word):
    font_size = font.size
    image = Image.new('L', (font_size * 2, font_size* 3), 0)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), word, font=font, fill=(255))
    array = np.array(image, dtype=np.uint8)
    row_sum = np.sum(array, axis=0)
    col_sum = np.sum(array, axis=1)
    x1 = 0
    x2 = len(row_sum)
    y1 = 0
    y2 = len(col_sum)
    for x in range(0, len(row_sum)):
        if row_sum[x] > 0:
            x1 = x
            break
    for x in range(0, len(row_sum)):
        if row_sum[len(row_sum) - 1 - x] > 0:
            x2 = len(row_sum) - x
            break
    for y in range(0, len(col_sum)):
        if col_sum[y] > 0:
            y1 = y
            break
    for y in range(0, len(col_sum)):
        if col_sum[len(col_sum) - 1 - y] > 0:
            y2 = len(col_sum) - y
            break
    return (x1, y1, x2, y2), array

def get_outer_box(box, angle):
    # 左上角为旋转中心
    xmin, ymin, xmax, ymax = box
    rotation_mat = cv2.getRotationMatrix2D((xmin, ymin), angle, 1)
    pts = np.array([[xmin, ymin, 1], [xmin, ymax, 1], [xmax, ymin, 1], [xmax, ymax, 1]], dtype=np.float32).T
    out_pts = np.dot(rotation_mat, pts)
    xmin = np.min(out_pts[0,:])
    xmax = np.max(out_pts[0,:])
    ymin = np.min(out_pts[1,:])
    ymax = np.max(out_pts[1,:])
    return (xmin, ymin, xmax, ymax)

def get_affine_pt(mat, pt):
    pt = np.dot(mat, list(pt) + [1])
    x, y = int(pt[0]), int(pt[1])
    return [x, y]

def draw_text(font, image, pos, word, fill):
    pil_image = Image.fromarray(image.astype('uint8')).convert('RGB')
    draw = ImageDraw.Draw(pil_image)
    draw.text(pos, word, font=font, fill=fill)
    return np.array(pil_image, dtype=np.uint8)

def draw_text(font, image, pos, word, fill, angle = None):
    height, width = image.shape[:2]
    if angle:
        rotated_image, rotation_mat = rotate_image(image, -angle, crop=False)
        word_box, _ = get_word_box(font, word)
        x, y = pos
        x_r, y_r = get_affine_pt(rotation_mat, (pos[0], pos[1]))
        word_box = (word_box[0]+x, word_box[1]+y, word_box[2]+x, word_box[3]+y)
        outer_box = get_outer_box(word_box, angle)

        pil_image = Image.fromarray(rotated_image.astype('uint8')).convert('RGB')
        draw = ImageDraw.Draw(pil_image)
        draw.text((int(x_r), int(y_r)), word, font=font, fill=fill)

        rotated_image = np.array(pil_image, dtype=np.uint8)
        cv2.imwrite('draw.jpg', rotated_image)
        new_image, _ = rotate_image(rotated_image, angle, target_size=(width, height))
        xmin, ymin, xmax, ymax = [int(i) for i in outer_box]
        res_image = image.copy()
        #res_image[ymin:ymax, xmin:xmax] = new_image[ymin:ymax, xmin:xmax]
        res_image = new_image
        cv2.imwrite('res.jpg', res_image)
        return res_image, outer_box
    else:
        pil_image = Image.fromarray(image.astype('uint8')).convert('RGB')
        draw = ImageDraw.Draw(pil_image)
        draw.text(pos, word, font=font, fill=fill)
        res_image = np.array(pil_image, dtype=np.uint8)
        word_box, _ = get_word_box(font, word)
        x, y = pos
        word_box = (word_box[0]+x, word_box[1]+y, word_box[2]+x, word_box[3]+y)
        return res_image, word_box
