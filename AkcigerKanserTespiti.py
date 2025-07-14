# Kütüphaneleri yüklüyoozzz (import libary)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout, BatchNormalization
from keras.callbacks import ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator
import cv2
import os
from tqdm import tqdm

# Verileri yüklüyooozzzz   (load data)
labels = ["PNEUMONIA","NORMAL"]
img_size = 150 #150 X 150

def getTrainingData(data_dir):
    data =  []
    for label in labels: # NORMAL
        path = os.path.join(data_dir,label) # C:\Users\muham\OneDrive\Desktop\Mezuniyet bootcampi\chest_xray\chest_xray\test\NORMAL
        class_num = labels.index(label) # ["PNEUMONIA" -> 0,"NORMAL" ->1 ]
        for img in tqdm(os.listdir(path)): # C:\Users\muham\OneDrive\Desktop\Mezuniyet bootcampi\chest_xray\chest_xray\test\NORMAL\IM-0001-0001.jpeg ....
            # print(img)le çekilenleri gözlemleriz
            try:
                # goruntuyu okuyup işleyecepşz
                img_arr = cv2.imread(os.path.join(path,img),cv2.IMREAD_GRAYSCALE) # Görüntüyü okumak için
                if img_arr is None:
                    print("Görsel okuma hatası")
                    continue
                # Görüntüyü yenidne bıyutlandıracazzz
                resized_arr = cv2.resize(img_arr, (img_size, img_size))
                
                # Veriyi listeye ekle
                data.append([resized_arr,class_num])
            except Exception as e:
                print("Hata: ",e)

    return  np.array(data,dtype=object)                

train = getTrainingData("C://Users//muham//OneDrive//Desktop//Mezuniyet bootcampi//chest_xray//chest_xray//train")
test = getTrainingData("C://Users//muham//OneDrive//Desktop//Mezuniyet bootcampi//chest_xray//chest_xray//test")
val = getTrainingData("C://Users//muham//OneDrive//Desktop//Mezuniyet bootcampi//chest_xray//chest_xray//val")

# Veri Göreslleştime ve ön işleme yapıyoruzzzz   (data visualization and preprocessing)
l = []
for i in train:
    if(i[1] == 0):
        l.append("PNEUMONIA")
    else:
        l.append("NORMAL")

sns.countplot(x=l)

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

plt.figure()
plt.imshow(train[-1][0], cmap="gray")
plt.title(labels[train[-1][1]])

# Normalizasyon   [0, 1] arasında scale etmek
#   [0,255] / 255 = [0,1]
x_train = np.array(x_train)/255
x_test = np.array(x_test)/255
x_val = np.array(x_val)/255

# (a,b,c) ----> (a,b,c,d)

x_train = x_train.reshape(-1, img_size, img_size, 1)
x_test = x_test.reshape(-1, img_size, img_size, 1)
x_val = x_val.reshape(-1, img_size, img_size, 1)

y_train = np.array(y_train)
y_trainest = np.array(y_test)
y_val = np.array(y_val)

# Veri Çoğaltma yapıyoruzzz (data augmentation)
datagen = ImageDataGenerator(
    featurewise_center = False, #Veri setinin genel ortalamasını 0 yapar
    samplewise_center = False, # Her bir örneğin ortalamasını 0 yapar
    featurewise_std_normalization = False, #Veriyi verinin std bölme
    samplewise_std_normalization = False, # Her bir örneği kendi std sapmasına bölme işlemi
    zca_whitening = False, #zca beyazlatma yöntemi, korelasyonu azaltma
    rotation_range = 30, #resimleri X derecce rastgele döndürür
    zoom_range = 0.2, #rastgele yakınlaştırma işleme
    width_shift_range = 0.1, #yatay olarak rastgele kaydirma
    height_shift_range = 0.1, #resimleri dikey olarak rastgele kaydirir
    horizontal_flip = True, #resimleri rastgele yatay cevirir
    vertical_flip = True, #resimleti rastgele dikey cevirir
    )
datagen.fit(x_train)



# Derin Öğrenme Modelimizi oluşturacağızzz (create deep learning model and train)

'''
Model olarak ekleyebileceğimiz neler olabilir

Feature Extraction Bloğumuz:
    (con2d - Normalizasyon - Maxpooling)
    (con2d - dropout - Normalizasyon - MaxPooling)
    (con2d - Normalizasyon - Maxpooling)
    (con2d - dropout -Normalizasyon - MaxPooling)
    (con2d - dropout -Normalizasyon - MaxPooling)(con2d - dropout -Normalizasyon - MaxPooling)
Classification Bloğumuz:
    flatten - Dense - Dropout - Dneses (output)
Complier: optimizer(rmsprop), loss(binary cross ent.), metric (accuracy)

'''
#Burada bir hata aldım hatanın çözümü terminalden aşağıdaki kodu yazıp env eklememiz gerekli çözülüyor
#import os
#os.environ['KMP_DUPLICATE_LIB_OK']='True'
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

#Yukarıda biz görünütyü matrise çevirdik şimdi düzleştirmemiz gerkiyor
model.add(Flatten())
model.add(Dense(units=128,activation="relu")) #relu kullanmamaızın sebebi train aşamasında türevlenebilir bir fonksiyon olduğu için hızlı
model.add(Dropout(0.2))
model.add(Dense(units=1,activation="sigmoid"))

model.compile(optimizer="rmsprop",loss="binary_crossentropy",metrics=["accuracy"])
model.summary()

learning_rate_reduction = ReduceLROnPlateau(monitor="val_accuracy",patience=2,verbose=1,factor=0.3,min_lr=0.000001)
epoch_number = 10
history = model.fit(datagen.flow(x_train,y_train, batch_size = 32), epochs = epoch_number, validation_data = datagen.flow(x_test,y_test),callbacks= [learning_rate_reduction])

print("Loss of Model: ",model.evaluate(x_test,y_test)[0])
print("Accuracy of Model: ",model.evaluate(x_test,y_test)[1]*100)

# Modelimizin değerlendireceğizzz (evaluation)
epochs = [i for i in range(epoch_number)]

fig, ax = plt.subplots(1,2)

train_acc = history.history["accuracy"]
train_loss = history.history["loss"]

val_acc = history.history["val_accuracy"]
val_loss = history.history["val_loss"]

ax[0].plot(epochs,train_acc,"go-",label="Traning Accuracy")
ax[0].plot(epochs,val_acc,"ro-",label="Validation Accuracy")
ax[0].legend()
ax[0].set_xlabel("Epochs")
ax[0].set_ylabel("Accuracy")

ax[1].plot(epochs,train_loss, "go-",label = "Traning Loss")
ax[1].plot(epochs,val_loss, "ro-",label = "Validation Loss")
ax[1].legend()
ax[1].set_xlabel("Epochs")
ax[1].set_ylabel("Loss")