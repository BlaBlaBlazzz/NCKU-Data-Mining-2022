import csv
import random
import numpy as np

with open("data.csv", 'w', newline='') as w:
    writer = csv.writer(w)

    #write feature title
    writer.writerow(['lead', 'chromium', 'mercury', 'arsenic', 'copper', 'nickel',
                    'zinc', 'aluminium', 'perchlorate', 'chloramine', 'radium', 'silver',
                    'uranium', 'selenium', 'cadmium', 'ammonia', 'biological adsorption', 'phytoremediation', 'output'])
    
    #generate random data
    for i in range(1000):
        data = []
        for num in range(18):
            data.append(random.randint(0, 1))
        
        threshold = data[7] + data[14] + data[9]
        output = 0
        if data[8] == 1:
            output = 1
        if threshold >= 2:
            output = 1
        if data[16] == 1:
            output = 0
        if data[17] == 1:
            if data[8] + threshold < 3:
                output = 0
        
        data.append(output)

        writer.writerow(data)


    

