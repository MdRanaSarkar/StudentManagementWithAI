from PIL import ImageGrab
import numpy as np
import cv2
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def record_screen():

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 25.0, screensize)

    while True:
        try:
            img = ImageGrab.grab()
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            out.write(frame)
            print('recording....')
        except KeyboardInterrupt:
            break

    out.release()
    cv2.destroyAllWindows()
