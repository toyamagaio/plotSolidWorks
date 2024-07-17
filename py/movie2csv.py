import os
import cv2
import pytesseract
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#video_path = '../../mach_jet/anime3.avi'
video_path = '../../mach_jet/anime0.1s.avi'
output_csv = 'output.csv'

save_dir='../../mach_jet/captured_frames'

cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)

frame_interval = int(fps)

data = []

##size of capture (x,y)=(1650, 778)
xt, yt, wt, ht = 750, 0, 100, 30  #
x1, y1, w1, h1 = 170, 410, 190, 180  #
xp, yp, wp, hp = 96, 47, 80, 17  #

frame_count = 0
custum_config='--psm 7' # digits
custum_config_p='--psm 7 digits' #

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    #print(type(frame))
    #print(frame.shape)

    if frame_count % frame_interval == 0:
        roi_t = frame[yt:yt+ht, xt:xt+wt]
        frame_filename = os.path.join(save_dir, f"frame_sec_{frame_count // frame_interval}.png")
        cv2.imwrite(frame_filename, roi_t)

        roi_1 = frame[y1:y1+h1, x1:x1+w1]
        frame_filename1 = os.path.join(save_dir, f"frame1_{frame_count // frame_interval}.png")
        cv2.imwrite(frame_filename1, roi_1)

        #print(roi_1.shape)
        roi_p = roi_1[yp:yp+hp,xp:xp+wp]
        frame_filenamep=os.path.join(save_dir,f"framep_{frame_count//frame_interval}.png")
        cv2.imwrite(frame_filenamep, roi_p)

        text   = pytesseract.image_to_string(roi_t, config=custum_config)
        text_p = pytesseract.image_to_string(roi_p, config=custum_config)
        print(text, text_p)
        print(type(text))
        
        data.append([frame_count / fps, text.strip(), text_p.strip()])

    frame_count += 1

cap.release()

df = pd.DataFrame(data, columns=['Time (s)', 'PhysTime', 'Pressure'])
df.to_csv(output_csv, index=False)

print("CSV",output_csv)
