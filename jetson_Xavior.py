import cv2
from ultralytics import YOLO
import torch
import Jetson.GPIO as GPIO
from RPi_GPIO_i2c_LCD import lcd
from time import sleep
GPIO.setmode(GPIO.BOARD)

i2c_address = 0x27
model = YOLO("best.pt")
lcdDisplay = lcd.HD44780(i2c_address)
cap = cv2.VideoCapture(0)

l1 = 11
l2 = 13
l3 = 15
l4 = 16
led1 = 33
led2 = 35
led3 = 36
# Thiết lập chân là OUTPUT (để điều khiển LED)
GPIO.setup(l1, GPIO.OUT)
GPIO.setup(l2, GPIO.OUT)
GPIO.setup(l3, GPIO.OUT)
GPIO.setup(l4, GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inference", annotated_frame)
        for result in results:
            print("class", result.boxes.cls)
            for k in result.boxes.cls:
            	if k == torch.Tensor([0.]):
            		lcdDisplay.set("HOA",1)
            		GPIO.output(l1, GPIO.HIGH)
            		GPIO.output(l2, GPIO.LOW)
            		GPIO.output(l3, GPIO.LOW)
            		GPIO.output(l4, GPIO.LOW)
            		GPIO.output(led1, GPIO.HIGH)
            		GPIO.output(led2, GPIO.LOW)
            		GPIO.output(led3, GPIO.LOW)
            	else:
            		lcdDisplay.set("                    ",1)
            	if k == torch.Tensor([1.]):
            		lcdDisplay.set("HIEU",2)
            		GPIO.output(l1, GPIO.LOW)
            		GPIO.output(l2, GPIO.LOW)
            		GPIO.output(l3, GPIO.HIGH)
            		GPIO.output(l4, GPIO.LOW)
            		GPIO.output(led1, GPIO.LOW)
            		GPIO.output(led2, GPIO.HIGH)
            		GPIO.output(led3, GPIO.LOW)
            	else:
            		lcdDisplay.set("                    ",2)
            	if k == torch.Tensor([2.]):
            		lcdDisplay.set("BALL",3)
            		GPIO.output(l1, GPIO.HIGH)
            		GPIO.output(l2, GPIO.LOW)
            		GPIO.output(l3, GPIO.HIGH)
            		GPIO.output(l4, GPIO.LOW)
            		GPIO.output(led1, GPIO.LOW)
            		GPIO.output(led2, GPIO.LOW)
            		GPIO.output(led3, GPIO.HIGH)
            	else:
            		lcdDisplay.set("                    ",3)
            #print("xyxy", result.boxes.xyxy)
            #print("conf", result.boxes.conf)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
