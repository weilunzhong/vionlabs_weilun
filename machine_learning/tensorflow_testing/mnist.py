import tensorflow as tf
import input_data

# variable creation func
def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

# func that defines the layer
def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding= 'SAME')


def regression_approach():
	# None for batch size and 784 is the image size flattened, 10 digits for classification
	x = tf.placeholder("float", shape=[None, 784])
	y_ = tf.placeholder("float", shape=[None, 10])

	# init of weights and bias
	W = tf.Variable(tf.zeros([784,10]))
	b = tf.Variable(tf.zeros([10]))

	# init vairables in a session
	sess.run(tf.initialize_all_variables())

	# predictions
	y = tf.nn.softmax(tf.matmul(x, W) + b)

	# cost func set to be cross entropy
	cross_entropy = -tf.reduce_sum(y_ * tf.log(y))

	# training happens after all is defined and steepest gradient descent is used
	train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

	for i in range(1000):
		batch = mnist.train.next_batch(50)
		train_step.run(feed_dict={x: batch[0], y_: batch[1]})

	# evaluate model
	correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

	accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
	print accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels})

def cnn_approach():
	x = tf.placeholder("float", shape=[None, 784])
	y_ = tf.placeholder("float", shape=[None, 10])
	x_image = tf.reshape(x, [-1,28,28,1])

	#first layer
	W_conv1 = weight_variable([5,5,1,32])
	b_conv1 = bias_variable([32])

	# 1st layer
	h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
	h_pool1 = max_pool_2x2(h_conv1)

	#second layer
	W_conv2 = weight_variable([5, 5, 32, 64])
	b_conv2 = bias_variable([64])

	h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
	h_pool2 = max_pool_2x2(h_conv2)

	# fully connected layer
	W_fc1 = weight_variable([7 * 7 * 64, 1024])
	b_fc1 = bias_variable([1024])

	h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
	h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

	# dropout
	prob = tf.placeholder("float")
	h_fc1_drop = tf.nn.dropout(h_fc1, prob)

	#readout layer
	W_fc2 = weight_variable([1024, 10])
	b_fc2 = bias_variable([10])

	#softmax layer
	y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)


	cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
	train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
	correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
	sess.run(tf.initialize_all_variables())
	for i in range(20000):
		batch = mnist.train.next_batch(50)
		if i%100 == 0:
			train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], prob: 1.0})
			print "step %d, training accuracy %g"%(i, train_accuracy)
		train_step.run(feed_dict={x: batch[0], y_: batch[1], prob: 0.5})

	print "test accuracy %g"%accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, prob: 1.0})


if __name__ == "__main__":
	mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
	sess = tf.InteractiveSession()
	#regression_approach()
	cnn_approach()

