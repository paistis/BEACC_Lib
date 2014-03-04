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
import pandas as pd


def hotplate(date):
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
			if len(var) > 0:
				time_tmp = time.strptime(var[0],'%Y%m%d%H%M%S')
				time_tmp = time.mktime(time_tmp)
				time_.append(time_tmp)
				acc.append(float(var[-1]))
	
	#print acc
	d = {'hotplate_time' : time_, 'hotplate_accumulation': acc}
	return pd.DataFrame(d)

def jeoptic(date):
	date_str = time.strftime("%Y%m%d",date)
	files = glob.glob("data/Jenoptik/"+date_str+"*")
	snow = []
	time_ = []
	data_=[]
	for filename in files:
		file_ = open(filename)
		lines = file_.readlines()
		file_.close
		for i in lines:
			var = i.split(',')
			if len(var) > 0:
				time_tmp = time.strptime(var[0],'%Y-%m-%d %H:%M:%S')
				time_tmp = time.mktime(time_tmp)
				time_.append(time_tmp)
				snow.append(float(var[2])-0.034)
	#print acc
	d = {'jenoptik_time' : time_, 'jenoptik_snow_depth': snow}
	return pd.DataFrame(d)

def parsivel23(date):
	date_str = time.strftime("%Y%m%d",date)
	files = glob.glob("data/Parsivel23/"+date_str+"*")	
	

def great_hdf5(date):
	date_str = time.strftime("%Y%m%d",date)
	f = h5py.File(date_str + ".hdf5", "w")
	dset = f.create_dataset("basetime", (1,), dtype='i')
	#read date from different device
	hotplate_data = hotplate(date)
	jenoptik_data = jeoptic(date)
	
	#jenoptik
	dset = f.create_dataset("jenoptik_time", (len(jenoptik_data['jenoptik_time'].values),), data=jenoptik_data['jenoptik_time'].values)
	dset = f.create_dataset("jenoptik_snow_depth", (len(jenoptik_data['jenoptik_snow_depth'].values),), data=jenoptik_data['jenoptik_snow_depth'].values)

	#hotplate
	dset = f.create_dataset("hotplate_time", (len(hotplate_data['hotplate_time'].values),), data=hotplate_data['hotplate_time'].values)
	dset = f.create_dataset("hotplate_accumulation", (len(hotplate_data['hotplate_accumulation'].values),), data=hotplate_data['hotplate_accumulation'].values)
	
def main():
	tmp=(2014,02,06,0,0,0,0,0,0)
	date=time.mktime(tmp)
	date = time.gmtime(date)
	great_hdf5(date)

main()
