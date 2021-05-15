import numpy as np
import os
import time
import matplotlib.pyplot as plt
from PIL import Image
from scipy import stats
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler, Normalizer, MinMaxScaler
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC

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
    imagine = np.array(imagine).flatten()
    train_labels.append(train_csv[numeImagine])
    imagini_train.append(imagine)

for numeImagine in os.listdir(PATH + "/validation"):
    imagine = Image.open(PATH + "/validation/" + numeImagine)
    imagine = np.array(imagine).flatten()
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
    imagine = plt.imread(PATH + "/test/" + numeImagine)
    imagine = np.array(imagine).flatten()
    imagini_test.append(imagine)
    ordine[numeImagine] = i
    i += 1
    nume_imagini.append(numeImagine)
imagini_test = np.array(imagini_test)
# endregion
# print(len(imagini_train), len(imagini_validare), len(imagini_test))

full_data = np.append(imagini_train, imagini_validare, 0)
full_data = np.append(full_data, imagini_test, 0)


toScale, toNormalize = True, False
if toNormalize:
    normalizer = Normalizer()
    normalizer.fit(full_data)
    imagini_train = normalizer.transform(imagini_train)
    imagini_validare = normalizer.transform(imagini_validare)
    imagini_test = normalizer.transform(imagini_test)
if toScale:
    scaler = MinMaxScaler()
    imagini_train = scaler.fit_transform(imagini_train)
    imagini_validare = scaler.fit_transform(imagini_validare)
    imagini_test = scaler.fit_transform(imagini_test)
print(np.max(imagini_validare))
train_labels = np.array(train_labels)
validation_labels = np.array(validation_labels)
print("Finished loading and preprocessing the data")
nbs = [MLPClassifier(max_iter=400)]
acc = []
for nb in nbs:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"Started training {str(nb)} at {current_time}")
    print(f"Training the model...")
    nb.fit(imagini_train, train_labels)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"Finished training at {current_time}.")
    print(nb.get_params(deep=True))
    print("Calculating accuracy...")
    temp = nb.score(imagini_validare, validation_labels)
    print(f"Accuracy for  {str(nb)}: {temp}")
    acc.append((temp, str(nb)))
    print("Predicting....")
    answer = nb.predict(imagini_test)
    print("Writing to file...")
    submission_path = r"E:\PyCharmProjects\IA\submission" + str(temp)+str(nb) + ".txt"
    with open(submission_path, 'w+') as f:
        f.write("id,label\n")
        for numeImagine in test_csv:
            f.write(f"{numeImagine},{answer[ordine[numeImagine]]}\n")
    print("Finished writing")
print(max(acc))

"""Decision tree try
print("Predicting....")
answer = nb.predict(imagini_test)
print("Writing to file...")
with open(r"E:\PyCharmProjects\IA\submission.txt", 'w+') as f:
    f.write("id,label\n")
    for numeImagine in test_csv:
        f.write(f"{numeImagine},{answer[ordine[numeImagine]]}\n")
print("Finished writing")
acc = []
for depth in range(1,20):
    nb = DecisionTreeClassifier(max_depth=depth)
    print(f"Training the model for max_depth {depth} ...")
    nb.fit(imagini_train, train_labels)
    print("Finished training.")
    print("Calculating accuracy...")
    temp = nb.score(imagini_validare, validation_labels)
    print(f"Accuracy for max_depth {depth} : {temp}")
    acc.append((temp, depth))
print(max(acc), min(acc)) #Max 0.537 pentru depth=5
"""
"""KNeighbours try
acc = []
for neighbours in range(1,20):
    nb = KNeighborsClassifier(neighbours, weights="distance")
    print(f"Training the model for {neighbours} neighbours...")
    nb.fit(imagini_train, train_labels)
    print("Finished training.")
    print("Calculating accuracy...")
    temp = nb.score(imagini_validare, validation_labels)
    print(f"Accuracy for {neighbours} neighbours: {temp}") 
    acc.append((temp, neighbours))
print(max(acc), min(acc))
"""
# GaussianMB - 0,455 cu normalizare+scalare inainte
# KNeighbours - max 0,442 pe testele de validare pt 19 vecini (probabil overfitting), majoritatea intre 0,42-0,43
# DecisionTreeClassifier Max 0.537 pentru depth=5 fara preprocesare(best so far), dupa incepe sa scada, 0.514 pt depth=15 cu preprocesare (probabil overfitting)
# MLPClassifier(random_state=1, max_iter=300) - 0.4653333333333333
# SVC 0.457
