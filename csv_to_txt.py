'''
This program will convert a CSV file to a text file.
The main purpose is to re-use the Movielens dataset and visualise it using
a graph and the tSNE software.

Quentin Deligny
'''

from pathlib import Path
from utility_functions import *
from omdb import get_metadata
#from spotlight.validator import Validator
import csv
import numpy as np

#Some rows are poorly formatted an run over multiple lines
def concat_rows(rows):
    i = 0
    for row in rows:
        if(row[0].isnumeric()) is not True:
            rows[i-1] = rows[i-1] + rows[i]
            del rows[i]

            
        i += 1

    return(rows)

#Some rows are poorly formatted with multiple entries per line
def reduce_row(row):
    
    reduceRow = ''
    for i in range(len(row)):
        reduceRow += row[i]

    return([reduceRow])


def assignMovieTitle100kData(file):

    listOfIds = []
    listOfTitles = []
    with open(file, "r") as outputFile:
        for row in csv.reader(outputFile):

            currentRowId = ''
            currentRowTitleYear = ''
            i = 0
            
            #each row is a list containing 1 string, however some contain multiple entries
            row = reduce_row(row)
            #print(type(row),len(row))
            
            while (row[0][i] != '|'):
                currentRowId += row[0][i]
                i += 1

            i += 1
            #print(len(row[0]))
            #print(row)
            #print(row[0][i])
            while (row[0][i] != '|'):
                currentRowTitleYear += row[0][i]
                i += 1
                
            listOfIds += [int(currentRowId)]
            listOfTitles += [currentRowTitleYear]

    outputFile.close()
    
    listOfTitles = stripYears(listOfTitles)

    file1 = "ml-100k/all_titles_100k.txt"
    file2 = "ml-100k/all_ids_100k.txt"

    with open(file1, 'w') as f:
        for item in listOfTitles:
            f.write("%s\n" % item)
    f.close()
                
    with open(file2, 'w') as d:
        for item in listOfIds:
            d.write("%s\n" % item)
    d.close()
    

    
def assignMovieGenre(file, file2):
    '''
    #Stores all the rows within the dataset
    allRows = []
    #Only stores rows whose id is found in the movieIdArray
    with open(file, "r",encoding = 'utf8') as outputFile:
        for row in csv.reader(outputFile):
            
            if 'movieId title genres' in row:
                continue
            
            if(len(row)>1):
                row = reduce_row(row)

            allRows += row
            
    outputFile.close()
    
    rows = concat_rows(allRows)
    rowTitles, rowGenres = stripRows(rows)
    '''
    allTitles100k = []
    allGenres100k = []
    
    #We now load the rows from the 100k dataset to assign genres to them
    with open(file2, "r") as outputFile:
        for row in csv.reader(outputFile):
            allTitles100k += row
    outputFile.close()

    for title in allTitles100k:
        metadata = get_metadata([title],True, False)
        try:
            titleGenre = metadata[0][3]
        #Could not find movie on OMDb
        except:
            titleGenre = "None"
        allGenres100k += [titleGenre]
        

    '''
    for title in allTitles100k:
        if title in rowTitles:
            k = rowTitles.index(title)
            associatedGenre = rowGenres[k]
            allGenres100k += [associatedGenre]
        else:
            allGenres100k += ['None']
    '''
    return(allGenres100k)
    

def getMovieTitleGenre(file, file2,arrayOfIds,allSingleGenre):
    '''
    Returns arrays of titles and genres (only one genre per item).
    file: file containing all titles
    file2: file containing all ids
    arrayOfIds: array for which we want to return titles and genres
    allSingleGenre: array containing all genres for each item (one per item)
    '''
    selectedTitles = []
    selectedGenres = []
    
    allTitles = []
    allIds = []
    with open(file, "r") as outputFile:
        for row in csv.reader(outputFile):
            allTitles += [row]
    outputFile.close()
    with open(file2, "r") as outputFile:
        for row in csv.reader(outputFile):
            allIds += [row]
    outputFile.close()

    
    for currentId in arrayOfIds:
        k = allIds.index([currentId])
        selectedTitles += allTitles[k]
        selectedGenres += [allSingleGenre[k]]
        
    return selectedTitles,selectedGenres
        
                
