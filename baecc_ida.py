import sys, os, time
from scipy import ndimage
from scipy import misc
import scipy.io
from matplotlib.image import AxesImage
from pylab import *
import numpy as np
import subprocess
import glob
import shutil
from PIL import Image, ImageDraw, ImageChops, ImageFilter
import matplotlib.pyplot as plt
import datetime,time
from os.path import join, getsize
import re
import h5py

f=0

def hotplate(date):
	global f
	date_str = time.strftime("%Y%m%d",date)
	files = glob.glob("data/Hotplate/hot_plate_100901_"+date_str+"*")
	acc = []
	time_ = []
	for filename in files:
		file_ = open(filename)
		lines = file_.readlines()
		file_.close
		for i in lines:
			var = i.split(',')
			print len(var)
			if len(var) > 0:
				time_tmp = time.strptime(var[0],'%Y%m%d%H%M%S')
				time_tmp = time.mktime(time_tmp)
				time_.append(time_tmp)
				acc.append(var[-1])
	#print acc
	dset = f.create_dataset("hotplate_accumulation", (len(acc),), data=acc)
	dset = f.create_dataset("hotplate_accumulation_time", (len(time_),), data=time_)

def jeoptic(date):
	global f
	date_str = time.strftime("%Y%m%d",date)
	files = glob.glob("data/Jenoptik/"+date_str+"*")
	print date_str
	snow = []
	time_ = []
	data_=[]
	for filename in files:
		file_ = open(filename)
		lines = file_.readlines()
		file_.close
		for i in lines:
			var = i.split(',')
			print len(var)
			if len(var) > 0:
				time_tmp = time.strptime(var[0],'%Y-%m-%d %H:%M:%S')
				time_tmp = time.mktime(time_tmp)
				time_.append(time_tmp)
				snow.append(var[-1])
	#print acc
	data_ = [time_,snow]
	dset = f.create_dataset("snow_depth", (len(snow),), data=snow)
	dset = f.create_dataset("snow_depth_time", (len(time_),), data=time_)

def great_hdf5(date):
	global f
	date_str = time.strftime("%Y%m%d",date)
	f = h5py.File(date_str + ".hdf5", "w")
	dset = f.create_dataset("basetime", (1,), dtype='i')
	#readhotpalte
	hotplate(date)
	#read jenoptic
	jeoptic(date)

def main():
	tmp=(2014,02,06,0,0,0,0,0,0)
	date=time.mktime(tmp)
	date = time.gmtime(date)
	print date
	great_hdf5(date)

main()
