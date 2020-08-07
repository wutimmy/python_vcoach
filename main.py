import cv2
from tools.OpenPose import OpenPose
import traceback
import sys
import math

exc_info=""
p1=[]
p2=[]
p3=[]
lineA=[]
lineB=[]
error=False


def left():
    global p1, p2, p3, lineA, lineB
    p1=lh[0]
    p2=lh[1]
    p3=lh[3]
    print("left")
    try:
        lineA=[lh[0],lh[1]]
        lineB=[lh[2],lh[3]]
    except:
        error = True
    
    cv2.putText(frame,"Detected Left Hand.",(40, 120), cv2.FONT_HERSHEY_SIMPLEX,  1, (255, 0, 0), 2, cv2.LINE_AA)

def right():
    global p1, p2, p3, lineA, lineB
    p1=rh[0]
    p2=rh[1]
    p3=rh[3]
    print("right")
    cv2.putText(frame,"Detected Right Hand.",(40, 120), cv2.FONT_HERSHEY_SIMPLEX,  1, (255, 0, 0), 2, cv2.LINE_AA)
    try:
        lineA=[rh[0],rh[1]]
        lineB=[rh[2],rh[3]]
    except:
        error = True

def slope(x1, y1, x2, y2): # Line slope given two points:
    return (y2-y1)/(x2-x1)

def angle(s1, s2): 
    return math.degrees(math.atan((s2-s1)/(1+(s2*s1))))

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
        """
        for person in people1:
            lh,rh=pose.draw_hand(body_frame, person)
        """
        
        try:
            exc_info = sys.exc_info()
            """
            p1=lh[0]
            p2=lh[1]
            p3=lh[3]
            """
            
            if bool(len(lh)) is False and bool(len(rh)) is True:
                right()
                
            elif bool(len(lh)) is True and bool(len(rh)) is False:
                left()
            elif bool(len(lh)) is False and bool(len(rh)) is False:
                print("No hands detected.")
                cv2.putText(frame,"No hands detected.",(40, 160), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.imshow("frame", frame)
                #cv2.imshow("body", body_frame)
                key_code = cv2.waitKey(1)
                if key_code in [27, ord('q')]:
                    break
                else:
                    continue
            elif bool(len(lh)) is True and bool(len(rh)) is True:
                print("Both hands detected.")
                #cv2.putText(frame,"Both hands detected. Testing...",(40, 180), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 0, 255), 2, cv2.LINE_AA)
                
                if lh[0][0] < rh[0][0] or lh[0][1] < rh[0][1]:
                    if lh[0][1] > rh[0][1]:
                        right()
                    else:
                        left()
                else:
                    right()

            

                """
                cv2.imshow("frame", frame)
                key_code = cv2.waitKey(1)
                if key_code in [27, ord('q')]:
                    break
                """

            else:
                print("else")
                cv2.imshow("frame", frame)
                #cv2.imshow("body", body_frame)
                key_code = cv2.waitKey(1)
                if key_code in [27, ord('q')]:
                    break
                else:
                    continue

            print("*************")
            print(lineA)
            print(lineB)
            print("*************")
            
            if not error:
                slope1 = slope(lineA[0][0], lineA[0][1], lineA[1][0], lineA[1][1])
                slope2 = slope(lineB[0][0], lineB[0][1], lineB[1][0], lineB[1][1])
                ang = angle(slope2, slope1)
                print("-"*10+"hand angle"+"-"*10)
                print(ang)
                print("-"*10+"hand angle"+"-"*10)
            
            k1=(p2[1]-p1[1])/(p2[0]-p1[0])
            k2=(p3[1]-p2[1])/(p3[0]-p2[0])
            print(k1-k2)
            print(k1,k2)
            
            
            
            if abs(k1-k2) < 0.5:
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
