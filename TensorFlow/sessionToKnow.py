import tensorflow as tf

matrix1 = tf.constant([[3,3]])
matrix2 = tf.constant([[2],[2]])

product = tf.matmul(matrix1, matrix2)

# method 1
sess = tf.Session()
result = sess.run(product)
print(result)
sess.close()

# method 2
with tf.Session() as sess:
    result2 = sess.run(product)
    print(result2)

state = tf.Variable(0, name='counter')
print(state.name)
one = tf.constant(1)

new_value = tf.add(state, one)  # new version: new_value = state + 1
update = tf.assign(state, new_value)

init = tf.global_variables_initializer()    # must have if define variable

with tf.Session() as sess:
    sess.run(init)
    for _ in range(3):
        sess.run(update)
        print(sess.run(state))

input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)

output = input1 * input2

with tf.Session() as sess:
    print(sess.run(output, feed_dict={input1:[7.], input2:[2.0]}))