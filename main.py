import cv2
from tools.OpenPose import OpenPose
import math


hands = False
right_ang = 0
left_ang = 0
ang_list = [["8","9","10"],["11","12","13"],["1","2","3"],["1","5","6"],["1","8","9"],["1","11","12"]]
angs_list = []
points = {}

def stright(points):
    kss = {}
    for i in points.keys():
        for j in points.keys():
            if int(i) - int(j) == 1:
                k=(points[i][1]-points[j][1])/(points[i][0]-points[j][0])
                kss[i+j]=k
            else:
                continue
    return kss

def ca_ang(pgroup):
    ang_c = math.atan2(points[pgroup[2]][1]-points[pgroup[1]][1],points[group[2]][0]-points[pgroup[1]][0])*180/math.pi
    ang_d = math.atan2(points[pgroup[1]][1]-points[pgroup[0]][1],points[pgroup[1]][0]-points[pgroup[0]][0])*180/math.pi
    tang = round(180 + ang_c - ang_d)
    """
    if tang < 0:
        tang = abs(tang)
    else:
        tang = 360 - tang
    """
    return tang


def ca_all_ang(ang_list):
    angs = {}
    for i in ang_list:
        try:
            angs["".join(i)] = ca_ang(i)
        except Exception as e:
            print(e)
            continue
    return angs
    


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

        #print(points)

        hands = False

        if "2" in points.keys() and "3" in points.keys() and "4" in points.keys():
            hands = True
            ang_a = math.atan2(points["4"][1]-points["3"][1],points["4"][0]-points["3"][0])*180/math.pi
            ang_b = math.atan2(points["3"][1]-points["2"][1],points["3"][0]-points["2"][0])*180/math.pi
            left_ang = round(180 + ang_a - ang_b)
        else:
            ang = 0
        cv2.putText(frame,"Left hand angle : %d"%(left_ang),(20, 60), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 0, 255), 2, cv2.LINE_AA)
        if "5" in points.keys() and "6" in points.keys() and "7" in points.keys():
            hands = True
            ang_a = math.atan2(points["7"][1]-points["6"][1],points["7"][0]-points["6"][0])*180/math.pi
            ang_b = math.atan2(points["6"][1]-points["5"][1],points["6"][0]-points["5"][0])*180/math.pi
            right_ang = round(180 + ang_a - ang_b)
            if right_ang < 0:
                right_ang = abs(right_ang)
            else:
                right_ang = 360 - right_ang
        else:
            right_ang = 0
        cv2.putText(frame,"Right hand angle : %d"%(right_ang),(20, 40), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 0, 255), 2, cv2.LINE_AA)
        if not hands:
            hands = False
            cv2.putText(frame,"No hands detected.",(20, 20), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 0, 255), 2, cv2.LINE_AA)
            #print("No hands detected.")

        ks = stright(points)
        #print(ks)

        try:
            if abs(ks["32"]-ks["43"]) < 0.5:
                cv2.putText(frame,"Left hand straight.",(20, 80), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame,"Left hand is not straight.",(20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_AA)
        except:
            pass
        try:
            if abs(ks["65"]-ks["76"]) < 0.5:
                cv2.putText(frame,"Right hand straight.",(20, 100), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame,"Right hand is not straight.",(20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_AA)
        except:
            pass
        
        try:
            if abs(ks["32"]) < 0.35 and abs(ks["43"]) < 0.35:
                cv2.putText(frame,"Left hand is level.",(20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame,"Left hand is not level.",(20, 120), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2, cv2.LINE_AA)
        
        except:
            pass

        try:
            if abs(ks["65"]) < 0.35 and abs(ks["76"]) < 0.35:
                cv2.putText(frame,"Right hand is level.",(20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame,"Right hand is not level.",(20, 120), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2, cv2.LINE_AA)
        
        except:
            pass

        try:
            angs_list=ca_all_ang(ang_list)
        except Exception as e:
            #print(e)
            pass

        print("*"*20)
        print(angs_list)
            

        

        cv2.imshow("frame", frame)
        key_code = cv2.waitKey(1)
        if key_code in [27, ord('q')]:
            break
    camera.release()
    cv2.destroyAllWindows()
