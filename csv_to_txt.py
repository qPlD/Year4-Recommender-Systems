'''
This program will convert a CSV file to a text file.
The main purpose is to re-use the Movielens dataset and visualise it using
a graph and the tSNE software.

Quentin Deligny
'''

from pathlib import Path
#from spotlight.validator import Validator
import csv
import numpy as np

def assignMovieTitle(movieIdArray,file):

    numbers = ['0','1','2','3','4','5','6','7','8','9']
    rows = []
    print(movieIdArray)
    with open(file, "r",encoding = 'utf8') as outputFile:
        for row in csv.reader(outputFile):
            
            if 'movieId title genres' in row:
                continue

            
            rowId = ''
            i = 0
            intId = 0
            while (row[0][i]) in numbers:
                rowId += row[0][i]
                intId = int(rowId)
                i+=1
                
            print(rowId)
            for ID in movieIdArray:
                
                #print("ID is",ID,type(ID))
                #print("row id is",intId,type(intId))
                if (ID == intId):
                    rows += row
    return (rows)
    

def assignSingleLabel(movieIdArray, file, showNone, showMultiple):
    '''
    movieIdArray: Array of integers with the IDs of Movies that need to be assigned labels.
    file: name of the file where the labels & movie IDs are stored independently.
    showNone: if True, show movies with no corresponding label in the movielens dataset.
    showMultiple: if True, plot will show movies with multiple labels by assigning them only one label.
    
    Returns movieGenreArray, an array of labels corresponding to the movieIdArray
    '''

    #List all 18 distinct genres for the movies
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    #Single Label Assignment will favour labels in the order they are listed
    possibleGenres = ['Action','Adventure','Animation','Children','Comedy','Crime',
                      'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
                      'Mystery','Romance','Sci-Fi','Thriller','War','Western']

    genresToColours = {'Action':'cornflowerblue',
                       'Adventure':'darkgrey',
                       'Animation':'lightcoral',
                       'Children':'red',
                       'Comedy':'orangered',
                       'Crime':'saddlebrown',
                       'Documentary':'orange',
                       'Drama':'darkgoldenrod',
                       'Fantasy':'gold',
                       'Film-Noir':'darkkhaki',
                       'Horror':'yellow',
                       'Musical':'yellowgreen',
                       'Mystery':'lawngreen',
                       'Romance':'aqua',
                       'Sci-Fi':'darkblue',
                       'Thriller':'indigo',
                       'War':'violet',
                       'Western':'deeppink',
                       'None':'black'}
    #This array will only contain the required labels
    idsToReturn = []
    movieGenreArray = []
    genresAsColours = []

    idNoLabel = []

    #Both arrays will have the same length, containing the entire data from the loaded file.
    arrayOfIds = []
    arrayOfGenres = []

    with open(file, "r",encoding = 'utf8') as outputFile:
        for row in csv.reader(outputFile):
            
            if 'movieId title genres' in row:
                continue
            rowId = ''
            i = 0
            intId = 0
            while (row[0][i]) in numbers:
                rowId += row[0][i]
                intId = int(rowId)
                i+=1
                
            

            
            block = row[len(row)-1]

            genreCount = 0
            for genre in possibleGenres:
                if genre in block:
                    rowgenre = genre
                    genreCount += 1

            if (showMultiple):
                arrayOfGenres += [rowgenre]
                arrayOfIds += [rowId]
            elif (genreCount ==  1):
                arrayOfGenres += [rowgenre]
                arrayOfIds += [rowId]
            else:
                arrayOfGenres += ["multi"]
                arrayOfIds += [rowId]
                
            if (intId > np.amax(movieIdArray)):
                break


        outputFile.close()


        
        for movieId in movieIdArray:
            idString = str(movieId)

            
            if idString in arrayOfIds:
                idIndex = arrayOfIds.index(idString)
                label = arrayOfGenres[idIndex]

            #Dataset IDs are not sequential, so the movieID may not be found
            elif(showNone):
                label = "None"
            else:
                idNoLabel += [movieId]
                continue

            
            #Case where we hide multilabels and show None labels
            if (label != "multi"):
                idsToReturn += [idString]
                movieGenreArray += [label]
            
            else:
                idNoLabel += [movieId]
            
            
    for genre in movieGenreArray:
        genresAsColours += [genresToColours[genre]]

        
    return(genresAsColours, idsToReturn, movieGenreArray, idNoLabel)
            
        
        
    

def csvToText(inputFile, outputFile):

    with open(txt_file1, "w",encoding = 'utf8') as my_output_file:
        with open(csv_file1, "r",encoding = 'utf8') as my_input_file:
            for row in csv.reader(my_input_file):
                my_output_file.write(" ".join(row)+'\n')
            
        print('File Successfully written.')
        my_output_file.close()

#data_folder = Path("ml-latest-small/")
csv_file1 = "ml-latest-small/movies.csv"
txt_file1 = "ml-latest-small/movielens_movies.txt"
#csvToText(csv_file1,txt_file1)

#testIds = [4,63,4460,216,34]
#print(testIds,assignSingleLabel(testIds,txt_file1))
    



