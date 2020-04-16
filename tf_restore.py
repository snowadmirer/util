#得到该网络中，所有可以加载的参数
variables = tf.contrib.framework.get_variables_to_restore()
#删除output层中的参数
variables_to_resotre = [v for v in varialbes if v.name.split('/')[0]!='output']
#构建这部分参数的saver
saver = tf.train.Saver(variables_to_restore)
saver.restore(sess,'model.ckpt')
