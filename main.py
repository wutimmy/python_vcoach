import cv2
from tools.OpenPose import OpenPose
import math


hands = False
hand = ""
right_ang = 0
left_ang = 0

def stright(x1,y1,x2,y2,x3,):
    k1=(p2[1]-p1[1])/(p2[0]-p1[0])
    k2=(p3[1]-p2[1])/(p3[0]-p2[0])


if __name__ == "__main__":
    pose = OpenPose()

    camera = cv2.VideoCapture(0)
    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            continue

        people = pose.detect(frame,in_height=100)
        for person in people:
            points = pose.draw(frame, person)

        print(points)

        hands = False

        if "2" in points.keys() and "3" in points.keys() and "4" in points.keys():
            hands = True
            hand = "Left"
            ang_a = math.atan2(points["4"][1]-points["3"][1],points["4"][0]-points["3"][0])*180/math.pi
            ang_b = math.atan2(points["3"][1]-points["2"][1],points["3"][0]-points["2"][0])*180/math.pi
            left_ang = round(180 + ang_a - ang_b)
        else:
            ang = 0
        cv2.putText(frame,"%s hand angle : %d"%(hand,left_ang),(20, 60), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 0, 255), 2, cv2.LINE_AA)
        if "5" in points.keys() and "6" in points.keys() and "7" in points.keys():
            hands = True
            hand = "Right"
            ang_a = math.atan2(points["7"][1]-points["6"][1],points["7"][0]-points["6"][0])*180/math.pi
            ang_b = math.atan2(points["6"][1]-points["5"][1],points["6"][0]-points["5"][0])*180/math.pi
            right_ang = round(180 + ang_a - ang_b)
            if right_ang < 0:
                right_ang = abs(right_ang)
            else:
                right_ang = 360 - right_ang
        else:
            right_ang = 0
        cv2.putText(frame,"%s hand angle : %d"%(hand,right_ang),(20, 40), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 0, 255), 2, cv2.LINE_AA)
        if not hands:
            hands = False
            cv2.putText(frame,"No hands detected.",(20, 20), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 0, 255), 2, cv2.LINE_AA)
            print("No hands detected.")

        

        cv2.imshow("frame", frame)
        key_code = cv2.waitKey(1)
        if key_code in [27, ord('q')]:
            break
    camera.release()
    cv2.destroyAllWindows()
