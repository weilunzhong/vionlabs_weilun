import tensorflow as tf
import input_data

# variable creation func
def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial, name="weights")

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial, name="bias")

# func that defines the layer
def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME', name="conv2d")

def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME', name="pool")


def regression_approach():
	# None for batch size and 784 is the image size flattened, 10 digits for classification
	x = tf.placeholder("float", shape=[None, 784], name="x_input")
	y_ = tf.placeholder("float", shape=[None, 10], name="y_input")

	# init of weights and bias
	W = tf.Variable(tf.zeros([784,10]), name="weights")
	b = tf.Variable(tf.zeros([10]), name="bias")

	# init vairables in a session
	# sess.run(tf.initialize_all_variables())

	# predictions
	with tf.name_scope("prediction") as scope:
		y = tf.nn.softmax(tf.matmul(x, W) + b)

	w_hist = tf.histogram_summary("weights", W)
	b_hist = tf.histogram_summary("biases", b)
	y_hist = tf.histogram_summary("y", y)

	# cost func set to be cross entropy
	with tf.name_scope("cost_func") as scope:
		cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
		ce_sum = tf.scalar_summary("cross_entropy", cross_entropy)

	# training happens after all is defined and steepest gradient descent is used
	with tf.name_scope("train") as scope:
		train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

	# evaluate model
	with tf.name_scope("test") as scope:
		correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
		accuracy_summary = tf.scalar_summary("accuracy", accuracy)

	# merge all the summaries
	merged = tf.merge_all_summaries()

	# Launch the graph
	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())

		writer = tf.train.SummaryWriter('/home/vionlabs/Documents/vionlabs_weilun/machine_learning/tensorflow_testing/graph', graph_def=sess.graph_def)
		# tf.initialize_all_variables().run()

		for i in range(1000):
			if i % 10 == 0:  # Record summary data, and the accuracy
				feed = {x: mnist.test.images, y_: mnist.test.labels}
				result = sess.run([merged, accuracy], feed_dict=feed)
				summary_str = result[0]
				acc = result[1]
				writer.add_summary(summary_str, i)
				print("Accuracy at step %s: %s" % (i, acc))
			else:
				batch_xs, batch_ys = mnist.train.next_batch(100)
				feed = {x: batch_xs, y_: batch_ys}
				sess.run(train_step, feed_dict=feed)


		print accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels})

def cnn_approach():
	"""
		In a Tensorflow CNN first define I/O with placeholder
		then define the structure layer-wise 

	"""
	x = tf.placeholder("float", shape=[None, 784], name="x_input")
	y_ = tf.placeholder("float", shape=[None, 10], name="y_input")
	x_image = tf.reshape(x, [-1,28,28,1])

	#first layer
	with tf.name_scope('first_layer') as scope:
		W_conv1 = weight_variable([5,5,1,32])
		b_conv1 = bias_variable([32])
		h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
		h_pool1 = max_pool_2x2(h_conv1)

	#second layer
	with tf.name_scope('second_layer') as scope:
		W_conv2 = weight_variable([5, 5, 32, 64])
		b_conv2 = bias_variable([64])
		h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
		h_pool2 = max_pool_2x2(h_conv2)

	# fully connected layer
	with tf.name_scope('fc_layer') as scope:
		W_fc1 = weight_variable([7 * 7 * 64, 1024])
		b_fc1 = bias_variable([1024])

		h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
		h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

	# dropout
	with tf.name_scope('dropout_layer') as scope:
		prob = tf.placeholder("float")
		h_fc1_drop = tf.nn.dropout(h_fc1, prob)

	#readout layer
	with tf.name_scope('readout_layer') as scope:
		W_fc2 = weight_variable([1024, 10])
		b_fc2 = bias_variable([10])

	#softmax layer
	with tf.name_scope('softmax_layer') as scope:
		y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

	# test phase
	with tf.name_scope("cost_func") as scope:
		cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
		ce_sum = tf.scalar_summary("cross_entropy", cross_entropy)

	with tf.name_scope("training") as scope:
		train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

	with tf.name_scope("test") as scope:
		correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
		accuracy_summary = tf.scalar_summary("accuracy", accuracy)


	merged = tf.merge_all_summaries()

	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())
		writer = tf.train.SummaryWriter('/home/vionlabs/Documents/vionlabs_weilun/machine_learning/tensorflow_testing/cnn_graph', graph_def=sess.graph_def)
		for i in range(20000):
			batch = mnist.train.next_batch(50)
			if i%100 == 0:
				train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], prob: 1.0})
				print "step %d, training accuracy %g"%(i, train_accuracy)
			train_step.run(feed_dict={x: batch[0], y_: batch[1], prob: 0.5})

			# write the log at 100th iteration
			summary_str = sess.run(merged, feed_dict={x: batch[0], y_: batch[1], prob: 0.5})
			writer.add_summary(summary_str, 100*i + 1)

		print "test accuracy %g"%accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, prob: 1.0})


if __name__ == "__main__":
	mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
	#regression_approach()
	cnn_approach()
