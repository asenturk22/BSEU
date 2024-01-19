import os
os.environ["KMP_DUPLICATE_LTB_OK"] = "TRUE"

# OpenCV library import
import cv2
import sys
import numpy as np
import imutils

from ultralytics import YOLO
from collections import defaultdict
from ultralytics.utils.checks import check_imshow
from ultralytics.utils.plotting import Annotator, colors

# Variable Declarations
video_path   = "inference/pexel.mp4"
model_path   = "models/yolov8n.pt"
color_green  = (  0, 255,   0)
color_red    = (  0,   0, 255)
color_blue   = (255,   0,   0)
color_white  = (255, 255, 255)
thickness    = 2  # kalınlık
font         = cv2.FONT_HERSHEY_SIMPLEX
font_scale   = 0.5
vehicle_ids  = [2, 3, 5, 7]

# yon tespit sayaclari
down         = {}
up           = {}
left         = {}
right        = {}
track_history = defaultdict(lambda: [])

# YOLOv8 nano modelinin indirilmesi
model = YOLO(model_path)
names = model.model.names

# Bir video akışını açar
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), "Error reading video file"

w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Yeni genişlik ve yükseklik değerleri
new_width = 1280                        # Belirli bir genişlik
new_height = int((new_width / w) * h)   # Oranı koruyarak yüksekliği hesapla

# Yeniden boyutlandırılmış video çerçeve boyutları
w, h = new_width, new_height

writer = cv2.VideoWriter("vehicle_tracking.avi",
                       fourcc,
                       20.0,
                       (w, h))

rectangle_coords = (0, 0, 250, 100)  # Dikdörtgen alanın koordinatları: (x1, y1, x2, y2)

# x,y koordinatları    
polygon_up    = np.array([[320,280], [519,300], [370,240], [246,248]], np.int32)
polygon_right = np.array([[1275,380], [1194,380], [1234,578], [1275,594]], np.int32)
polygon_down  = np.array([[1200,720], [994,600], [393,600], [388,720]], np.int32)
polygon_left  = np.array([[5,300], [50,300], [50,460], [5,460]], np.int32)

# Video görüntülerini okumak
while cap.isOpened():
    success, frame = cap.read()
    if success:    
        # video boyutunu yeniden yapılandır. 
        frame = imutils.resize(frame, width=w)
        
        cv2.polylines(frame, [polygon_up], isClosed=True, color=color_green, thickness=thickness)
        cv2.polylines(frame, [polygon_down], isClosed=True, color=color_green, thickness=thickness)
        cv2.polylines(frame, [polygon_left], isClosed=True, color=color_green, thickness=thickness)
        cv2.polylines(frame, [polygon_right], isClosed=True, color=color_green, thickness=thickness)

        # 'model' nesnesi üzerinde 'track()' yöntemini kullanarak bir görüntüde nesne takibi yapılır.
        # 'track()' fonksiyonu, nesne takibini gerçekleştirir ve sonuçları 'results' değişkenine atan bir veri yapısı döndürür.
        results = model.track(frame, persist=True, verbose=False)

        # Sonuçlardan sadece ilk nesnenin koordinat kutularını ('boxes') alır.
        # Bu kutular, takip edilen nesnenin konumunu belirtir.
        boxes = results[0].boxes.xyxy.cpu()
       
        
        
        if results[0].boxes.id is not None:
            # Extract prediction results
            clss = results[0].boxes.cls.cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confs = results[0].boxes.conf.float().cpu().tolist()
            
            # Annotator Init
            annotator = Annotator(frame, line_width=2)
            
            for box, cls, track_id in zip(boxes, clss, track_ids):
                cls = int(cls)
                                
                if cls in vehicle_ids:   
                    annotator.box_label(box, color=colors(int(cls), True), label=f'ID: {track_id} - {names[cls]}')
                    cx = int((box[0] + box[2]) / 2)
                    cy = int((box[1] + box[3]) / 2)
                    
                    # Nesnenin takip geçmişini tut
                    track = track_history[track_id]
                    #track.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))
                    track.append((cx, cy))
                    if len(track) > 30:
                        track.pop(0)
                        
                    # Plot tracks 
                    points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))        
                    cv2.circle(frame, (track[-1]), 7, colors(int(cls), True), -1)
                    cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)
                    
                    #msasureDist : noktanın poligona olan mesafesini ölçüyor. 
                    up_result     = cv2.pointPolygonTest(polygon_up,    (cx, cy), measureDist=False)
                    down_result   = cv2.pointPolygonTest(polygon_down,  (cx, cy), measureDist=False)
                    left_result   = cv2.pointPolygonTest(polygon_left,  (cx, cy), measureDist=False)
                    right_result  = cv2.pointPolygonTest(polygon_right, (cx, cy), measureDist=False)
                    
                    if up_result > 0: 
                        up[track_id] = box
                        
                    if down_result > 0: 
                        down[track_id] = box
                        
                    if left_result > 0: 
                        left[track_id] = box
                        
                    if right_result > 0: 
                        right[track_id] = box

        down_counter  = "{:<10} : {:>5}".format("Gelis".ljust(10), str(len(list(down.keys()))).rjust(5)).upper()
        up_counter    = "{:<10} : {:>5}".format("Gidis".ljust(10), str(len(list(up.keys()))).rjust(5)).upper()
        left_counter  = "{:<10} : {:>5}".format("Sol".ljust(10),   str(len(list(left.keys()))).rjust(5)).upper()
        right_counter = "{:<10} : {:>5}".format("Sag".ljust(10),   str(len(list(right.keys()))).rjust(5)).upper()

        cv2.rectangle(frame, (rectangle_coords[0], rectangle_coords[1]), (rectangle_coords[2], rectangle_coords[3]),  (65, 53, 52), -1)
        cv2.putText(frame, down_counter,  (20, 20), font, font_scale, color_white, 1, cv2.LINE_AA)
        cv2.putText(frame, up_counter,    (20, 40), font, font_scale, color_white, 1, cv2.LINE_AA)
        cv2.putText(frame, left_counter,  (20, 60), font, font_scale, color_white, 1, cv2.LINE_AA)
        cv2.putText(frame, right_counter, (20, 80), font, font_scale, color_white, 1, cv2.LINE_AA)
        
        writer.write(frame)
        # Okunan frame'i ekranda göster
        cv2.imshow("Vehicle Tracking", frame)
        cv2.imwrite("last.png", frame)


        # Görüntüyü 10ms olarak beklet ve "q" tuşuna basılı ise işlemi sonlandır.
        if (cv2.waitKey(1) & 0xFF == ord("q")):  # ord("q") -> q  harfinin hex kodunu üretir. 
            break
    else:
        break
      

# kaynakları belleğe iade et
cap.release() 
writer.release()

#  OpenCV kütüphanesinde açılmış olan tüm pencereleri kapat
cv2.destroyAllWindows() 

print("[INFO].. the video was successfully processed/saved!")    
