import cv2
import numpy as np

prefix = "engine/object_detection/"
if __name__ == "__main__":
    prefix = ""


def get_detected_objs(file_name):
    # Load Yolo
    net = cv2.dnn.readNet(prefix+"yolov3-tiny.weights", prefix+"yolov3-tiny.cfg")
    classes = []
    with open(prefix+"coco_eng.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    img = cv2.imread('raw/'+file_name)
    # img = cv2.resize(img, None, fx=0.4, fy=0.4)
    print(file_name)
    print(img)
    height, width, channels = img.shape

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

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
    detected_objs = []

    for i in range(len(boxes)):
        if i in indexes:
            label = str(classes[class_ids[i]])
            detected_objs.append(label)
    return detected_objs


if __name__ == "__main__":
    print(get_detected_objs())
