import cv2
import time 
import operator
import requests
import numpy as np
import datetime
import httplib, urllib, base64

# local modules
from video import create_capture
from common import clock, draw_str

wait_seconds = 5

_key = 'XXXXX' #Here you have to paste your primary key''
_maxNumRetries = 10



def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


def timer_ok(timer, json, data, headers, params):
	if (datetime.datetime.today() - timer).total_seconds() > wait_seconds:
		print('ok')
		print timer
		
		result = processRequest( json, data, headers, params )
		print (result)
		
		timer = datetime.datetime.today()
		
		return timer
	else :
		return timer
	

def processRequest( json, data, headers, params ):

	try:
		conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
		conn.request("POST", "/face/v1.0/detect?%s" % params, data, headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

	
if __name__ == '__main__':
	import sys, getopt
	print(__doc__)

	args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
	try:
		video_src = video_src[0]
	except:
		video_src = 1
	args = dict(args)
	
	# Computer Vision parameters
	params = urllib.urlencode({
	# Request parameters
	'returnFaceId': 'true',
	'returnFaceLandmarks': 'false',
	'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
	})

	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/octet-stream' 
	
	json = None
	
	timer = datetime.datetime.today()
	
	cascade_fn = args.get('--cascade', "opencv_data/haarcascade_frontalface_alt.xml")
	nested_fn  = args.get('--nested-cascade', "opencv_data/haarcascade_eye.xml")

	cascade = cv2.CascadeClassifier(cascade_fn)
	nested = cv2.CascadeClassifier(nested_fn)

	cam = create_capture(1, fallback='synth:bg=../data/lena.jpg:noise=0.05')
	rval, frame = cam.read()
	
	while rval:
		
		rval, frame = cam.read()	
		
		cv2.imwrite('photo.png',frame)
		data = open('photo.png', 'rb').read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.equalizeHist(gray)

		t = clock()
		rects = detect(gray, cascade)
		vis = frame.copy()
		draw_rects(vis, rects, (0, 255, 0))
		if not nested.empty():
			for x1, y1, x2, y2 in rects:
				roi = gray[y1:y2, x1:x2]
				vis_roi = vis[y1:y2, x1:x2]
				subrects = detect(roi.copy(), nested)
				draw_rects(vis_roi, subrects, (255, 0, 0))
				timer = timer_ok( timer, json, data, headers, params )
		dt = clock() - t

		draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
		cv2.imshow('facedetect', vis)
		
				
		key = cv2.waitKey(20)
		if key == 27: # exit on ESC
			break
	cv2.destroyWindow("preview")



