import pandas as pd #Imports pandas for additional csv output functions
import matplotlib.pyplot as plt #Imports matplotlib for Visualization
import numpy as np #Imports numpy for Visualizaton
pd.options.mode.chained_assignment = None #Removes warning given by pandas
pd.set_option('display.max_rows', None) #Prevents pandas from skipping rows
data = pd.read_csv("2021-12-merseyside-street.csv") #Imports csv file
data = data.dropna('columns','all') #Remove empty columns
menu = True #Menu variable set to true to make menu loop
BBox = -3.2238,-2.5735, 53.2993, 53.6861 #Bounding box values of map
map = plt.imread('map.png') #Stores map of Merseyside in variable

def ViewOnMap(searchResults,searchQuery): #Views specified coordinates on map
    longitude = searchResults[['Longitude']]
    latitude = searchResults[['Latitude']]
    fig, ax = plt.subplots(figsize = (8,7))
    ax.scatter(longitude, latitude, zorder=1, alpha= 0.2, c='b', s=10)
    ax.set_title(searchQuery+" Crime Rates")
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(map, zorder=0, extent = BBox, aspect= 'equal')
    plt.show()

def areaTocrimeGraph(): #Graph to see specified areas with specified crime
    searchColumn = 'Crime type'
    outputColumn = 'LSOA name'
    if plotGraph(searchColumn, outputColumn) == "Y":
        areaTocrimeGraph()

def plotCrimeToAreaGraphs(): #Graph to see crime types in a specified area
    searchColumn = 'LSOA code'
    outputColumn= 'Crime type'
    if plotGraph(searchColumn, outputColumn) == "Y":
        plotCrimeToAreaGraphs()

def plotCrimeToAreaGraphLine(): #Graph to see crime types in a specified area (in a line graph format)
    columnSearch = 'LSOA code'
    columnOutput= 'Crime type'
    df = pd.DataFrame(data,columns=[columnSearch,columnOutput])
    plt.plot(df[columnSearch], df[columnOutput], color='black', marker='o')
    plt.title('Area to Crime Graph', fontsize=14)
    plt.ylabel('Crime Rate', fontsize=14)
    plt.grid(True)            
    plt.show()

def lastOutcomeToCrimeGraph(): #Graph to see last outcome crime types
    searchColumn = 'Last outcome category'
    outputColumn = 'Crime type'
    if plotGraph(searchColumn,outputColumn) == "Y":
        lastOutcomeToCrimeGraph()

def plotAreaToOutcomeGraph(): #Graph to see the amount different outcomes in a selected area
    searchColumn = 'LSOA code'
    outputColumn = 'Last outcome category'
    if plotGraph(searchColumn,outputColumn) == "Y":
        plotAreaToOutcomeGraph()

def SearchByCrime(): #Search by the crime type
    searchColumn = 'Crime type'
    uniqueValues = data[searchColumn].unique()
    print("Choose from the following crimes:") 
    searchDataFrame(uniqueValues,searchColumn) 
    
def SearchByArea(): #Search by the area (LSOA name)
    searchColumn = 'LSOA name'
    uniqueValues = data[searchColumn].unique()
    print("Choose from the following areas:")
    searchDataFrame(uniqueValues,searchColumn)

def SearchByStreet(): #Search by the street (Location)
    searchColumn = 'Location'
    uniqueValues = data[searchColumn].unique()
    print("Choose from the following areas:")
    searchDataFrame(uniqueValues,searchColumn)

def SearchByOutcome(): #Search by the last outcome category
    searchColumn = 'Last outcome category'
    uniqueValues = data[searchColumn].unique()
    print("Choose from the following areas:")
    searchDataFrame(uniqueValues,searchColumn)

def searchDataFrame(uniqueValues,searchColumn): #Searches dataframe for specified input
    for count,option in enumerate(uniqueValues): #Number elements in list
        print (count,option) #Output numbered list
    searchQuery = input("Enter option number or search query:")
    if searchQuery.isnumeric(): #Checks if input is a number
        searchQuery = uniqueValues[int(searchQuery)] #If input is number, get that element from the list
    searchResults = data[data[searchColumn].str.contains(searchQuery, case=False, na=False)]
    if searchResults.empty:
        print("No results found")
    else:
        print(searchResults)
        if input("View results on map? Y/N").upper() == "Y": #Converts input to uppercase so that lowercase can be accepted
            ViewOnMap(searchResults,searchQuery)

def plotGraph(searchColumn,outputColumn): 
    uniqueValues = data[searchColumn].dropna().unique() #Remove empty columns and find unique values in specified dataset column
    for count,option in enumerate(uniqueValues): #Number elements in list6
        print (count,option) #Output numbered elements in list
    searchQuery = input('Enter option number or search query:') 
    if searchQuery.isnumeric(): #Checks if input is a number
        searchQuery = uniqueValues[int(searchQuery)] #If input is number, get that element from the list
    searchResults = data.loc[data[searchColumn].str.contains(searchQuery, case=False, na=False)]
    if searchResults.empty:
       print("No results found")
    else:
        searchResults[outputColumn] = searchResults[outputColumn].str.split('(\d+)').str[0] #Removes number from LSOA name so that areas merge into one
        print(searchResults[outputColumn].value_counts())
        fig, ax = plt.subplots()
        ax.bar(searchResults[outputColumn].value_counts().index, searchResults[outputColumn].value_counts()) #outputs bar graph with only present values 
        ax.set_title(searchQuery+" Crime Rates")
        plt.xticks(rotation = 90) #Rotate graph labels
        plt.show() #Show graph
    choice = input("Would you like to search again (y/n): ").upper() #Converts input to uppercase so that lowercase can be accepted
    return choice #Return user choice for original function to handle

while menu: #Menu loop
    print("Merseyside Crime Rates Database")
    print("1. View entire database\n2. Search by crime type\n3. Search by area\n4. Search by street\n5. Search by outcome\n6. Crime types as graph\n7. Quit")
    choice = input()
    while choice not in ["1", "2", "3", "4", "5", "6", "7"]: #If the entered number is not in the list of options
            choice = input("Invalid choice.  Choose menu option (1-7): ") #Validation for choice between 1-7
    if choice == "1":
        print(data) #Outputs all rows and columns using pandas
    elif choice == "2":
        #Search by crime
        SearchByCrime()
    elif choice == "3":
        #Search by area
        SearchByArea()
    elif choice == "4":
        #Search by street
        SearchByStreet()
    elif choice == "5":
        #Search by outcome
        SearchByOutcome()
    elif choice == "6":
         choice = input("Please enter which type of graph you wish to see:\n1.Graph of all crime in a single area\n2.Graph of amount of single crime in all areas\n3.Amount of each crime by specific outcome\n4.Outcome in a single area\n5 Crime by area in a line graph.")
         if choice == "1":
                #Crime types in area
                plotCrimeToAreaGraphs()
         elif choice == "2":
                #Areas with crime type
                areaTocrimeGraph()
         elif choice == "3":
                #Crime types with last outcome
                lastOutcomeToCrimeGraph()
         elif choice == "4":
                #Crime types with last outcome
                plotAreaToOutcomeGraph()
         elif choice == "5":
            #Crime by Area (Line graph)
            plotCrimeToAreaGraphLine()
    elif choice =='7':
        quit() #Quits program