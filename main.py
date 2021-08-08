from GPSPhoto import gpsphoto
from geopy.geocoders import Nominatim
from os import walk

# initialize Nominatim API
geoLocator = Nominatim(user_agent="testApp")

loop = 'Y'
restart = 'Y'
count_pictureNotLocalized = 0
error = 0

while restart == 'Y':
    loop = 'Y'
    while loop == 'Y':
        count_pictureNotLocalized = 0
        count_pictureLocalized = 0
        error = 0
        originCityFound = set()
        last_latitude = -100
        last_longitude = -100
        inputFolder = input("Enter the input folder : E:/theod media/images/Bilder/")
        inputFolder = "E:/theod media/images/Bilder/%s" % inputFolder
        for root, dirs, files in walk("%s" % inputFolder):
            for file in files:
                if not file.endswith(".mp4"):
                    try:
                        data = gpsphoto.getGPSData("%s/%s" % (inputFolder, file))
                        if data is not None:
                            if 'Latitude' in data:
                                if data['Latitude'] is None:
                                    count_pictureNotLocalized = count_pictureNotLocalized + 1
                                else:
                                    # print("%s , %s" % (data['Latitude'], data['Longitude']))
                                    count_pictureLocalized = count_pictureLocalized + 1
                                    if abs(last_latitude - data['Latitude']) > 0.1 or abs(
                                            last_longitude - data['Longitude']) > 0.1:
                                        last_latitude = data['Latitude']
                                        last_longitude = data['Longitude']
                                        location = geoLocator.reverse("%s , %s" % (data['Latitude'], data['Longitude']))
                                        address = location.raw['address']
                                        city = address.get('city', '')
                                        state = address.get('state', '')
                                        country = address.get('country', '')
                                        code = address.get('country_code')
                                        zipcode = address.get('postcode')

                                        originCityFound.add(zipcode)

                                        location = geoLocator.geocode(zipcode)
                                        print("%s :  zip code %s (%s, %s) : %s  (%s, %s): %s %s %s" % (file, city,
                                                                                                       location.latitude,
                                                                                                       location.longitude,
                                                                                                       zipcode,
                                                                                                       data['Latitude'],
                                                                                                       data[
                                                                                                           'Longitude'],
                                                                                                       country, state,
                                                                                                       city))
                            else:
                                count_pictureNotLocalized = count_pictureNotLocalized + 1
                        else:
                            count_pictureNotLocalized = count_pictureNotLocalized + 1
                    except ValueError:
                        error = error + 1

                else:
                    print("File of mp4 type cannot be handled")

        print(
            "operation done with %s localisation found and %s not found" % (
                count_pictureLocalized, count_pictureNotLocalized))
        loop = input("Do you want to select another folder ? (Y/N)")

    print("Which city do you want to choose as location for your picture ?")
    print("originCityFound")
    coordinateOrCodePostal = input("Do you want to enter coordinate(C) or code postal(Z): ")
    if coordinateOrCodePostal == 'Z':
        code_postal_chosen = input("Enter the city code you want for your picture : ")
        location = geoLocator.geocode(code_postal_chosen)
        info = gpsphoto.GPSInfo((location.latitude, location.longitude))
    else:
        latitude = input("Enter the latitude for your picture : ")
        longitude = input("Enter the longitude for your picture : ")
        info = gpsphoto.GPSInfo((float(latitude), float(longitude)))

    SameFolder = input("Output same as input ? (Y/N):")
    if SameFolder == 'Y':
        outputFolder = inputFolder
    else:
        outputFolder = input("Enter the output folder ( C:/Users/theod/Downloads/Test ) :")

    for root, dirs, files in walk("%s" % inputFolder):
        for file in files:
            if not file.endswith(".mp4"):
                try:
                    data = gpsphoto.getGPSData("%s/%s" % (inputFolder, file))
                    picture = gpsphoto.GPSPhoto("%s/%s" % (inputFolder, file))
                    if data is not None:
                        if 'Latitude' in data:
                            if data['Latitude'] is None:
                                print("coord added :%s" % count_pictureNotLocalized)
                                count_pictureNotLocalized = count_pictureNotLocalized - 1
                                try:
                                    picture.modGPSData(info, '%s/%s' % (outputFolder, file))
                                except ValueError:
                                    error = error + 1
                            else:
                                print("Do nothing")
                        else:
                            print("coord added :%s" % count_pictureNotLocalized)
                            count_pictureNotLocalized = count_pictureNotLocalized - 1
                            picture.modGPSData(info, '%s/%s' % (outputFolder, file))
                    else:
                        print("coord added :%s" % count_pictureNotLocalized)
                        count_pictureNotLocalized = count_pictureNotLocalized - 1
                        picture.modGPSData(info, '%s/%s' % (outputFolder, file))
                except ValueError:
                    error = error + 1
            else:
                print("File of mp4 type cannot be handled")

    restart = input("operation done with %s errors. Do you want to select another folder ? (Y/N)" % error)
