from statistics import mode
import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split

from datetime import datetime
from playsound import playsound
from matplotlib import pyplot as plt 


class minmax_norm:

    def __init__(self,df_input):
        self.mins = df_input.min()
        self.maxs = df_input.max()
        self.minmax_norm_df = (df_input - self.mins) / (self.maxs - self.mins)

    def denorm(self, colum_df):
        print(type(pd.DataFrame()))
        columns = ''
        if type(colum_df) == type(pd.DataFrame()):
            columns = colum_df.columns
        elif type(colum_df) == type(pd.Series()):
            columns = colum_df.name
        else:
            raise Exception('Invalid type of parameter')
        return colum_df * (self.maxs[columns] - self.mins[columns]) + self.mins[columns]


start=datetime.now()
try:

    training_df = pd.read_csv("../trainingRN1.csv", sep="\t", decimal=",")
    training_df.dropna(inplace=True)
    norm = minmax_norm(training_df.iloc[:,1:])
    training_df = norm.minmax_norm_df
    X_train, X_test, y_train, y_test = train_test_split(training_df.iloc[:,1:-1],training_df.iloc[:,-1:], test_size=0.2, shuffle=False)
    input_shape = (X_train.shape [1] ,) 

    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)
    print(input_shape)

    model = Sequential()
    model.add(Dense(50, input_shape=input_shape, activation="relu"))
    model.add(Dropout(0.1))
    model.add(Dense(20, activation="relu"))
    model.add(Dropout(0.1))
    model.add(Dense(1, activation="relu"))
    print(model.summary())
    # opt = tf.keras.optimizers.Adam(learning_rate=1e-3, decay=1e-5)
    model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.SGD(learning_rate=0.3, momentum=0.01) , metrics=['accuracy'])
    historico = model.fit(X_train, y_train, epochs=300, batch_size=1, verbose=0, validation_split=0.2, shuffle=False)

    ## plots de evolución de loss 
    plt.plot(historico.history['loss']) 
    plt.title('model loss') 
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left') 
    plt.show()

except Exception as e:
    playsound('../error.mp3',True)
    duration=datetime.now()-start
    print("Duracion Error: ",duration)
    raise e

duration=datetime.now()-start
print("Training test completed in: ",duration)

playsound('../ok.mp3',True)