def assignMovieIds (ratings,titleFile,idFile):
    
    userRatings = np.asarray(ratings)
    titles = userRatings[0::2]
    ratedIds = []
    allRowTitles = []
    allIds = []
    
    with open(titleFile, "r") as outputFile:
        for row in csv.reader(outputFile):
            allRowTitles += row
    outputFile.close()
    with open(idFile, "r") as outputFile2:
        for row in csv.reader(outputFile2):
            allIds += row
    outputFile2.close()
        
    for title in titles:
        k = allRowTitles.index(title)
        movieId = allIds[k]
        ratedIds += [movieId]

    return (ratedIds,userRatings[1::2])

def assignSingleLabel(movieIdArray,arrayOfGenres,idFile,showNone):
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

    #Both arrays will have the same length, containing the entire data from the loaded file.
    movieIdArray = []
    with open(idFile, "r") as outputFile2:
        for row in csv.reader(outputFile2):
            movieIdArray += row
    outputFile2.close()


    for i in range(len(arrayOfGenres)):
        currentGenres = arrayOfGenres[i]

        #used to add the first genre in the possible genres
        alphabeticalOrder = True
        for genre in possibleGenres:
            if genre in currentGenres and (alphabeticalOrder):
                arrayOfGenres[i] = genre
                alphabeticalOrder = False

    #Array no longer contains multiple genres
    for label in arrayOfGenres:
        print(label)
        genresAsColours += [genresToColours[label]]

        
    return(genresAsColours, movieIdArray, arrayOfGenres)
            
        
        
    

def csvToText(inputFile, outputFile):
    #data_folder = Path("ml-latest-small/")
    csv_file1 = "ml-latest-small/movies.csv"
    txt_file1 = "ml-latest-small/movielens_movies.txt"

    with open(txt_file1, "w",encoding = 'utf8') as my_output_file:
        with open(csv_file1, "r",encoding = 'utf8') as my_input_file:
            for row in csv.reader(my_input_file):
                my_output_file.write(" ".join(row)+'\n')
            
        print('File Successfully written.')
        my_output_file.close()


# old deprecated functions which was working for a different extraction method
'''
def assignMovieTitle(file,option,movieIdArray=[]):
    
    allIds = []
    #Stores all the rows within the dataset
    allRows = []
    #Only stores rows whose id is found in the movieIdArray
    rows = []
    previousRow = ''
    mapping = {}
    with open(file, "r",encoding = 'utf8') as outputFile:
        for row in csv.reader(outputFile):
            
            if 'movieId title genres' in row:
                continue

            
            rowId = ''
            i = 0
            intId = 0
            while (row[0][i].isnumeric()):
                rowId += row[0][i]
                i+=1
                
            intId = int(rowId)

            #print(row[0][0].isnumeric(),intId)
            
            if(len(row)>1):
                row = reduce_row(row)

            if (option):
                if(intId>=np.amax(movieIdArray)) and (row[0][0].isnumeric()) and (intId not in allIds):
                    allIds += [intId]
                    allRows += row

            if(intId in movieIdArray) and (row[0][0].isnumeric()) and (intId not in allIds):
                    rows += row
                    allRows += row
                    allIds += [intId]

                
         
                
    if (option == False):
        rows = concat_rows(rows)
        #print(rows)
        rowTitles, rowGenres = stripRows(rows)
        #print(rowTitles)
        return (rowTitles,rowGenres)

                
    else:
        allRows = concat_rows(allRows)
        allRows = np.asarray(allRows)
        allRows = allRows[:len(allIds)].tolist()
        allRowTitles, allRowGenres = stripRows(allRows)
        dest_file = "ml-latest-small/all_titles.txt"
        dest_file_ids = "ml-latest-small/all_ids.txt"

        with open(dest_file, 'w') as f:
            for item in allRowTitles:
                f.write("%s\n" % item)
                
        with open(dest_file_ids, 'w') as d:
            for item in allIds:
                d.write("%s\n" % item)

        return allRowTitles





def assignSingleLabel(movieIdArray, file, showNone, showMultiple):
    movieIdArray: Array of integers with the IDs of Movies that need to be assigned labels.
    file: name of the file where the labels & movie IDs are stored independently.
    showNone: if True, show movies with no corresponding label in the movielens dataset.
    showMultiple: if True, plot will show movies with multiple labels by assigning them only one label.
    
    Returns movieGenreArray, an array of labels corresponding to the movieIdArray

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

'''    



