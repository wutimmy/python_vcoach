import cv2
from tools.OpenPose import OpenPose

xys={}

if __name__ == "__main__":
    pose = OpenPose()

    camera = cv2.VideoCapture(0)
    while camera.isOpened():
        lh=[]
        rh=[]
        success, frame = camera.read()
        if not success:
            continue

        people = pose.detect(frame, in_height=100)
        for person in people:
            lh,rh=pose.draw_hand(frame, person)
        print(lh,rh)
        
        try:
            p1=rh[0]
            p2=rh[1]
            p3=rh[3]
            """
            if lh is None and rh is not None:
                p1=rh[0]
                p2=rh[1]
                p3=rh[3]
            elif lh is not None and rh is None:
                p1=lh[0]
                p2=lh[1]
                p3=lh[3]
            elif lh is None and rh is None:
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
                continue
            else:
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
                continue
            """
            k1=(p2[1]-p1[1])/(p2[0]-p1[0])
            k2=(p3[1]-p2[1])/(p3[0]-p2[0])
            print(k1-k2)
            print(k1,k2)
            if abs(k1-k2) < 0.5:
                print("hand straight.")
                cv2.putText(frame,"hand straight.",(40, 40), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 255, 255), 1, cv2.LINE_AA)
            else:
                print("hand is not straight.")
                cv2.putText(frame,"hand is not straight.",(40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
            if abs(k1) < 0.4 and abs(k2) < 0.4:
                print("hand is level.")
                cv2.putText(frame,"hand is level.",(40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            else:
                print("hand is not level.")
                cv2.putText(frame,"hand is not level.",(40, 80), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 1, cv2.LINE_AA)

                
        except Exception as e:
            print(e)
        
        cv2.imshow("frame", frame)


        key_code = cv2.waitKey(1)


        if key_code in [27, ord('q')]:
            break


    camera.release()
    cv2.destroyAllWindows()
