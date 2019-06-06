#TODO: select 1 hash type to augment
#TODO: get objective comparison hash type

with open('filename.pickle', 'rb') as handle:
  b = pickle.load(handle)


  if FLAGS.original_image is None or FLAGS.compared_image is None:
    print('\nUsage: python msssim.py --original_image=original.png --compared_image=distorted.png\n\n')
    return

  if not tf.gfile.Exists(FLAGS.original_image):
    print('\nCannot find --original_image.\n')
    return

  if not tf.gfile.Exists(FLAGS.compared_image):
    print('\nCannot find --compared_image.\n')
    return

  with tf.gfile.FastGFile(FLAGS.original_image) as image_file:
    img1_str = image_file.read()
  with tf.gfile.FastGFile(FLAGS.compared_image) as image_file:
    img2_str = image_file.read()

  input_img = tf.placeholder(tf.string)
  decoded_image = tf.expand_dims(tf.image.decode_png(input_img, channels=3), 0)

  with tf.Session() as sess:
    img1 = sess.run(decoded_image, feed_dict={input_img: img1_str})
    img2 = sess.run(decoded_image, feed_dict={input_img: img2_str})

  print(MultiScaleSSIM(img1, img2, max_val=255)

def main(_):