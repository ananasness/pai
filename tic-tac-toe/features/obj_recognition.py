import sys, os
import wikipedia
sys.path.append(os.path.join(os.getcwd(), '../darknet/python/'))

from darknet import *
from features.classifier import *


class ObjRecognition:
    def __init__(self):
        prefix = b"../../darknet/"
        self.net = load_net(prefix + b"cfg/yolov3.cfg", prefix + b"yolov3.weights", 0)
        self.meta = load_meta(prefix + b"cfg/coco.data")

    def get_info_about(self, img_path):
        objs = detect(self.net, self.meta, img_path.encode('utf-8'))
        res = "Sorry, I couldn't get what's on the picture"
        if len(objs):
            if objs[0][0].decode('utf-8') == 'person':
                per, conf = person_infer("../../classifier.pkl", img_path)
                if conf > 0.7:
                    res = "Oh! That's a member of our team - " + per
                elif conf > 0.5:
                    res = "I have a feeling that that's a member of our team - " + per
                else:
                    res = wikipedia.page(objs[0][0].decode('utf-8')).url
            else:
                res = wikipedia.page(objs[0][0].decode('utf-8')).url
        return res
