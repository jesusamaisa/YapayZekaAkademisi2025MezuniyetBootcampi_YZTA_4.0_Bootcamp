# Kütüphaneleri yüklüyoruz (import library)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import cv2
import os

from tqdm import tqdm

# KMP duplicate library hatası için
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Verileri yüklüyoruz (load data)
labels = ["PNEUMONIA","NORMAL"]
img_size = 150 #150 X 150

def getTrainingData(data_dir):
    data = []
    for label in labels: # NORMAL
        path = os.path.join(data_dir,label) # C:\Users\muham\OneDrive\Desktop\Mezuniyet bootcampi\chest_xray\chest_xray\test\NORMAL
        class_num = labels.index(label) # ["PNEUMONIA" -> 0,"NORMAL" ->1 ]
        for img in tqdm(os.listdir(path)): # C:\Users\muham\OneDrive\Desktop\Mezuniyet bootcampi\chest_xray\chest_xray\test\NORMAL\IM-0001-0001.jpeg ....
            # print(img) ile çekilenleri gözlemleriz
            try:
                # görüntüyü okuyup işleyeceğiz
                img_arr = cv2.imread(os.path.join(path,img),cv2.IMREAD_GRAYSCALE) # Görüntüyü okumak için
                if img_arr is None:
                    print("Görsel okuma hatası")
                    continue
                # Görüntüyü yeniden boyutlandıracağız
                resized_arr = cv2.resize(img_arr, (img_size, img_size))
                
                # Veriyi listeye ekle
                data.append([resized_arr,class_num])
            except Exception as e:
                print("Hata: ",e)

    return np.array(data,dtype=object)                

train = getTrainingData("C://Users//muham//OneDrive//Desktop//Mezuniyet bootcampi//chest_xray//chest_xray//train")
test = getTrainingData("C://Users//muham//OneDrive//Desktop//Mezuniyet bootcampi//chest_xray//chest_xray//test")
val = getTrainingData("C://Users//muham//OneDrive//Desktop//Mezuniyet bootcampi//chest_xray//chest_xray//val")

# Veri Görselleştirme ve ön işleme yapıyoruz (data visualization and preprocessing)
l = []
for i in train:
    if(i[1] == 0):
        l.append("PNEUMONIA")
    else:
        l.append("NORMAL")

sns.countplot(x=l)
plt.show()

x_train = []
y_train = []

x_test = []
y_test = []

x_val = []
y_val = []

for feature, label in train:
    x_train.append(feature)
    y_train.append(label)
    
for feature, label in test:
    x_test.append(feature)
    y_test.append(label)

for feature, label in val:
    x_val.append(feature)
    y_val.append(label)

plt.figure()
plt.imshow(train[0][0], cmap="gray")
plt.title(labels[train[0][1]])
plt.show()

plt.figure()
plt.imshow(train[-1][0], cmap="gray")
plt.title(labels[train[-1][1]])
plt.show()

# Normalizasyon [0, 1] arasında scale etmek
# [0,255] / 255 = [0,1]
x_train = np.array(x_train)/255
x_test = np.array(x_test)/255
x_val = np.array(x_val)/255

# (a,b,c) ----> (a,b,c,d)
x_train = x_train.reshape(-1, img_size, img_size, 1)
x_test = x_test.reshape(-1, img_size, img_size, 1)
x_val = x_val.reshape(-1, img_size, img_size, 1)

y_train = np.array(y_train)
y_test = np.array(y_test)  # Burada y_trainest yazılmış, y_test olarak düzelttim
y_val = np.array(y_val)

# Veri Çoğaltma yapıyoruz (data augmentation)
datagen = ImageDataGenerator(
    featurewise_center = False, #Veri setinin genel ortalamasını 0 yapar
    samplewise_center = False, # Her bir örneğin ortalamasını 0 yapar
    featurewise_std_normalization = False, #Veriyi verinin std bölme
    samplewise_std_normalization = False, # Her bir örneği kendi std sapmasına bölme işlemi
    zca_whitening = False, #zca beyazlatma yöntemi, korelasyonu azaltma
    rotation_range = 30, #resimleri X derece rastgele döndürür
    zoom_range = 0.2, #rastgele yakınlaştırma işlemi
    width_shift_range = 0.1, #yatay olarak rastgele kaydırma
    height_shift_range = 0.1, #resimleri dikey olarak rastgele kaydırır
    horizontal_flip = True, #resimleri rastgele yatay çevirir
    vertical_flip = True, #resimleri rastgele dikey çevirir
    )
datagen.fit(x_train)

# Derin Öğrenme Modelimizi oluşturacağız (create deep learning model and train)

'''
Model olarak ekleyebileceğimiz neler olabilir

Feature Extraction Bloğumuz:
    (conv2d - Normalizasyon - Maxpooling)
    (conv2d - dropout - Normalizasyon - MaxPooling)
    (conv2d - Normalizasyon - Maxpooling)
    (conv2d - dropout -Normalizasyon - MaxPooling)
    (conv2d - dropout -Normalizasyon - MaxPooling)(conv2d - dropout -Normalizasyon - MaxPooling)
Classification Bloğumuz:
    flatten - Dense - Dropout - Dense (output)
Compiler: optimizer(rmsprop), loss(binary cross ent.), metric (accuracy)
'''

model = Sequential()
model.add(Conv2D(32,(7,7), strides=1,padding="same",activation="relu",input_shape= (150,150,1)))
model.add(BatchNormalization())
model.add(MaxPool2D((2,2),strides=2,padding="same"))

model.add(Conv2D(64,(5,5),strides=1,padding="same",activation="relu"))
model.add(Dropout(0.1))
model.add(MaxPool2D((2,2),strides=2,padding="same"))

model.add(Conv2D(64, (5,5), strides=1,padding="same",activation="relu"))
model.add(BatchNormalization())
model.add(MaxPool2D((2,2),strides=2,padding="same"))

model.add(Conv2D(128,(3,3),strides=1,padding="same",activation="relu"))
model.add(Dropout(0.2))
model.add(BatchNormalization())
model.add(MaxPool2D((2,2),strides=2,padding="same"))
 
model.add(Conv2D(256,(3,3),strides=1,padding="same",activation="relu"))
model.add(Dropout(0.2))
model.add(BatchNormalization())
model.add(MaxPool2D((2,2),strides=2,padding="same"))

#Yukarıda biz görüntüyü matrise çevirdik şimdi düzleştirmemiz gerekiyor
model.add(Flatten())
model.add(Dense(units=128,activation="relu")) #relu kullanmamızın sebebi train aşamasında türevlenebilir bir fonksiyon olduğu için hızlı
model.add(Dropout(0.2))
model.add(Dense(units=1,activation="sigmoid"))

model.compile(optimizer="rmsprop",loss="binary_crossentropy",metrics=["accuracy"])
model.summary()

learning_rate_reduction = ReduceLROnPlateau(monitor="val_accuracy",patience=2,verbose=1,factor=0.3,min_lr=0.000001)
epoch_number = 10
history = model.fit(datagen.flow(x_train,y_train, batch_size = 32), epochs = epoch_number, validation_data = datagen.flow(x_val,y_val),callbacks= [learning_rate_reduction])

print("Loss of Model: ",model.evaluate(x_test,y_test)[0])
print("Accuracy of Model: ",model.evaluate(x_test,y_test)[1]*100)

# Modelimizi değerlendireceğiz (evaluation)

# Eğitim geçmişini görselleştirme
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

# Model kaydetme
model.save('lung_cancer_detection_model.h5')
print("Model kaydedildi!")