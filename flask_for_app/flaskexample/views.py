from flask import render_template
from flask import request
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import os
import numpy as np
import cv2
from skimage import io, exposure, transform, color

@app.route('/')
@app.route('/index')
def index():
    return render_template('master.html')

@app.route('/go', methods=['POST'])
def go():
    # import ipdb; ipdb.set_trace();
    file = request.files['query']
    uploads_root = '/Users/amyshapiro/flask_for_app/flaskexample/static/uploads'
    save_path = os.path.join(uploads_root, file.filename)
    url_path = os.path.join('/static/uploads', file.filename)
    file.save(save_path)
    best_match_image_url = find_best_match_image(save_path)
    return render_template(
        'go.html',
        filepath=url_path,
        best_match_image_url=best_match_image_url,
    )

def find_best_match_image(input_image_path):
    return input_image_path

def get_squares(img):
    """Take in a photo, return a top, bottom, and central square of the given size (centered)"""
    top_sq = img[110:130,115:135,:]
    mid_sq = img[165:185,115:135,:]
    bottom_sq = img[300:320, 115:135,:]
    return (top_sq, mid_sq, bottom_sq)

def get_hsv_histograms(img):
    """Takes in an image in HSV color space and returns an array of len = 692 which is the frequency
    of pixels with each Hue[0-180], Saturation[0-256], and Value[0-256]"""
    hue_hist = cv2.calcHist([img],[0],None,[180],[0,180])
    sat_hist = cv2.calcHist([img],[1],None,[256],[0,256])
    val_hist = cv2.calcHist([img],[2],None,[256],[0,256])
    hsv_hist = np.concatenate((hue_hist, sat_hist, val_hist))
    return hsv_hist

def process_image(img_file):
    """Takes in a path to a folder and returns processed image histogram frequency"""

    #Create an empty list to store the processed data
    frames = []

    #1. read in image
    img = cv2.imread(img_file, 1)

    #2. resize image if not 250(L) x 350(H)
    if img.size != (250, 350):
        img = cv2.resize(img, (250, 350))

    #3. convert image to HSV colorspace
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #4. get top, mid, and bottom squares
    square_trio = get_squares(img)

    #5. get histograms from each square
    top_hist = pd.DataFrame(get_hsv_histograms(square_trio[0]), columns = [os.path.basename(img_file)])
    mid_hist = pd.DataFrame(get_hsv_histograms(square_trio[1]), columns = [os.path.basename(img_file)])
    bottom_hist = pd.DataFrame(get_hsv_histograms(square_trio[2]), columns = [os.path.basename(img_file)])
    hist = top_hist.append(mid_hist, ignore_index = True).append(bottom_hist, ignore_index = True).transpose()
    frames.append(hist)

    data_df = pd.concat(frames)

    return data_df
