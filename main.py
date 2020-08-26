import cv2
from tools.OpenPose import OpenPose
import math
import traceback


hands = False
ans = True
right_ang = 0
left_ang = 0
ang_list = [["8","9","10"],["11","12","13"],["1","2","3"],["1","5","6"],["1","8","9"],["1","11","12"]]
left_body = ["156","11112","111213"]
right_body = ["123","189","8910"]
jud = ["80-100","150-170","140-160"]
angs_list = []
points = {}
ds = "Left"
left_stright = False
right_stright = False
passs = True

def check_dict_keys(dict,target,hand="Left"):
    global ans, ds
    for i in dict.keys():
        if i not in target:
            ans = False
            ds = ""
            return ans
        else:
            ans = True
    ds = hand
    return ans

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
    if pgroup[0] in points.keys() and pgroup[1] in points.keys() and pgroup[2] in points.keys():
        ang_c = math.atan2(points[pgroup[2]][1]-points[pgroup[1]][1],points[pgroup[2]][0]-points[pgroup[1]][0])*180/math.pi
        ang_d = math.atan2(points[pgroup[1]][1]-points[pgroup[0]][1],points[pgroup[1]][0]-points[pgroup[0]][0])*180/math.pi
        tang = round(180 + ang_c - ang_d)
        return tang
    else:
        return 0


def ca_all_ang(ang_list):
    angs = {}
    for i in ang_list:
        if bool(ca_ang(i)) is False:
            continue
        else:
            angs["".join(i)] = ca_ang(i)
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
                left_stright = True
                cv2.putText(frame,"Left hand straight.",(20, 80), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 255), 2, cv2.LINE_AA)
            else:
                left_stright = False
                cv2.putText(frame,"Left hand is not straight.",(20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_AA)
        except:
            pass
        try:
            if abs(ks["65"]-ks["76"]) < 0.5:
                right_stright = True
                cv2.putText(frame,"Right hand straight.",(20, 100), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 255), 2, cv2.LINE_AA)
            else:
                right_stright = False
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
        
        if check_dict_keys(angs_list,left_body,hand="Left") or check_dict_keys(angs_list,right_body,hand="Right"):
            print("ok")
            passs = True
            if ds == "Left":
                if left_stright:
                    for i in range(len(jud)-1):
                        if not int(jud[i].split("-")[0]) <= angs_list[left_body[i]] <= int(jud[i].split("-")[1]):
                            passs = False
                        else:
                            passs = True
                else:
                    passs = False
            elif ds == "Right":
                if right_stright:
                    for i in range(len(jud)-1):
                        if int(jud[i].split("-")[0]) <= angs_list[right_body[i]] <= int(jud[i].split("-")[1]):
                            passs = True
                        else:
                            passs = False
                else:
                    passs = False
            else:
                passs = False
        else:
            passs = False
        
        print(passs)              


        print(angs_list)
        cv2.imshow("frame", frame)
        key_code = cv2.waitKey(1)
        if key_code in [27, ord('q')]:
            break
    
    camera.release()
    cv2.destroyAllWindows()
