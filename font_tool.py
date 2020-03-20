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
