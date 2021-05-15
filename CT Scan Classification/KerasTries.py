import keras
import numpy as np
import os
import time
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf

SIZE = 50
MODEL_PATH = r"E:\KerasNASLARGENOWEIGHTSHigherAugument"


def diagram(hist, fileName):
    plt.plot(hist.history["sparse_categorical_accuracy"])
    plt.plot(hist.history["val_sparse_categorical_accuracy"])
    plt.plot(hist.history["loss"])
    plt.plot(hist.history["val_loss"])
    plt.title("model accuracy & loss")
    plt.ylabel("accuracy & loss")
    plt.xlabel("epoch")
    plt.legend(["train_accuracy", "validation_accuracy", "train_loss", "validation_loss"], loc="upper left")
    plt.show()
    plt.savefig(MODEL_PATH + "\\" + fileName)


def kerasModel():
    data_augmentation = keras.Sequential(
        [tf.keras.layers.experimental.preprocessing.RandomFlip("horizontal",
                                                               input_shape=(SIZE,
                                                                            SIZE,
                                                                            3)),
         tf.keras.
             layers.experimental.preprocessing.RandomZoom(0.1),
         tf.keras.
             layers.experimental.preprocessing.RandomRotation(0.1)
         ]
    )
    base_model = keras.applications.ResNet152V2(include_top=False,
                                                weights='imagenet',  # Load weights pre-trained on ImageNet.
                                                input_shape=(SIZE, SIZE,
                                                             3))
    base_model.trainable = False
    number_of_classes = 3
    inputs = keras.Input(shape=(SIZE,
                                SIZE,
                                3))
    x = data_augmentation(inputs)
    norm_layer = keras.layers.experimental.preprocessing.Normalization()
    mean = np.array([127.5] * 3)
    var = mean ** 2
    x = norm_layer(x)
    norm_layer.set_weights([mean, var])
    x = base_model(x, training=False)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.2)(x)
    initializer = tf.keras.initializers.GlorotUniform(seed=42)
    activation = None  # tf.keras.activations.sigmoid or softmax
    outputs = keras.layers.Dense(number_of_classes,
                                 kernel_initializer=initializer,
                                 activation=activation)(x)
    model = keras.Model(inputs, outputs)
    model.compile(optimizer=keras.optimizers.Adam(),
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # default from_logits=False
                  metrics=[keras.metrics.SparseCategoricalAccuracy()])
    return model


def kerasModelTrainable():
    data_augmentation = keras.Sequential(
        [tf.keras.layers.experimental.preprocessing.RandomFlip("horizontal",
                                                               input_shape=(SIZE,
                                                                            SIZE,
                                                                            3)),
         tf.keras.
             layers.experimental.preprocessing.RandomZoom(0.15, fill_mode="constant"),
         tf.keras.
             layers.experimental.preprocessing.RandomRotation(0.15, fill_mode="constant"),
         tf.keras.
             layers.experimental.preprocessing.RandomTranslation(0.15, 0.15, fill_mode="constant")
         ]
    )
    base_model = keras.applications.NASNetLarge(include_top=False,
                                                weights=None,  # Train from 0
                                                input_shape=(SIZE, SIZE,
                                                             3), classes=3)
    base_model.trainable = True
    number_of_classes = 3
    inputs = keras.Input(shape=(SIZE,
                                SIZE,
                                3))
    x = data_augmentation(inputs)
    norm_layer = keras.layers.experimental.preprocessing.Normalization()
    mean = np.array([127.5] * 3)
    var = mean ** 2
    x = norm_layer(x)
    norm_layer.set_weights([mean, var])
    x = base_model(x, training=True)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.2)(x)
    initializer = tf.keras.initializers.GlorotUniform(seed=42)
    activation = None
    outputs = keras.layers.Dense(number_of_classes,
                                 kernel_initializer=initializer,
                                 activation=activation)(x)
    model = keras.Model(inputs, outputs)
    model.compile(optimizer=keras.optimizers.Adam(),
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # default from_logits=False
                  metrics=[keras.metrics.SparseCategoricalAccuracy()])
    return model


