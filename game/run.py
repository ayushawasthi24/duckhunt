import pyautogui
from hand_model import HandGestureModel
import cv2

di=pyautogui.size()
di=(di[0],di[1])
# print(di)
model=HandGestureModel(model_path='./game/outfile.task',dim=di)
print(di)
i=0
# click_wait
while i<500:
    i+=1
    pos=model.get_pos()
    if(model.is_click()):pyautogui.click()
    pyautogui.moveTo(pos[0], pos[1], duration = 0)