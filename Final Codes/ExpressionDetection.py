from PyQt5.QtWidgets import QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QDir, Qt, QUrl
from imutils.video import VideoStream
from keras.models import load_model
from tkinter import *
from imutils import face_utils
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QIcon
from time import sleep
import numpy as np
import datetime
import argparse
import imutils
import tkinter
import math
import time
import dlib
import cv2
import sys




class GazeEstimator():

	def __init__(self):
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
		
	def detectFace(self, gray_frame):
		rects = self.detector(gray_frame)
		rect = None
		
		for rect in rects:
			return rect
		
		return rect



class EmotionPredictor():

	def __init__(self):
		self.model = load_model('fer-2013.hdf5')
	
	
	def getExpression(self, face_frame):
		face_frame = cv2.resize(face_frame, (48, 48))
		face_frame = face_frame.astype('float32') / 255
		face_frame = np.asarray(face_frame)
		face_frame = face_frame.reshape(1, 1, face_frame.shape[0], face_frame.shape[1])
		facial_expression = self.model.predict(face_frame)
		
		return facial_expression



class VideoWindow(QMainWindow):

	def preliminaryHistogramEqualization(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
		h, s, v = cv2.split(frame)
		v = cv2.equalizeHist(v)
		frame = cv2.merge([h, s, v])
		frame = cv2.cvtColor(frame, cv2.COLOR_HSV2RGB)
		
		return frame
		
	
	def find_parameters(self):
		try:
			dataFile = open('gaze.conf', 'r')
			lines = dataFile.read().split('\n')[:-1]

			for i in range(len(lines)):
				lines[i] = lines[i].split(', ')
		
			line = lines[0]
			eye_width_sum = int(line[0])
			width_range = int(line[1])
		
			return eye_width_sum, width_range
		
		except:
			return self.bias_const, self.width_bias
			

	
	def fileNameFromTime(self):
		date_time = datetime.datetime.now()
		date_time = str(date_time)
		date_time = date_time.replace(":", "-")
		date_time = date_time.replace(" ", "-")
		date_time = date_time.replace(".", "")
		date_time = "../Output/" + date_time + ".txt"
		
		return date_time
		
		
	def gaze_position_estimation(self, eye_location, width, width_range):
		bias = width_range
		gaze_result = (eye_location + bias) * (width / (2*bias))
		
		return gaze_result
		
	
	def setDimention(self):
		root = tkinter.Tk()
		width = root.winfo_screenwidth()
		height = root.winfo_screenheight()
		dim = (width, height)		
		return dim  
	
		
	def openFile(self):
		#fileName, _ = QFileDialog.getOpenFileName(self, "Open Video File", QDir.homePath())
		fileName = "/home/ant/Documents/1 minute Video.mp4"
		bias_const, width_range = self.find_parameters()
		
		video_file_flag = (fileName != '') & fileName.endswith(".mp4")
		
		if video_file_flag == False:
			self.showMessage("Choose a valid video(.mp4) file.")
			return 
		
		cap = cv2.VideoCapture(fileName)
		capWebCam = cv2.VideoCapture(0)
			
		if (capWebCam.isOpened() != True):
			self.showWebcamError()
			return 
			
		cv2.namedWindow(fileName)
		cv2.moveWindow(fileName, 0, 0)
		tots = cap.get(cv2.CAP_PROP_POS_FRAMES)
			
		status = 'play'
		emotionModel = EmotionPredictor()
		gazeModel = GazeEstimator()
		
		preference = 'center'
		show_prefer = np.array([500, 500])
		visual_prefer_x = np.array([0, 0, 0, 0, 0])
		target = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

		facial_expression = np.array([0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.16])
		w_file_name = self.fileNameFromTime()
		fileWriter = open(w_file_name, "w")
			
		frame_index = -1
		face_identified = 0
		result = 'neutral'
		dim = self.setDimention()
		scrn_width = dim[0]
		show_prefer[1] = dim[1]//2
			
		while (cap.isOpened()):
			frame_index = frame_index + 1
			cv2.namedWindow(fileName, cv2.WINDOW_NORMAL);
			cv2.setWindowProperty(fileName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
			visual_prefer_x[(frame_index % 5)] = 0
			
			try:
				ret, image = cap.read()
				
				if image is None:
					fileWriter.close()
					capWebCam.release()
					cv2.destroyWindow(fileName)
					return 
					  
				image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

				if frame_index % 5 == 0:
					face_identified = 0
				
				if face_identified == 0:
					result = " "
					
				status = {ord('q'): 'exit', ord('Q'): 'exit',
						  -1: status, 27: 'exit'}[cv2.waitKey(1)]

				retWebCam, frame = capWebCam.read()
				frame = self.preliminaryHistogramEqualization(frame)
					
				gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
				
				rect = gazeModel.detectFace(gray)  
				if rect is None:
					cv2.imshow(fileName, image)
					continue     

				# facial expression recognition
				face_crop = gray[rect.top():rect.bottom(), rect.left():rect.right()]
				facial_expression = facial_expression + emotionModel.getExpression(face_crop)
				     
				if frame_index % 5 == 0:
					   
					result = target[np.argmax(facial_expression)]
					facial_expression = np.array([0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.16])
				
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(image, result, (50, 50), font, 1, (200, 0, 0), 3, cv2.LINE_AA)
				cv2.imshow(fileName, image)
				
				if status == 'play':
					frame_rate = cv2.getTrackbarPos('F', 'image')
					continue

				if status == 'exit':
					fileWriter.close()
					capWebCam.release()
					cv2.destroyWindow(fileName)
					return 

			except:
				pass

		fileWriter.close()
		capWebCam.release()
		cv2.destroyWindow(fileName)
	
	
	def showMessage(self, msg):
		master = tkinter.Tk()
		w_message = Message(master, text=msg, width=700)
		w_message.pack(padx=10, pady=20)
		Button(master, text='Close', command=lambda:self.remove_ui(master)).pack(pady=4)
		master.resizable(False, False)
		master.mainloop()
	
	
	def showWebcamError(self):
		error_master = tkinter.Tk()
		w_message = Message(error_master, text="Can not open webcam.", width=700)
		w_message.pack(padx=10, pady=20)
		Button(error_master, text='Close', command=lambda:self.remove_ui(error_master)).pack(pady=4)
		error_master.resizable(False, False)
		error_master.mainloop()
	
	
	def __init__(self, parent=None):
		super(VideoWindow, self).__init__(parent)

		self.width_bias = 30
		self.bias_const = 200
		self.openFile()
		
	
	def exitCall(self):
		sys.exit(app.exec_())



if __name__ == '__main__':
	app = QApplication(sys.argv)
	player = VideoWindow()
	player.resize(640, 480)
	player.show()
	sys.exit(app.exec_())