# region PATHS
PATH = r"C:\Users\radu_\Desktop\An2\IA\ai-unibuc-23-31-2021"
test_csv = np.genfromtxt(PATH + "/test.txt", dtype=None, encoding=None)
train_csv = np.genfromtxt(PATH + "/train.txt", delimiter=",", dtype=None, encoding=None)
validation_csv = np.genfromtxt(PATH + "/validation.txt", delimiter=",", dtype=None, encoding=None)
# endregion
# region Initializare liste
imagini_train, imagini_validare, imagini_test = [], [], []
train_csv = {k: v for (k, v) in train_csv}
validation_csv = {k: v for (k, v) in validation_csv}
train_labels = []
validation_labels = []
# endregion
# region Incarcare imagini train si validare
for numeImagine in os.listdir(PATH + "/train"):
    imagine = Image.open(PATH + "/train/" + numeImagine)
    imagine = imagine.convert('RGB')
    imagine = np.array(imagine).astype('d')
    train_labels.append(train_csv[numeImagine])
    imagini_train.append(imagine)

for numeImagine in os.listdir(PATH + "/validation"):
    imagine = Image.open(PATH + "/validation/" + numeImagine)
    imagine = imagine.convert('RGB')
    imagine = np.array(imagine).astype('d')
    validation_labels.append(validation_csv[numeImagine])
    imagini_validare.append(imagine)
imagini_train = np.array(imagini_train)
imagini_validare = np.array(imagini_validare)
train_labels = np.array(train_labels)
validation_labels = np.array(validation_labels)

nume_imagini = []
i = 0
ordine = dict()
for numeImagine in os.listdir(PATH + "/test"):
    imagine = Image.open(PATH + "/test/" + numeImagine)
    imagine = imagine.convert('RGB')
    imagine = np.array(imagine).astype('d')
    imagini_test.append(imagine)
    ordine[numeImagine] = i
    i += 1
    nume_imagini.append(numeImagine)
imagini_test = np.array(imagini_test)
# endregion
print(np.max(imagini_validare))
train_labels = np.array(train_labels)
validation_labels = np.array(validation_labels)
print("Finished loading and preprocessing the data")

estimator = kerasModelTrainable()
checkpoint_path = MODEL_PATH + r"\cp.ckpt"
loadCheck = r"E:\KerasNASLARGENOWEIGHTS2" + r"\cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 save_best_only=True,
                                                 period=1,
                                                 verbose=1)

earlystopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss",
                                                 mode="min", patience=40,
                                                 restore_best_weights=True)

# estimator.load_weights(loadCheck)
# Train the new part of the model
hist1 = estimator.fit(imagini_train, train_labels, epochs=1000, validation_data=(imagini_validare, validation_labels),
                      callbacks=[earlystopping, cp_callback])
answer = estimator.predict(imagini_test)
np.save(MODEL_PATH + r"\PredictFileBeforeLastTrain", answer)
validation_predict = estimator.predict(imagini_validare)
np.save(MODEL_PATH + r"\PredictFileValidareBeforeLastTrain", validation_predict)
try:
    print(min(hist1.history["val_loss"]))
except:
    pass
# Try to squeeze a little bit more
# estimator.trainable = True
print("Finished training the first part")
estimator.compile(optimizer=keras.optimizers.Adam(1e-5),
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # default from_logits=False
                  metrics=[keras.metrics.SparseCategoricalAccuracy()])
earlystopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss",
                                                 mode="min", patience=10,
                                                 restore_best_weights=True)
hist2 = estimator.fit(imagini_train, train_labels, epochs=1000, validation_data=(imagini_validare, validation_labels),
                      callbacks=[earlystopping, cp_callback])
answer = estimator.predict(imagini_test)
validation_predict = estimator.predict(imagini_validare)
np.save(MODEL_PATH + r"\PredictFileValidare", validation_predict)
np.save(MODEL_PATH + r"\PredictFile", answer)
try:
    print("Dupa al 2-lea train")
    print(min(hist2.history["val_loss"]))
except:
    pass
diagram(hist1, "BeforeFineTuning.png")
diagram(hist2, "AfterFineTuning.png")


"""
Option 1:
activation = sigmoid or softmax
loss =SparseCategoricalCrossentropy()
accuracy metric= SparseCategoricalAccuracy()
Option 2:
activation = None
loss =SparseCategoricalCrossentropy(from_logits=True)
accuracy metric= SparseCategoricalAccuracy()
"""
