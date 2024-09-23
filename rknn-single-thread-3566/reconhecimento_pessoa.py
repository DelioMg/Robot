import os
import urllib
import traceback
import time
import datetime as dt
import sys
import numpy as np
import cv2
from rknnlite.api import RKNNLite

# Constantes do modelo e parâmetros de detecção
RKNN_MODEL = 'yolov5s.rknn'
DATASET = './dataset.txt'
OBJ_THRESH = 0.25
NMS_THRESH = 0.45
IMG_SIZE = 640
CLASSES = ("person",)  # Mantém apenas a classe "person"

# Funções auxiliares para o pós-processamento
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def xywh2xyxy(x):
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y

def process(input, mask, anchors):
    anchors = [anchors[i] for i in mask]
    grid_h, grid_w = map(int, input.shape[0:2])

    box_confidence = sigmoid(input[..., 4])
    box_confidence = np.expand_dims(box_confidence, axis=-1)
    box_class_probs = sigmoid(input[..., 5:])
    box_xy = sigmoid(input[..., :2]) * 2 - 0.5

    col = np.tile(np.arange(0, grid_w), grid_w).reshape(-1, grid_w)
    row = np.tile(np.arange(0, grid_h).reshape(-1, 1), grid_h)
    col = col.reshape(grid_h, grid_w, 1, 1).repeat(3, axis=-2)
    row = row.reshape(grid_h, grid_w, 1, 1).repeat(3, axis=-2)
    grid = np.concatenate((col, row), axis=-1)
    box_xy += grid
    box_xy *= int(IMG_SIZE / grid_h)

    box_wh = np.power(sigmoid(input[..., 2:4]) * 2, 2)
    box_wh = box_wh * anchors
    box = np.concatenate((box_xy, box_wh), axis=-1)

    return box, box_confidence, box_class_probs

def filter_boxes(boxes, box_confidences, box_class_probs):
    boxes = boxes.reshape(-1, 4)
    box_confidences = box_confidences.reshape(-1)
    box_class_probs = box_class_probs.reshape(-1, box_class_probs.shape[-1])

    _box_pos = np.where(box_confidences >= OBJ_THRESH)
    boxes = boxes[_box_pos]
    box_confidences = box_confidences[_box_pos]
    box_class_probs = box_class_probs[_box_pos]

    class_max_score = np.max(box_class_probs, axis=-1)
    classes = np.argmax(box_class_probs, axis=-1)

    # Filtrar apenas a classe "person" (índice 0)
    _class_pos = np.where(classes == 0)
    boxes = boxes[_class_pos]
    scores = (class_max_score * box_confidences)[_class_pos]

    return boxes, scores

def nms_boxes(boxes, scores):
    x = boxes[:, 0]
    y = boxes[:, 1]
    w = boxes[:, 2] - boxes[:, 0]
    h = boxes[:, 3] - boxes[:, 1]
    areas = w * h
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x[i], x[order[1:].astype(int)])
        yy1 = np.maximum(y[i], y[order[1:].astype(int)])
        xx2 = np.minimum(x[i] + w[i], x[order[1:].astype(int)] + w[order[1:].astype(int)])
        yy2 = np.minimum(y[i] + h[i], y[order[1:].astype(int)] + h[order[1:].astype(int)])

        w1 = np.maximum(0.0, xx2 - xx1 + 0.00001)
        h1 = np.maximum(0.0, yy2 - yy1 + 0.00001)
        inter = w1 * h1

        ovr = inter / (areas[i] + areas[order[1:].astype(int)] - inter)
        inds = np.where(ovr <= NMS_THRESH)[0]
        order = order[inds + 1]
    return np.array(keep)

def yolov5_post_process(input_data):
    masks = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    anchors = [[10, 13], [16, 30], [33, 23], [30, 61], [62, 45],
               [59, 119], [116, 90], [156, 198], [373, 326]]

    boxes, scores = [], []
    for input, mask in zip(input_data, masks):
        b, c, s = process(input, mask, anchors)
        b, s = filter_boxes(b, c, s)
        boxes.append(b)
        scores.append(s)

    boxes = np.concatenate(boxes)
    boxes = xywh2xyxy(boxes)
    scores = np.concatenate(scores)

    keep = nms_boxes(boxes, scores)
    boxes = boxes[keep]
    scores = scores[keep]

    return boxes, scores

def detect_person(frame):
    # Carregar modelo RKNN
    rknn = RKNNLite()
    ret = rknn.load_rknn(RKNN_MODEL)
    ret = rknn.init_runtime()
    if ret != 0:
        print('Erro ao inicializar o ambiente de runtime!')
        return None

    # Capturar vídeo da câmera
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

        # Inference
        outputs = rknn.inference(inputs=[img_resized])

        input0_data = outputs[0].reshape([3, -1] + list(outputs[0].shape[-2:]))
        input1_data = outputs[1].reshape([3, -1] + list(outputs[1].shape[-2:]))
        input2_data = outputs[2].reshape([3, -1] + list(outputs[2].shape[-2:]))
        input_data = [np.transpose(input0_data, (2, 3, 0, 1)),
                      np.transpose(input1_data, (2, 3, 0, 1)),
                      np.transpose(input2_data, (2, 3, 0, 1))]

        # Pós-processamento
        boxes, scores = yolov5_post_process(input_data)

        if boxes is not None and len(boxes) > 0:
            print(f"Pessoa detectada com pontuação: {scores[0]}")
            return boxes[0]  # Retorna as coordenadas da pessoa detectada

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None


