import tensorflow as tf
import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

sess = tf.InteractiveSession()

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