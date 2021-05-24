import streamlit as st
import cv2
import time
import numpy as np
from PIL import Image

#load model and weights
model = model_from_json(open("EmotionRecCNNAnalysis/model.json", "r").read()) 
model.load_weights('EmotionRecCNNAnalysis/model.h5')

run_emotion = st.checkbox('Start Emotion Detector')
FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)
while run_emotion:
    _, frame = camera.read()
    FRAME_WINDOW.image(app.emotion_recog(camera, model, run_emotion))
else:
    camera.release()
    cv2.destroyAllWindows()
    st.write('Stopped')

@st.cache(persist=True)
def load_image(img):
    im = Image.open(img)
    return im


# Load Yolo
net = cv2.dnn.readNet("weights/yolov5.weights", "weights/yolov5.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
img = cv2.imread(load_image)
img = cv2.resize(img, None, fx=0.8, fy=0.7)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

# Showing informations on the screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
print(indexes)

font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        cv2.putText(img, label, (x, y + 30), font, 3, color, 2)


cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()



def display_output():
    st.text("")
    col2.subheader("Object-Detected Image")
    st.text("")
    plt.figure(figsize = (15,15))
    plt.imshow(img)
    col2.pyplot(use_column_width=True)
