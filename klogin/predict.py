import pandas as pd
import tensorflow as tf
import numpy as np


# 데이터 정규화
def data_standatdization(x):
    x_np = np.asarray(x)
    return (x_np - x_np.mean()) / x_np.std()

# 데이터 스케일링
def min_max_scaling(x):
    x_np = np.asarray(x)
    return (x_np - x_np.min()) / (x_np.max() - x_np.min() + 1e-7)

# 데이터 역스케일링
def reverse_min_max_scaling(org_x, x):
    org_x_np = np.asarray(org_x)
    x_np = np.asarray(x)
    return (x_np * (org_x_np.max() - org_x_np.min() + 1e-7)) + org_x_np.min()

def lstm_cell(rnn_cell_hidden_dim, forget_bias, keep_prob):
    cell = tf.contrib.rnn.BasicLSTMCell(num_units=rnn_cell_hidden_dim,
                                            forget_bias=forget_bias, state_is_tuple=True, activation=tf.nn.softsign)
    if keep_prob < 1.0:
        cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=keep_prob)
    return cell

def foresee(df):
    tf.reset_default_graph()
    input_data_column_cnt = 5  # 입력데이터의 컬럼 개수(Variable 개수)
    output_data_column_cnt = 1  # 결과데이터의 컬럼 개수

    seq_length = 90  # 1개 시퀀스의 길이(시계열데이터 입력 개수)
    rnn_cell_hidden_dim = 20  # 각 셀의 (hidden)출력 크기
    forget_bias = 1.0  # 망각편향(기본값 1.0)
    num_stacked_layers = 1  # stacked LSTM layers 개수
    keep_prob = 0.8  # dropout할 때 keep할 비율

    epoch_num = 1500  # 에폭 횟수(학습용전체데이터를 몇 회 반복해서 학습할 것인가 입력)
    learning_rate = 0.01  # 학습률"


    stock_info = df.values[1:].astype(np.float)

    ############################################################
    price = stock_info[:, :-1]
    norm_price = min_max_scaling(price)  # 가격형태 데이터 정규화 처리

    # 거래량형태 데이터를 정규화한다
    # ['Open','High','Low','Close','Adj Close','Volume']에서 마지막 'Volume'만 취함
    # [:,-1]이 아닌 [:,-1:]이므로 주의하자! 스칼라가아닌 벡터값 산출해야만 쉽게 병합 가능
    volume = stock_info[:, -1:]
    norm_volume = min_max_scaling(volume)  # 거래량형태 데이터 정규화 처리

    # 행은 그대로 두고 열을 우측에 붙여 합친다
    x = np.concatenate((norm_price, norm_volume), axis=1)  # axis=1, 세로로 합친다

    y = x[:, [-2]]  # 타켓은 주식 종가이다

    dataX = []  # 입력으로 사용될 Sequence Data
    dataY = []  # 출력(타켓)으로 사용

    for i in range(0, len(y) - seq_length):
        _x = x[i: i + seq_length]
        _y = y[i + seq_length]  # 다음 나타날 주가(정답)
        dataX.append(_x)  # dataX 리스트에 추가
        dataY.append(_y)  # dataY 리스트에 추가

    train_size = int(len(dataY) * 0.7)
    test_size = len(dataY) - train_size

    trainX = np.array(dataX[0:train_size])
    trainY = np.array(dataY[0:train_size])

    testX = np.array(dataX[train_size:len(dataX)])
    testY = np.array(dataY[train_size:len(dataY)])

    X = tf.placeholder(tf.float32, [None, seq_length, input_data_column_cnt])
    Y = tf.placeholder(tf.float32, [None, 1])

    targets = tf.placeholder(tf.float32, [None, 1])

    predictions = tf.placeholder(tf.float32, [None, 1])



    stackedRNNs = [lstm_cell(rnn_cell_hidden_dim, forget_bias, keep_prob) for _ in range(num_stacked_layers)]
    multi_cells = tf.contrib.rnn.MultiRNNCell(stackedRNNs,
                                              state_is_tuple=True) if num_stacked_layers > 1 else lstm_cell(rnn_cell_hidden_dim, forget_bias, keep_prob)

    hypothesis, _states = tf.nn.dynamic_rnn(multi_cells, X, dtype=tf.float32)

    hypothesis = tf.contrib.layers.fully_connected(hypothesis[:, -1], output_data_column_cnt, activation_fn=tf.identity)


    loss = tf.reduce_sum(tf.square(hypothesis - Y))

    optimizer = tf.train.AdamOptimizer(learning_rate)
    train = optimizer.minimize(loss)

    rmse = tf.sqrt(tf.reduce_mean(tf.squared_difference(targets, predictions)))

    train_error_summary = []  # 학습용 데이터의 오류를 중간 중간 기록한다
    test_error_summary = []  # 테스트용 데이터의 오류를 중간 중간 기록한다
    test_predict = ''  # 테스트용데이터로 예측한 결과

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    for epoch in range(epoch_num):
        _, _loss = sess.run([train, loss], feed_dict={X: trainX, Y: trainY})
        if ((epoch + 1) % 100 == 0) or (epoch == epoch_num - 1):  # 100번째마다 또는 마지막 epoch인 경우
            # 학습용데이터로 rmse오차를 구한다
            train_predict = sess.run(hypothesis, feed_dict={X: trainX})
            train_error = sess.run(rmse, feed_dict={targets: trainY, predictions: train_predict})
            train_error_summary.append(train_error)

            # 테스트용데이터로 rmse오차를 구한다
            test_predict = sess.run(hypothesis, feed_dict={X: testX})
            test_error = sess.run(rmse, feed_dict={targets: testY, predictions: test_predict})
            test_error_summary.append(test_error)

    recent_data = np.array([x[len(x) - seq_length:]])

    # 내일 종가를 예측해본다
    test_predict = sess.run(hypothesis, feed_dict={X: recent_data})

    test_predict = reverse_min_max_scaling(price, test_predict)  # 금액데이터 역정규화한다

    return test_predict[0]