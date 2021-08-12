####custom module####
import models
import preprocessing as pp
####################
import os
import random
import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import pandas as pd

from glob import glob
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from sklearn.model_selection import train_test_split

class configure:
    seed = 42
    EPOCH = 25
    BATCH_SIZE = 32
    lr = 1e-4
    decay_rate = lr / EPOCH


    modelinfo = {'Unet': (256, 256), 'ResUnet' : (256, 256),'Vgg16_Unet' :(224, 224), 'Vgg16_FCN' : (224, 224)}
    modelname = 'Vgg16_FCN'
    model = models.Vgg16_FCN()
    target_size = modelinfo[modelname]


def seed_fixing(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    tf.random.set_seed(seed)

seed_fixing(configure.seed)

#directory creating
os.makedirs(f'result/{configure.modelname}', exist_ok=True)


# data path load
image_path = glob('Data/images/*.png')
mask_path = glob('Data/masks/*.png')

# train, val, test split
df = pd.DataFrame(data={'filename': image_path, 'mask': mask_path})
df_train , df_test = train_test_split(df, train_size=0.9, random_state=configure.seed)
df_train , df_val = train_test_split(df_train, train_size=0.8, random_state=configure.seed)

print('[train data]\n'+'image -',len(df_train['filename']),'mask -',len(df_train['mask']))
print('[validation data]\n'+'image -',len(df_val['filename']),'mask -',len(df_val['mask']))
print('[test data]\n'+'image -',len(df_test['filename']),'mask -',len(df_test['mask']))


# # dataset genrating
# args = dict(width_shift_range = 0.1,
#             height_shift_range = 0.1,
#             shear_range=0.1,
#             rotation_range = 90,
#             zoom_range = 0.2,
#             horizontal_flip=True,
#             fill_mode='nearest')

# train_set = pp.dataset_generater(df_train,
#                                  arg = args,
#                                  image_col='filename',
#                                  mask_col='mask',
#                                  batch_size=configure.BATCH_SIZE,
#                                  target_size=configure.target_size)

# val_set = pp.dataset_generater(df_val,
#                                image_col='filename',
#                                mask_col='mask',
#                                batch_size=configure.BATCH_SIZE,
#                                target_size=configure.target_size)

# # callback
# modelname = f'result/{configure.modelname}/{configure.modelname}_checkpoint-epoch-{configure.EPOCH}-batch-{configure.BATCH_SIZE}-trial-001.h5'

# checkpoint = ModelCheckpoint(modelname,
#                              monitor='val_loss',
#                              verbose=1,
#                              save_best_only=True,
#                              mode='auto'
#                             )

# reduceLR = ReduceLROnPlateau(monitor='val_loss',
#                              factor=0.5,
#                              patience=2
#                              )

# earlystopping = EarlyStopping(monitor='val_loss',
#                               patience=5,
#                              )

# # model create & compile
# model = configure.model
# model.summary()
# print('Model Created!!')
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# # model fit
# results = model.fit(train_set,
#                     steps_per_epoch=len(df_train) / configure.BATCH_SIZE,
#                     validation_data = val_set,
#                     validation_steps=len(df_val) / configure.BATCH_SIZE,
#                     epochs=configure.EPOCH,
#                     callbacks = [checkpoint, reduceLR]
#                     )

# #summarize history for accuracy & loss
# plt.subplot(3,1,1)
# plt.plot(results.history['accuracy'])
# plt.plot(results.history['val_accuracy'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')

# plt.subplot(3,1,3)
# plt.plot(results.history['loss'])
# plt.plot(results.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.savefig(f'result/{configure.modelname}/0.acc_loss.png')

# for n in range(30):
#     img = cv2.imread(df_test['filename'].iloc[n])
#     img = cv2.resize(img , configure.target_size)
#     img = img / 255
#     img = img[np.newaxis, :, :, :]

#     mask = cv2.imread(df_test['mask'].iloc[n])
#     mask = cv2.resize(mask , configure.target_size)
#     pred=model.predict(img)

#     plt.figure(figsize=(10,3))
#     plt.subplot(1,3,1)
#     plt.imshow(np.squeeze(img))
#     plt.title('Original Image')
#     plt.subplot(1,3,2)
#     plt.imshow(np.squeeze(mask))
#     plt.title('Mask Image')
#     plt.subplot(1,3,3)
#     plt.imshow(np.squeeze(pred) > .5)
#     plt.title('Predict')
#     plt.savefig(f'result/{configure.modelname}/0.result_{n}.png')
