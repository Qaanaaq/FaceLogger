import cv2
import dlib
import os
import csv
import open_files
import pandas as pd

def normalize(videofile, param):


    filebasedir= os.path.dirname(videofile)
    filenaming= os.path.basename(videofile)
    filenaming= os. path. splitext(filenaming)[0]

    #csv
    with open(filebasedir + '/delta_facs_' + filenaming + '.csv', newline='') as csvfile:
        temp_reader = csv.reader(csvfile, delimiter=',')

        data = list(temp_reader)
        row_count = len(data)
        column_count= len(data[0])-2
        frame_count = row_count - 1

    try:
        print (f"Rows: {row_count}")
        print (f"Columns: {column_count}")
    except IndexError:
        print('No data found')


    for nn in range (1, column_count):
        temp_max = 0
        for n in range(1, row_count):
            cell = float(data[n][nn])
            cell = abs(cell)
            if cell > temp_max:
                temp_max = cell


        with open(filebasedir + '/delta_facs_' + filenaming + '.csv', 'r+', newline='') as csvfile:
            temp_reader = csv.reader(csvfile, delimiter=',')

            for n in range(1, row_count):
                cell = float(data[n][nn])
                cell = cell / temp_max
                cell ="%.2f" % round(cell, 2)
                data[n][nn] = cell

    #print (data)
    with open(filebasedir + '/delta_facs_' + filenaming + '_normalized.csv', 'w', newline='') as csvfile:
        temp_writer = csv.writer(csvfile, delimiter=',')
        title = ["Frame", "MouthOpen", "MouthWide", "JawOpen", "MouthCorner_Left", "MouthCorner_Right","UpperLipRaiser","LowerLipRaiser","LipPresser","EyeBlink", "InnerBrowRaiser", "OuterBrowRaiser","BrowLowerer", "EyeHoriz", "EyeVert"]
        temp_writer.writerow(title)
        for n in range(1, frame_count):
            temp_writer.writerow(data[n])

    temporary = (filebasedir + '/delta_facs_' + filenaming + '.csv')
    os.remove(temporary)
    os.rename(filebasedir + '/delta_facs_' + filenaming + '_normalized.csv',filebasedir + '/delta_facs_' + filenaming + '.csv')
    print("Normalization done!")
    param.config(text = "Normalizing done!")
