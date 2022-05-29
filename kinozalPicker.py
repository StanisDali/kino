import cv2
import pickle



width, height = 14, 13

try: #попытка сохранения точек в имеющийся фаил (если он есть)
    with open('kinozalPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x,y,flags,params): #как присвоить каждой точке свое уникальное название?
    if events == cv2.EVENT_LBUTTONDOWN: #добавление объектов по клику
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN: #удаление по клику (если кликаем внутри объекта
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('kinozalPos', 'wb') as f: #запись точек в имеющийся
        pickle.dump(posList, f)

while True:

    img = cv2.imread('ref1.jpeg')

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 255), 1)

    cv2.imshow('image', img)
    cv2.setMouseCallback('image', mouseClick )
    cv2.waitKey(1)
