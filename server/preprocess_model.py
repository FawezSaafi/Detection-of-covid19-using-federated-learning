
from keras.applications.vgg16 import VGG16
from keras.layers import Flatten
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import vgg16
from keras.layers import Dense
import pandas as pd
import os
from sklearn.model_selection import train_test_split


def preprocess(data_path, number):  # data_path
    i=0
    df = pd.DataFrame(columns=['label', 'path'])

    for filename in os.listdir(data_path + "/covid"):
        i=i+1
        df.loc[i] = ["covid", data_path + "/covid/" + filename]

    for filename in os.listdir(data_path + "/normal"):
        i=i+1
        df.loc[i] = ["normal", data_path + "/normal/" + filename]

    train_df, test_valid_df = train_test_split(df,
                                               test_size=0.20,
                                               random_state=40,
                                               stratify=df[['label']])


    test_df, val_df = train_test_split(test_valid_df,
                                       test_size=0.50,
                                       random_state=40)




    train_data_gen = ImageDataGenerator(preprocessing_function=vgg16.preprocess_input, zoom_range=0.2,
                                        horizontal_flip=True, shear_range=0.2, rescale=1. / 255)
    train = train_data_gen.flow_from_dataframe(dataframe=train_df, x_col="path", y_col="label",
                                               target_size=(224, 224))
    validation_data_gen = ImageDataGenerator(preprocessing_function=vgg16.preprocess_input, rescale=1. / 255)
    valid = validation_data_gen.flow_from_dataframe(dataframe=val_df, x_col="path", y_col="label",
                                                    target_size=(224, 224))
    test_data_gen = ImageDataGenerator(preprocessing_function=vgg16.preprocess_input, rescale=1. / 255)
    test = test_data_gen.flow_from_dataframe(dataframe=test_df, x_col="path", y_col="label",
                                             target_size=(224, 224), shuffle=False)
    return train, test, valid



def vgg_model():
    vgg = VGG16(input_shape=(224, 224, 3), include_top=False)
    for layer in vgg.layers:  # Don't train the parameters again
        layer.trainable = False
    x = Flatten()(vgg.output)
    x = Dense(units=2, activation='sigmoid', name='predictions')(x)

    model = Model(vgg.input, x)
    return model


