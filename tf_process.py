def tf_resize_with_pad(img, target_height, target_width):
    target_h = tf.constant(target_height, dtype=tf.int32)
    target_w = tf.constant(target_width, dtype=tf.int32)

    input_shape = tf.cast(tf.shape(img), tf.int32)
    h, w = input_shape[1], input_shape[2]

    resize_scale = tf.minimum(tf.cast(target_w, tf.float32)/tf.cast(w, tf.float32), tf.cast(target_h, tf.float32)/tf.cast(h, tf.float32))

    new_w = tf.cast(resize_scale * tf.cast(w, tf.float32), tf.int32)
    new_h = tf.cast(resize_scale * tf.cast(h, tf.float32), tf.int32)

    #img = tf.expand_dims(img, axis=0)
    img = tf.image.resize(img, (new_h, new_w))

    pad_h = [(target_h - new_h) // 2, target_h - new_h - (target_h - new_h) // 2]
    pad_w = [(target_w - new_w) // 2, target_w - new_w - (target_w - new_w) // 2]
    img = tf.pad(img, [[0, 0], pad_h, pad_w, [0,0]], constant_values=128)

    return img
