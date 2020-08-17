import cv2
from tools.OpenPose import OpenPose
import traceback
import sys
import math

exc_info=""
p1=[]
p2=[]
p3=[]



def left():
    global p1, p2, p3, lineA, lineB
    p1=lh[0]
    p2=lh[1]
    p3=lh[3]
    print("left")

    
    cv2.putText(frame,"Detected Left Hand.",(40, 120), cv2.FONT_HERSHEY_SIMPLEX,  1, (255, 0, 0), 2, cv2.LINE_AA)

def right():
    global p1, p2, p3, lineA, lineB
    p1=rh[0]
    p2=rh[1]
    p3=rh[3]
    print("right")
    cv2.putText(frame,"Detected Right Hand.",(40, 120), cv2.FONT_HERSHEY_SIMPLEX,  1, (255, 0, 0), 2, cv2.LINE_AA)



if __name__ == "__main__":
    pose = OpenPose()

    camera = cv2.VideoCapture(0)
    while camera.isOpened():
        lh=[]
        rh=[]
        success, frame = camera.read()
        body_frame=frame.copy()
        if not success:
            continue

        people = pose.detect(frame, in_height=150)
        #people1 = pose.detect(body_frame, in_height=100)
        for person in people:
            lh,rh=pose.draw_hand(frame, person)
        print(lh,rh)

        
        try:
            exc_info = sys.exc_info()
            
            if bool(len(lh)) is False and bool(len(rh)) is True and len(rh) == 4:
                right()
            elif bool(len(lh)) is True and bool(len(rh)) is False and len(lh) == 4:
                left()
            elif bool(len(lh)) is False and bool(len(rh)) is False and len(lh) == 0 and len(rh) == 0:
                print("No hands detected.")
                cv2.putText(frame,"No hands detected.",(40, 160), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.imshow("frame", frame)
                #cv2.imshow("body", body_frame)
                key_code = cv2.waitKey(1)
                if key_code in [27, ord('q')]:
                    break
                else:
                    continue
            elif bool(len(lh)) is True and bool(len(rh)) is True and len(lh) != 0 and len(rh) != 0:
                print("Both hands detected.")
                #cv2.putText(frame,"Both hands detected. Testing...",(40, 180), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 0, 255), 2, cv2.LINE_AA)
                
                if lh[0][0] < rh[0][0] or lh[0][1] < rh[0][1]:
                    if lh[0][1] > rh[0][1]:
                        right()
                    else:
                        left()
                else:
                    right()




            print("*************")
            ang_a = math.atan2(p3[1]-p2[1],p3[0]-p2[0])*180/math.pi
            ang_b = math.atan2(p2[1]-p1[1],p2[0]-p1[0])*180/math.pi
            ang = round(180 + ang_a - ang_b)
            print(ang)
            cv2.putText(frame,"Hand Angle : "+str(ang),(40, 180), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)
            print("*************")
            
            
            k1=(p2[1]-p1[1])/(p2[0]-p1[0])
            k2=(p3[1]-p2[1])/(p3[0]-p2[0])
            print(k1-k2)
            print(k1,k2)
            
            
            
            if abs(k2-k1) < 0.5:
                print("hand straight.")
                cv2.putText(frame,"hand straight.",(40, 40), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 255, 255), 2, cv2.LINE_AA)
            else:
                print("hand is not straight.")
                cv2.putText(frame,"hand is not straight.",(40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            if abs(k1) < 0.35 and abs(k2) < 0.35:
                print("hand is level.")
                cv2.putText(frame,"hand is level.",(40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                print("hand is not level.")
                cv2.putText(frame,"hand is not level.",(40, 80), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)

                
        except Exception:
            print(traceback.format_exc())
        
        cv2.imshow("frame", frame)
        #cv2.imshow("body", body_frame)


        key_code = cv2.waitKey(1)


        if key_code in [27, ord('q')]:
            break


    camera.release()
    cv2.destroyAllWindows()
