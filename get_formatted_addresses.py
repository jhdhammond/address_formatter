import csv
import requests

rowArray = []

apiKey = input('Enter API key: ')

with open('raw_addresses.txt', newline='') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:

		countryShort = ''
		countryLong = ''
		administrative_area_level_1_short = ''
		administrative_area_level_2_short = ''
		administrative_area_level_1_long = ''
		administrative_area_level_2_long = ''
		postal_code = ''
		name = ''
		placeId = ''
		
		formatted_text = row[0].replace(' ', '%20')

		placeIdRequest = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=' + formatted_text + '&inputtype=textquery&fields=name,place_id&key=' + apiKey
		resp = requests.get(url=placeIdRequest)
		data = resp.json()
		try:
			name = data['candidates'][0]['name']
			placeId = data['candidates'][0]['place_id']

			try:
				detailsRequest = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + placeId + '&fields=address_component&key=' + apiKey
				resp1 = requests.get(url=detailsRequest)
				data1 = resp1.json()
				components = data1['result']['address_components']
				

				for x in components:
					if 'country' in x['types']:
						countryLong = x['long_name']
						countryShort = x['short_name']
					if 'postal_code' in x['types']:
						postal_code = x['long_name']
					if 'administrative_area_level_1' in x['types']:
						administrative_area_level_1_long = x['long_name']
						administrative_area_level_1_short = x['short_name']
					if 'administrative_area_level_2' in x['types']:
						administrative_area_level_2_long = x['long_name']
						administrative_area_level_2_short = x['short_name']				
			except:
				print('bummer')

		except:
			row.append('not found')
			row.append('not found')
		finally:
			row.append(name)
			row.append(placeId)
			row.append(countryShort)
			row.append(countryLong)
			row.append(administrative_area_level_1_short)
			row.append(administrative_area_level_1_long)
			row.append(administrative_area_level_2_short)
			row.append(administrative_area_level_2_long)
			row.append(postal_code)


		rowArray.append(row)



with open('employee_file.csv', mode='w') as employee_file:
	employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	employee_writer.writerow(['Original Address', 'Short Name', 'PlaceId', 'CountryCode', 'Country', 'admin area 1 short', 'admin area 1 long', 'admin area 2 short', 'admin area 2 long', 'postcode'])

	for row in rowArray:
		employee_writer.writerow(row)
    


