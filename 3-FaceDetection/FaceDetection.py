import cv2
import time 
import operator
import requests
import numpy as np
import datetime

# local modules
from video import create_capture
from common import clock, draw_str

wait_seconds = 5
_url = 'https://api.projectoxford.ai/vision/v1.0/describe?maxCandidates=1'
_key = 'e721e9eb5d754f14a173b90a038bfea7' #Here you have to paste your primary key''
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
		print 'ok'
		print timer
		
		result = processRequest( json, data, headers, params )
		print (result)
		
		timer = datetime.datetime.today()
		
		return timer
	else :
		return timer
	
def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            #print( "Message: %s" % ( response.json()['error']['message'] ) )

        break
        
    return result
	
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
	params = { 'visualFeatures' : 'Color,Categories'} 

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



