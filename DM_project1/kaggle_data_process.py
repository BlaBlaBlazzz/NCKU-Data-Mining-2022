import csv
import FP_growth

def load_kaggle_data(filepath):
    with open(filepath, newline='') as csvfile:
        rows = csv.reader(csvfile)
        features = []
        for row in rows:
            features.append(row)
    
    #delete 'Movie name' and the title list
    for f in features:
        del f[0]
    del features[0]

    final_features = []
    for f in features:
        tmp_f = []
        # Release Period
        if f[0] == 'Normal':
            tmp_f.append('A')
        elif f[0] == 'Holiday':
            tmp_f.append('B')
        
        # Whether Remake
        if f[1] == 'Yes':
            tmp_f.append('C')
        elif f[1] == 'No':
            tmp_f.append('D')
        
        # Whether Franchise
        if f[2] == 'Yes':
            tmp_f.append('E')
        elif f[2] == 'No':
            tmp_f.append('F')
        
        # Genre
        if f[3] == 'drama':
            tmp_f.append('G')
        elif f[3] == 'comedy':
            tmp_f.append('H')
        elif f[3] == 'thriller':
            tmp_f.append('I')
        elif f[3] == 'action':
            tmp_f.append('J')
        elif f[3] == 'love_story':
            tmp_f.append('K')
        else:
            tmp_f.append("L")
        
        # New Actor
        if f[4] == 'Yes':
            tmp_f.append('M')
        elif f[4] == 'No':
            tmp_f.append('N')
        
        # New Director
        if f[5] == 'Yes':
            tmp_f.append('O')
        elif f[5] == 'No':
            tmp_f.append('P')
        
        # New Music Director
        if f[6] == 'Yes':
            tmp_f.append('Q')
        elif f[6] == 'No':
            tmp_f.append('R')
        
        # Lead Star
        if f[7] == 'Akshay Kumar':
            tmp_f.append('S')
        elif f[7] == 'Ajay Devgn':
            tmp_f.append('T')
        else:
            tmp_f.append('U')

        # Director
        if f[8] == 'Ram Gopal Verma':
            tmp_f.append('V')
        elif f[8] == 'Vikram Bhatt':
            tmp_f.append('W')
        else:
            tmp_f.append('X')
        
        # Music Director
        if f[9] == 'Pritam':
            tmp_f.append('Y')
        elif f[9] == 'Himesh Reshammiya':
            tmp_f.append('Z')
        else:
            tmp_f.append('AA')
        
        # Number of Screens
        if int(f[10]) < 460 :
            tmp_f.append('AB')
        else:
            tmp_f.append('AC')
        
        # Revenue(INR)
        if int(f[11]) < 210292500:
            tmp_f.append('AD')
        else:
            tmp_f.append('AE')
        
        # Budget(INR)
        if int(f[12]) < 801618525:
            tmp_f.append('AF')
        else:
            tmp_f.append('AG')
        final_features.append(tmp_f)

    return final_features
        


# data = load_kaggle_data('kaggle-Bollywood Movies Dataset.csv')
# #print(data)
# ass = FP_growth.association_rule(data, 0.5, 0.1)
# print(len(ass))