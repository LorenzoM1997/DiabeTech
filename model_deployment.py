import tensorflow as tf
import numpy as np
import random
import pymysql
import sched, time
import datetime

def update():
    conn = pymysql.connect(host = "us-cdbr-iron-east-05.cleardb.net", user = "b775d3dbad5185", password="e5f86bf8", database = "heroku_4060b21460e1636", charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from diabetes_app_users")
    for user in cur.fetchall():
        cur2 = conn.cursor()
        cur2.execute("SELECT * from (select * from diabetes_app_training_data WHERE User_id = %s LIMIT 0, 250) as T UNION (select * from diabetes_app_training_data ORDER BY rand() LIMIT 0, 500)", (user[0]))
        for i in cur2.fetchall():
            print(i)

def testing(input_data,W1_s, W2_s, b1_s, b2_s):
    x = tf.placeholder(tf.float32, [None, 15])
    W1 = tf.placeholder(tf.float32, [15, 5])
    W2 = tf.placeholder(tf.float32, [5, 1])
    b1 = tf.placeholder(tf.float32, [5])
    b2 = tf.placeholder(tf.float32, [1])
    h1 = tf.nn.relu(tf.matmul(x, W1) + b1)
    p = tf.nn.relu(tf.matmul(h1, W2) + b2)
    sess = tf.InteractiveSession()
    inputs = np.reshape(np.copy(input_data),(1,15))
    values = np.zeros(0)
    inputs[0,0] = inputs[0,1]
    for _ in range(18):
        inputs[0,0] += 10
        v = sess.run(p, feed_dict={x: inputs,
                                            W1: W1_s,
                                            W2: W2_s,
                                            b1: b1_s,
                                            b2: b2_s})
        values = np.append(values, v)
    
    return values

def prediction(user, weights):
    time = user[1].seconds / 60
    code = user[3]
    code2 = user[4]
    value = user[5]
    input_data = np.zeros((1,15))
    input_data[0,1] = time
    input_data[0,code] = 1
    input_data[0,code2] = 1
    input_data[0,14] = value
    W1 = np.reshape(weights[:75], (15,5))
    W2 = np.reshape(weights[75:80], (5,1))
    b1 = weights[80:85]
    b2 = np.reshape(weights[85], (1,))
    return testing(input_data, W1, W2, b1, b2)

def training(W1, W2, b1, b2):
    npzfile = np.load("small_but_prettier_dataset.npz")
    data = np.reshape(npzfile['arr_0'], (-1, 15))
    input_data = np.copy(data[1:]).astype(float)
        
    output_data = np.zeros((0,1))
    prev_row = None
    first_row = True
    size = len(input_data)
    i = 1
    while i < size:
        curr = i
        prev = i-1
        if input_data[prev][0] == input_data[curr][0]:
            input_data[prev][0] = input_data[curr][1]
            output_data = np.append(output_data, input_data[curr][14])
            i += 1
        else:
            input_data = np.delete(input_data, prev, 0)
        if i == len(input_data):
            break

    output_data = np.append(output_data, input_data[curr][14])
    output_data = np.reshape(output_data, (-1,1))

    x = tf.placeholder(tf.float32, [None, 15])
    W1 = tf.placeholder(tf.float32, [15, 5])
    W2 = tf.placeholder(tf.float32, [5, 1])
    b1 = tf.placeholder(tf.float32, [5])
    b2 = tf.placeholder(tf.float32, [1])
    h1 = tf.nn.relu(tf.matmul(x, W1) + b1)
    p = tf.nn.relu(tf.matmul(h1, W2) + b2)

    #the expected output matrix
    y = tf.placeholder(tf.float32, [None, 1])

    squared_deltas = tf.square(p - y)
    loss = tf.reduce_mean(squared_deltas)

    lr = 0.001
    train_step = tf.train.RMSPropOptimizer(lr).minimize(loss)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    for i in range(200000):
        aslice = random.randint(0,len(input_data)-101)
        batch_xs = input_data[aslice:aslice+100]
        batch_ys = output_data[aslice:aslice+100]
        sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys})
    W1_s = sess.run(W1)
    W2_s = sess.run(W2)
    b1_s = sess.run(b1)
    b2_s = sess.run(b2)

def request_for_prediction(s,conn): 
    
    cur = conn.cursor()
    cur.execute("select * from diabetes_app_training_data where User_id= 1")
    user = cur.fetchone()
    cur2 = conn.cursor()
    cur2.execute("select W1,W2,W3,W4,W5,W6,W7,W8,W9,W10,W11,W12,W13,W14,W15,W16,W17,W18,W19,W20,W21,W22,W23,W24,W25,W26,W27,W28,W29,W30,W31,W32,W33,W34,W35,W36,W37,W38,W39,W40,W41,W42,W43,W44,W45,W46,W47,W48,W49,W50,W51,W52,W53,W54,W55,W56,W57,W58,W59,W60,W61,W62,W63,W64,W65,W66,W67,W68,W69,W70,W71,W72,W73,W74,W75,W76,W77,W78,W79,W80,W81,W82,W83,W84,W85,W86 from diabetes_app_user_weights ORDER BY time_stamp ASC LIMIT 0,1")
    weights = cur2.fetchone()
    v = prediction(user, weights)
    string = ""
    for i in range(len(v)-1):
        string += "t"+str(i+1)+"="+str(v[i])+","
    string += "t18="+str(v[i])
    cur3 = conn.cursor()
    string = "update diabetes_app_user_display_data set "+string+" where User_id = 1"
    print("done")
    cur3.execute(string)
    conn.commit()
    
    s.enter(3, 1, request_for_prediction, (s,conn))

def main():
    conn = pymysql.connect(host = "us-cdbr-iron-east-05.cleardb.net", user = "b775d3dbad5185", password="e5f86bf8", database = "heroku_4060b21460e1636", charset='utf8')
    """cur = conn.cursor()
    cur.execute("insert into diabetes_app_user_weights (W1,W2,W3,W4,W5,W6,W7,W8,W9,W10,W11,W12,W13,W14,W15,W16,W17,W18,W19,W20,W21,W22,W23,W24,W25,W26,W27,W28,W29,W30,W31,W32,W33,W34,W35,W36,W37,W38,W39,W40,W41,W42,W43,W44,W45,W46,W47,W48,W49,W50,W51,W52,W53,W54,W55,W56,W57,W58,W59,W60,W61,W62,W63,W64,W65,W66,W67,W68,W69,W70,W71,W72,W73,W74,W75,W76,W77,W78,W79,W80,W81,W82,W83,W84,W85,W86, User_id, time_stamp) VALUES (0.467172,0.467172,0.574407,0.574407,0.271868,-0.600734,-0.600734,-0.467715,-0.467715,-0.618343,0.0666067,0.0666067,-0.0159075,-0.0159075,0.00923896,7.55717,7.55717,7.29731,7.29731,8.21297,1.0,1.0,1.0,1.0,1.0,5.09837,5.09837,5.82199,5.82199,6.01926,-57.658,-57.658,-51.5672,-51.5672,-51.0096,-12.8693,-12.8693,-11.4535,-11.4535,-11.2544,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,-0.203572,-0.203572,0.157962,0.157962,0.0803116,1.01721,1.01721,0.515274,0.515274,-1.39671,2.27564,2.27564,2.32176,2.32176,3.15193677,1.37725105,1,%s )",(datetime.datetime.now(),))
    
    conn.commit()"""
    
    s = sched.scheduler(time.time, time.sleep)

    s.enter(0.5, 1, request_for_prediction, (s,conn))
    s.run()
    
if __name__ == "__main__":
    main()
