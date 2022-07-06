from statistics import mode
import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from datetime import datetime
from playsound import playsound
from matplotlib import pyplot as plt 





start=datetime.now()
try:

    training_df = pd.read_csv("trainingRN1.csv", sep="\t", decimal=",")
    X_train, X_test, y_train, y_test = train_test_split(training_df.iloc[:,1:-1],training_df.iloc[:,-1:], test_size=0.2, shuffle=False)
    input_shape = (6,int(X_train.shape[1]/6)) 
    X_train = np.reshape(X_train,(X_train.shape[0], 6, int(X_train.shape[1]/6)))
    X_test = np.reshape(X_test,(X_test.shape[0], 6, int(X_test.shape[1]/6)))

    print(X_train)
    print(X_test)
    print(y_train)
    print(y_test)

    # model = Sequential()

    # model.add(LSTM(150, input_shape=input_shape, return_sequences=True, dropout=0.2))

    # model.add(LSTM(150, return_sequences=True, dropout=0.2))
   
    # model.add(Dense(50, activation="relu"))
    # model.add(Dropout(0.2))

    # model.add(Dense(20, activation="relu"))
    # model.add(Dropout(0.1))
    
    # model.add(Dense(1, activation="relu"))

    # opt = tf.keras.optimizers.Adam(learning_rate=1e-3, decay=1e-5)

    # model.compile(loss='mean_squared_error', optimizer=opt, metrics=['accuracy'])

    # historico = model.fit(X_train, y_train, epochs=2, batch_size=10, verbose=1, validation_split=0.2, shuffle=False)

    # ## plots de evolución de loss y accuracy
    # plt.plot(historico.history['loss']) 
    # plt.plot(historico.history['val_loss']) 
    # plt.title('model loss') 
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'val'], loc='upper left') 
    # plt.show()









except Exception as e:
    playsound('error.mp3',True)
    duration=datetime.now()-start
    print("Duracion Error: ",duration)
    raise e

duration=datetime.now()-start
print("Training test completed in: ",duration)

playsound('ok.mp3',True)