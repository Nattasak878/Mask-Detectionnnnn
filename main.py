import cv2
import tensorflow.keras 
from PIL import Image, ImageOps
import numpy as np

webcam = cv2.VideoCapture(0)
face_cascade ="haarcascade_frontalface_default.xml"
face_classifier = cv2.CascadeClassifier(face_cascade)
np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model('keras_model.h5')
size = (224,224)
count = 9999

while True:
  success, image_bgr = webcam.read()
  image_bgr = cv2.flip(image_bgr, 1)
  image_bw = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY) 
  image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) 
  faces = face_classifier.detectMultiScale(image_bw)
  image_org = image_bgr.copy()
  for face in faces:
    x,y,w,h = face
    cface_rgb = Image.fromarray(image_rgb[y:y+h, x:x+w])
    data = np.ndarray(shape = (1,224,224,3), dtype = np.float32)
    image = cface_rgb
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    print(prediction)
    if prediction[0][0] > prediction[0][1]:
      cv2.putText(image_bgr, "์Non-masked", (x, y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2)
      cv2.rectangle(image_bgr, (x,y), (x+w, y+h), (0,0,255), 2)
    else: 
      cv2.putText(image_bgr, "Masked", (x, y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)
      cv2.rectangle(image_bgr, (x,y), (x+w, y+h), (0,255,0), 2)
  cv2.imshow("Mask Detection", image_bgr)
  if(cv2.waitKey(1) & 0xFF == ord("e")):
    break
webcam.release()
cv2.destroyAllWindows()
