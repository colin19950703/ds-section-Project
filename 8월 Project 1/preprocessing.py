import numpy as np
import tensorflow as tf
import cv2
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

def train_load(img_path, mask_path, target_size = (224,224)):
    image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, target_size)
    image = np.asarray(image)

    mask = cv2.imread(mask_path, cv2.IMREAD_COLOR)
    mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
    mask = cv2.resize(mask, target_size)
    mask = np.asarray(mask)    

    image, mask = augmentation(image, mask)
    
    return image,mask[:, :, np.newaxis]

def val_load(img_path,mask_path, target_size = (224, 224)):
    image = cv2.imread(img_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, target_size)
    image = np.asarray(image)

    mask = cv2.imread(mask_path, cv2.IMREAD_COLOR)
    mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
    mask = cv2.resize(mask, target_size) 
    mask = np.asarray(mask)    
    
    return image,mask[:, :, np.newaxis]

def augmentation(inp, targ):
    inp, targ = random_rot(inp, targ)
    inp, targ = random_flip(inp, targ)
    
    return inp, targ

def random_rot(inp, targ):
    k = np.random.randint(4)
    inp = np.rot90(inp, k)
    targ = np.rot90(targ, k)
    
    return inp, targ

def random_flip(inp, targ):
    f = np.random.randint(2)
    if f == 0:
        inp = np.fliplr(inp)
        targ = np.fliplr(targ)
        
    return inp, targ

def dataset_generater(df, arg = dict(), image_col = "", mask_col = "", batch_size = 32,
                      image_color_mode="rgb", mask_color_mode="grayscale",
                      image_save_prefix="image", mask_save_prefix="mask",
                      save_to_dir=None, seed = 42, target_size=(0, 0)):

    image_data_generator = ImageDataGenerator(**arg)
    mask_data_generator = ImageDataGenerator(**arg)

    image_data_generator = image_data_generator.flow_from_dataframe(dataframe= df,
                                             x_col= image_col,
                                             target_size = target_size,
                                             color_mode = image_color_mode,
                                             class_mode = None,
                                             batch_size=batch_size,
                                             seed = seed,                                                
                                             save_prefix  = image_save_prefix,
                                             )
    
    mask_data_generator = mask_data_generator.flow_from_dataframe(dataframe= df,
                                            x_col= mask_col,
                                            target_size = target_size,
                                            color_mode = mask_color_mode,
                                            class_mode = None,
                                            batch_size=batch_size,
                                            seed = seed,                                                
                                            save_to_dir = save_to_dir,
                                            save_prefix  = mask_save_prefix,
                                            )

    data_set = zip(image_data_generator, mask_data_generator)

    for (img, mask) in data_set:
        img = img / 255
        mask = mask / 255
        mask[mask > 0.5] = 1
        mask[mask <= 0.5] = 0
        yield (img, mask)