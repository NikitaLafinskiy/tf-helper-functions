# -*- coding: utf-8 -*-
"""tf-helper-functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19hvryGv5PDjj-pELvc2SbKWb2e5fRMeq
"""

def extract_data(folder):
  """
  Requires pyunpack and patool packages in order to work.
  Takes in a .rar folder name as the first argument and extracts data from it.
  """
  import pyunpack
  
  pyunpack.Archive(folder).extractall("")

def parse_data(folder):
  """
  Takes the folder name to parse as the first argument and prints all the names of all the files and directories inside of that folder.
  """
  import os

  for dirpath, dirnames, filenames in os.walk(folder):
    print(f"There are {len(filenames)} files and {len(dirnames)} directories in {dirpath}")

def list_classes(folder):
  """
  Takes the folder name as the first argument and prints all classes inside of that folder.
  """
  import pathlib
  import numpy as np

  data_dir = pathlib.Path(folder)
  arr = []
  for item in data_dir.glob("*"):
    arr.append(item.name)
  class_names = np.array(arr)
  print(class_names)

def view_images(folder, class_names, cols=4, rows=1):
  """
  Description:
    Displays images inside of a specified folder.
  
  Arguments:
    folder - name of the folder to parse;
    class_names - pick classes that will be displayed from the folder;
    cols - the number of columns of images;
    rows - the number of rows of images; 
  """
  import matplotlib.image as mpimg
  import matplotlib.pyplot as plt
  import random
  import os

  for i in range(rows):
    fig, ax = plt.subplots(figsize=(14,20), ncols=cols)
    for a in ax:
      random_class_num = random.randint(0, len(class_names)-1)
      random_img_num = random.randint(0, len(os.listdir(f"{folder}/{class_names[random_class_num]}"))-1)
      dir = f"{folder}/{class_names[random_class_num]}"
      random_img = os.listdir(dir)[random_img_num]
      img = mpimg.imread(f"{dir}/{random_img}", 0)
      a.imshow(img)
      a.axis(False)

def plot_metric_curves(history):
  """
  Takes the models *history* as the first parameter, plots the loss and the accuracy curves.
  """
  import matplotlib.pyplot as plt
  import pandas as pd 
  
  hist = pd.DataFrame(history.history)
  epochs = range(len(hist.loss))

  fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(12, 6))
  ax1.plot(epochs, hist.accuracy, label="accuracy")
  ax1.plot(epochs, hist.val_accuracy, label="validation accuracy")
  ax1.set(title="Accuracy score:", xlabel="Epoch", ylabel="Score")
  ax1.legend()

  ax2.plot(epochs, hist.loss, label="loss")
  ax2.plot(epochs, hist.val_loss, label="val_loss")
  ax2.set(title="Loss values:", xlabel="Epoch", ylabel="Value")
  ax2.legend()

def mase(y_true, y_pred):
  naive = y_true[:-1]
  naive_mae = np.absolute(np.average(y_true[1:] - naive))
  pred_mae = np.absolute(np.average(y_true - y_pred))
  return pred_mae / naive_mae

def eval_preds(y_true, y_pred):
  from sklearn.metrics import mae, mse

  df = pd.DataFrame([[mae(y_true, y_pred), mse(y_true, y_pred), mase(y_true, y_pred)]], columns=["MAE", "MSE", "MASE"], index='Score:')
  return df

def metrics(y_test, y_preds, multiclass=False):
  """
  Arguments: 
    y_test: Labels from the test dataset the model made predictions on;
    y_preds: Labels predicted by the model;
  """
  import pandas as pd 
  from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

  if(multiclass==True):
    acc = accuracy_score(y_test,y_preds)
    recall = recall_score(y_test,y_preds, average="micro")
    precision = precision_score(y_test, y_preds, average="micro")
    f1 = f1_score(y_test, y_preds, average="micro")
  elif(multiclass==False):
    acc = accuracy_score(y_test,y_preds)
    recall = recall_score(y_test,y_preds)
    precision = precision_score(y_test, y_preds)
    f1 = f1_score(y_test, y_preds)
  df = pd.DataFrame([[acc, recall, precision, f1]], columns=["Accuracy", "Recall", "Precision", "F1 Score"], index=["Score:"])
  return df

def plot_confusion_matrix(y_test, y_preds):
    """
    Arguments: 
      y_test: Labels from the test dataset the model made predictions on;
      y_preds: Labels predicted by the model;
    """
    from sklearn.metrics import ConfusionMatrixDisplay

    confusion_matrix = ConfusionMatrixDisplay.from_predictions(y_test, y_preds);
    return confusion_matrix

def read_image(fn, im_size=224):
  """
  Arguments:
    fn: filename to decodeand resize;
    im_size: the final size of the image;
  """
  import tensorflow as tf

  img = tf.io.read_file(fn)
  img = tf.image.decode_image(img,3)
  img = tf.image.resize(img, size=[im_size, im_size])
  return tf.expand_dims(img, 0)

def predict_label(fn, model, titles=['Class1', 'Class2']):
  """
    Arguments:
      fn: name of the file that the predictions are going to be made on;
      model: the model that is going to be used to make prediction;
      titles: the list of titles of the class names;
  """
  import matplotlib.pyplot as plt 
  import matplotlib.image as mpimg
  import numpy as np 

  img = read_image(fn)
  pred = model.predict(img)
  pred = np.argmax(pred)
  fig, ax = plt.subplots(figsize=(7,10))

  ax.set(title=titles[pred])
  ax.imshow(mpimg.imread(fn,0))
  ax.axis(False)

def save_tensorboard_model(dir_name, experiment_name):
  import datetime
  import tensorflow as tf
  log_dir = f"{dir_name}/{experiment_name}/{datetime.datetime.now().strftime('%Y%m%d_%H')}"
  tb_cb = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
  return tb_cb

