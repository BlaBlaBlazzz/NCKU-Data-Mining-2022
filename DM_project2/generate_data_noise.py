import csv
import random
import numpy as np

with open("data_with_noise.csv", 'a+', newline='') as w:
    writer = csv.writer(w)

    #gernerate noise data
    for i in range(200):
        data = []
        for feature in range(19):
            data.append(random.randint(0, 1))
        writer.writerow(data)
