import numpy as np
import os
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


MODEL_PATH = r"E:\KerasNASLARGENOWEIGHTS3"
answer = np.load(MODEL_PATH+r"\PredictFile.npy")
submission_path = MODEL_PATH + r"\submissionFile" + ".txt"
i = 0
ordine = dict()
for numeImagine in os.listdir(PATH + "/test"):
    ordine[numeImagine] = i
    i += 1

with open(submission_path, 'w+') as f:
    f.write("id,label\n")
    for numeImagine in test_csv:
        f.write(f"{numeImagine},{np.argmax(answer[ordine[numeImagine]])}\n")
print("Finished writing")