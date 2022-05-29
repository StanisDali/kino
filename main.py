"""Блок по скачиванию фотки с ФТП (название? частота (1 минута?))
*** Блок по сравнению фотографий (исходник с полученной фоткой) -- как разводить инфу с разных камер и чатов?
Блок с отрисовкой интерфейса: отображение фотографии, места и несовпадения,общая инфа про план и факт
Блок администратора: настройка адресов скачивания исходных фоток, адресов сохранения итоговых фоток, бэкапы.
Блок с чатботом (отправка админу информации о несовпадениях, отчет за неделю) или чатботы под каждый кинозал? из 4-х
Cделано по видео: https://youtu.be/caKnQlCMIYI """


import cv2
import pickle
import cvzone
import numpy as np

# поступающее фото
img = cv2.imread('primer1.jpeg')

with open('kinozalPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 14, 13

def checkPlace(imgPro): #вырезание всех сделанных областей в функцию

    spaceCounter = 0

    for pos in posList:
        x,y = pos


        imgCrop = imgPro[y:y + height, x:x + width]
        #cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
      #  cvzone.putTextRect(img, str(count), (x,y+height-5), scale = 1, thickness=1, offset=0)
        if count < 0.5:
            color = (0, 255, 0)
            thickness = 1

        else:
            color = (0, 0, 255)
            thickness = 1
            spaceCounter += 1  # заменить на подсчет из отдельного файла!!!!
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(img, f'Free: {spaceCounter} / {len(posList)}', (100, 50), scale = 2, thickness=2, offset=5, colorR=(0,200, 0))

while True:

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Преобразование фотки в чб и блюр
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkPlace(imgDilate)



    cv2.imshow("image", img)
    #cv2.imshow("imageBlur", imgBlur)
    #cv2.imshow("imageTres", imgThreshold)
    #cv2.imshow("imageMed", imgMedian)
    cv2.waitKey(1)