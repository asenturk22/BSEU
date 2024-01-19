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
video_path   = "inference/otoban.mp4"
model_path   = "models/yolov8n.pt"
color_green  = (  0, 255,   0)
color_red    = (  0,   0, 255)
color_blue   = (255,   0,   0)
color_white  = (255, 255, 255)
thickness    = 2  # kalınlık
font         = cv2.FONT_HERSHEY_SIMPLEX
font_scale   = 0.5
vehicle_ids  = [2, 3, 5, 7]
down         = {}
up           = {}



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
fourcc = cv2.VideoWriter_fourcc(*'mp4v')


# Yeni genişlik ve yükseklik değerleri
new_width = 1280                        # Belirli bir genişlik
new_height = int((new_width / w) * h)   # Oranı koruyarak yüksekliği hesapla

# Yeniden boyutlandırılmış video çerçeve boyutları
w, h = new_width, new_height

threshold     = h - 120
cy_center    = int(w / 2)

writer = cv2.VideoWriter("vehicle_tracking.avi",
                       cv2.VideoWriter_fourcc(*'mp4v'),
                       fps,
                       (w, h))


rectangle_coords = (0, 0, 300, 200)  # Dikdörtgen alanın koordinatları: (x1, y1, x2, y2)


# Video görüntülerini okumak
while cap.isOpened():
    success, frame = cap.read()
    if success:    
        # video boyutunu yeniden yapılandır. 
        frame = imutils.resize(frame, width=w)

        # 'model' nesnesi üzerinde 'track()' yöntemini kullanarak bir görüntüde nesne takibi yapılır.
        # 'track()' fonksiyonu, nesne takibini gerçekleştirir ve sonuçları 'results' değişkenine atan bir veri yapısı döndürür.
        results = model.track(frame, persist=True, verbose=False)

        # Sonuçlardan sadece ilk nesnenin koordinat kutularını ('boxes') alır.
        # Bu kutular, takip edilen nesnenin konumunu belirtir.
        boxes = results[0].boxes.xyxy.cpu()
       
        cv2.line(frame, (0, threshold), (w, threshold), color_red, thickness)
        cv2.putText(frame, "Reference", (600,threshold - 10), font, 0.7, color_red, thickness) 
        
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
                    
                    if cy > (threshold - 4) and cy < (threshold + 4) and cx < cy_center: 
                        down[track_id] = box, names[cls]
                        
                    if cy > (threshold - 4) and cy < (threshold + 4) and cx > cy_center: 
                        up[track_id]   = box, names[cls]
                        
                    class_counts = {}    
                    for up_key in up: 
                        #print("up : ", up[up_key][1])
                        class_name = up[up_key][1]
                        if class_name in class_counts:
                             class_counts[class_name] += 1
                        else:
                            class_counts[class_name] = 1
                            
                    for down_key in down: 
                        #print("down : ", down[down_key][1])
                        class_name = down[down_key][1]   
                        if class_name in class_counts:
                             class_counts[class_name] += 1
                        else:
                            class_counts[class_name] = 1

                    up_text = "Giden : {}".format(len(list(up.keys())))
                    down_text = "Gelen : {}".format(len(list(down.keys())))
                    cv2.rectangle(frame, (w - 160, threshold - 40), (w - 10 , threshold - 5),  (65, 53, 52), -1)
                    cv2.putText(frame, up_text, (w - 150, threshold - 15), font, 0.8, color_white, thickness)                    
                    cv2.rectangle(frame, (10, threshold - 40), (160 , threshold - 5),  (65, 53, 52), -1)
                    cv2.putText(frame, down_text, (20, threshold - 15), font, 0.8, color_white, thickness)
                    
                    cv2.rectangle(frame, (rectangle_coords[0], rectangle_coords[1]), (rectangle_coords[2], rectangle_coords[3]),  (65, 53, 52), -1)
                    text_position = (rectangle_coords[0] + 20, rectangle_coords[1] + 50)
                    for key, value in class_counts.items():
                        #text = f"{key}     : {value}".upper()
                        text = "{:<10} : {:>5}".format(key[:10], str(value).rjust(5)).upper()                        
                        cv2.putText(frame, text, text_position, font, 0.8, color_white, 1, cv2.LINE_AA)
                        text_position = (text_position[0], text_position[1] + 50)  # Yeni satıra geçmek için pozisyonu güncelle

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
