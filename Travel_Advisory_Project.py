from pip._vendor import requests   #imports the requests library


#creation of a class called tripInformation
class tripInformation:

#creation of an init method that accepts user input as a parameter
#if no input is passed as a parameter, then user is asked for input
    
  def __init__(self, userInput=''):
      self.userInput = userInput if userInput else input('Enter the name of the country you wish to travel to: ')

  #api call for countries, to get information from the rest country api

  def getGeneralInfo(self):
    formatCountryName = self.userInput.replace(' ', '%20')   #addes %20 into the endpoint url to replace spaces
    countryUrl = 'https://restcountries.com/v3.1/name/{name}'.format(name = formatCountryName) #endpoint
    response = requests.get(countryUrl) #making a call to the api
    checkConnection = response.status_code  #gets the status code and stores it to a variable
    if checkConnection != 200:
      print('error!, country name is invalid or spelled incorrectly, check again') # Print error message if the request failed
    else:
      countryData = response.json() # Retrieve country data if the request was successful
      with open('countries.txt', 'w') as file: # Open a text file to write the country information
        file.write('These are some of the basic facts on the country:'+'\n'+ '\n'+ '\n') # write header
        #Iterate through each country in the response data
        for i in countryData:
          file.write('Name: ' + str(i.get('name')) + '\n') # Write the country's name to the file and creates a new line
          file.write('Capital: ' + str(i.get('capital')) + '\n') #Write the country's capital to the file
          file.write('Languages: ' + str(i.get('languages')) + '\n') # Write the country's languages to the file
          file.write('Currencies: ' + str(i.get('currencies')) + '\n') # Write the country's currencies to the file
          file.write('Alt Spellings: ' + str(i.get('altSpellings')) + '\n\n') # Write the country's alternative spellings to the file and creates two new lines in the file
  
  
  

    #api for getting latest news from countries
    #api key is the same for all free calls
    
    
  def getNewsInfo(self):
      # Build the URL for the news API using the provided API key and user input (country)
      newsUrl ='https://newsapi.org/v2/top-headlines?q={country}&apiKey=insertAPIKey'.format(country = self.userInput) #endpoint

      response = requests.get(newsUrl)

      checkConnection= response.status_code
      if checkConnection != 200:
        print('error! getting news information from the country')
      else:
        newsData = response.json()
        if newsData['articles'] == []: # Check if there are no articles for the selected country
          with open('countries.txt', 'a') as file:
            file.write('\n \n no top headlines today for this country! Try again later \n \n')
            
       # If there are articles, proceed to process and write them to the 'countries.txt' file
        else:  
           with open('countries.txt', 'a') as file:  # Open 'countries.txt' file in append mode
             articles = newsData.get('articles', [])  # Retrieve the list of articles from the JSON data
             file.write('these are the top headlines on the country of choice today:'+'\n'+ '\n'+ '\n')
             for article in articles:
                # Writes the following to the list of articles
                 file.write(f"Title: {article['title']}\n")
                 file.write(f"Author: {article['author']}\n")
                 file.write(f"Description: {article['description']}\n")
                 file.write(f"Published At: {article['publishedAt']}\n")
                 file.write(f"URL: {article['url']}\n")
                 file.write(f"URL to Image: {article['urlToImage']}\n")
                 file.write(f"Content: {article['content']}\n\n")
            #api call to obtain weather information on the country selected above
  def getWeatherInfo(self):
      api_key = ''
      
      endpoint = 'http://api.openweathermap.org/data/2.5/weather'
      payload = {
                'unit': 'metrics',
                'appid': api_key
            }
      payload['q'] = self.userInput
        
      response = requests.get(url= endpoint, params= payload)
     
      checkConnection= response.status_code
      if checkConnection != 200:
          print('error!, Country does not exist')
      else:
          weatherData=response.json()
          with open('countries.txt', 'a') as file:
              mainInfo = weatherData.get('main', {})
              file.write('This is the weather forecast for today in the country:'+'\n'+ '\n'+ '\n')
                
              for key, value in mainInfo.items():
                  file.write(f"{key}: {value}\n")
        
                # Extract the 'weather' information from the 'weatherData' dictionary
              weatherInfo = weatherData.get('weather', [])
              file.write('\nAdditional Weather Information about the weather:'+'\n'+ '\n'+ '\n')
                            
              for info in weatherInfo:
                  for key, value in info.items():
                      file.write(f"{key}: {value}\n")
        
# Create an instance of the 'tripInformation' class
trip = tripInformation()
        
# Call methods to gather general, news, and weather information for the trip
trip.getGeneralInfo()
trip.getNewsInfo()
trip.getWeatherInfo()
