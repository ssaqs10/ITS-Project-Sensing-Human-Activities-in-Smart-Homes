import numpy as np
import pandas as pd

from scipy import stats

from config import * # Global variables

# Returns a tuple consisting of a convoluted data and labels
def get_convoluted_data(data):

    data_convoluted = []
    labels = []

    # Slide a "SEGMENT_TIME_SIZE" wide window with a step size of "TIME_STEP"
    # print("SEGMENT_TIME_SIZE, N_HIDDEN_NEURONS, BATCH_SIZE: ", SEGMENT_TIME_SIZE, N_HIDDEN_NEURONS, BATCH_SIZE)
    for i in range(0, len(data) - SEGMENT_TIME_SIZE + 1, TIME_STEP):
        x = data['x-axis'].values[i: i + SEGMENT_TIME_SIZE]
        y = data['y-axis'].values[i: i + SEGMENT_TIME_SIZE]
        z = data['z-axis'].values[i: i + SEGMENT_TIME_SIZE]
        data_convoluted.append([x, y, z])

        # Label for a data window is the label that appears most commonly
        label = stats.mode(data['activity'][i: i + SEGMENT_TIME_SIZE])[0][0]
        labels.append(label)

    # Convert to numpy
    data_convoluted = np.asarray(data_convoluted, dtype=np.float32)
    # print(data_convoluted.shape)
    data_convoluted = data_convoluted.transpose(0, 2, 1)

    # One-hot encoding
    # Previously used get_dummies
    # labels_ = np.asarray(pd.get_dummies(labels), dtype=np.float32)

    labels = one_hot_encode(labels)

    return data_convoluted, labels

def one_hot_encode(labels):
    length = len(LABELS_NAMES)
    encoded = []
    for i, label in enumerate(labels):
        array = np.zeros(length)
        array[label_position(label)] = 1
        encoded.append(array)

    return np.asarray(encoded, dtype=np.float32)

def label_position(_label):
    for i in range(len(LABELS_NAMES)):
        if(LABELS_NAMES[i] == _label):
            return i
