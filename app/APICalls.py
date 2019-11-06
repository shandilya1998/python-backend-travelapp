from app.key import API_key
import requests
import copy
import random
import time
import json

class APICalls():
    def call_places_text_api_(self,
                             query = None,
                             location = None,
                             radius = None,
                             next_page_token = None):
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        if next_page_token and not query:
            search_payload = {"key": API_key, "pagetoken": next_page_token}
        elif next_page_token and query:
            raise TypeError('"query" and "next_page_token" must not be passed together')
        else:
            search_payload = {"key": API_key, "query": query}
        if location and radius:
            search_payload["location"] = location
            search_payload["radius"] = radius
        response = requests.get(url, search_payload)
        data = response.json()
        print(data['status'])
        while(True):
            if data['status'] == 'OVER_QUERY_LIMIT':
                time.sleep(random.randint(50,120))
                response = requests.get(url, search_payload)
                data = response.json()
                print(data['status'])
            elif not data['results']:
                break
            else:
                break
        if 'next_page_token' in data.keys():
            return (data, data['next_page_token'])
        else:
            return (data, None)

    def call_places_text_api(self,
                             query = None,
                             location = None,
                             radius = None):
        next_page_token = None
        data_parsed = {}
        while(True):
            data, next_page_token = self.call_places_text_api_(query = query,
                                                               next_page_token = next_page_token,
                                                               location = location,
                                                               radius = radius)
            data = self.parse_json(data)
            data_parsed.update(copy.deepcopy(data))
            query = None
            time.sleep(random.randint(10,70))
            if not next_page_token:
                break
        return data_parsed

    def parse_json(self,
                   data):
        data_parsed = {}
        results = data['results']
        for result in results:
            if 'permanently_closed' in result.keys():
                continue
            place_info = {}
            place_id = result['place_id']
            place_info['name'] = copy.deepcopy(result['name'])
#            place_info['address'] = copy.deepcopy(result['formatted_address'])
#            place_info['latitude'] = copy.deepcopy(result['geometry']['location']['lat'])
#            place_info['longitude'] = copy.deepcopy(result['geometry']['location']['lng'])
            data_parsed[place_id] = copy.deepcopy(place_info)
        return data_parsed

    def call_places_details_api(self,
                                place_id,
                                fields = None): # do not pass fields before changing the code
        url = 'https://maps.googleapis.com/maps/api/place/details/json'
        search_payload = {}
        if not fields:
            search_payload = {"key": API_key,"fields": "photos,rating,reviews,url,website,opening_hours,formatted_phone_number","place_id": place_id}
        #else:
            #search_payload = {"key": API_key,
                             # "fields": fields,
                              #"place_id": place_id}
        data = requests.get(url, params=search_payload)
        data = data.json()
        while (True):
            if data['status'] == 'OVER_QUERY_LIMIT':
                time.sleep(random.randint(10,70))
                response = requests.get(url, search_payload)
                data = response.json()
                print(data['status'])
            else:
                break
        result = data['result']
        data_ = {}
        try:
            data_['photos'] = json.dumps(result['photos'])
        except KeyError:
            print('photos missing in response')
            data_['photos'] = None
        try:
            data_['formatted_phone_number'] = result['formatted_phone_number']
        except KeyError:
            print('phone number missing in response')
            data_['formatted_phone_number'] = None
        try:
            data_['rating'] = result['rating']
        except KeyError:
            print('rating missing in response')
            data_['rating'] = None
        try:
            review_ = {}
            for index,review in enumerate(result['reviews']):
                review_[index] = review
            data_['reviews'] = json.dumps(review_)
        except KeyError:
            print('reviews missing in respone')
            data_['reviews'] = None
        try:
            data_['website'] = result['website']
        except KeyError:
            print('website missing in response')
            data_['website'] = None
        try:
            data_['opening_hours'] = json.dumps(result['opening_hours'])
        except KeyError:
            print('opening_hours missing in response')
            data_['opening_hours'] = None
            data_['url'] = result['url']
        time.sleep(random.randint(50,120))
        return data_
    
    def call_places_photo_api(photoreference, maxwidth):
        url = 'https://maps.googleapis.com/maps/api/place/photo'
        search_payload = {'key' : API_key, 
                          'photoreference' : photoreference, 
                          'maxwidth' : maxwidth}
        response = requests.get(url, search_payload)
        return response
        
        
    

#ob = APICalls()
#data_ = ob.call_places_text_api('museums in new york city')
#print(data_)









data = {'html_attributions': [],
        'next_page_token': 'CpQCAQEAACg-mnqUSbF7kGSwlGTjTA-TqQ60CMl9upXu4SLKo-KUgqSIBlWXsVDlC2jgOO_eWOslbZpD9dcwSux36sGVTfeKL8UbTBAc8uC3yCt_XoqoueXPs4Y39_H6ZNUA0GyQxmMjNoxiZK865f7wtnQpJtYgB1O1iBMDnUNXqLcblwHWcPgv1qhGf1Uvi6pxMri3iqxY4PBq6Ch_IuK_qqe292vwh81YwwMzgGUcMECagkSD5Mchc2um0EpybqZ9nftDv8DY53a085K_jF5oYeXbQE3Lo3cZKP-7EwumYKEATuUwoHgWG5-opIVmYqNMDy_yIzwLcFYKO_9wTshypkql6HO2eWLeiEY38pPrIRIzkp_UEhDcBx58pZQ6WJ7Qf5bLFf7-GhS6mKlWPQJcP94EoMdlbtq8-keu6A',
        'results': [{'formatted_address': '337 W 36th St, New York, NY 10018, USA',
                     'geometry': {'location': {'lat': 40.7543486,
                                               'lng': -73.993907},
                                  'viewport': {'northeast': {'lat': 40.75558702989272,
                                                             'lng': -73.99263912010727},
                                               'southwest': {'lat': 40.75288737010727,
                                                             'lng': -73.9953387798927}}},
                     'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                     'id': '2dc83236faeb2afd7f226ca467111a2439ed428a',
                     'name': 'Staypineapple, An Artful Hotel, Midtown New York',
                     'photos': [{'height': 1992,
                                 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">A Google User</a>'],
                                 'photo_reference': 'CmRaAAAAvGV8XlpsI_e59n5Zd8cBb3TPFefvsajoJaJtpjooPU9rsAuUF85eYctSR5s8Sbnvt7enaQLv_N20JXDHH77bI9QUu9LL7aRPD6O47OQXei6wpxNDMSwk1ITEFTkHPLSBEhAABwTuTPPRLYjGAjHaAUR5GhRWJUStVAFAVHmCCFuFKPX3tUfJQQ',
                                 'width': 5087}],
                     'place_id': 'ChIJq6oOd61ZwokRYLmMUZxbrFg',
                     'plus_code': {'compound_code': 'Q234+PC New York, USA',
                                   'global_code': '87G8Q234+PC'},
                     'rating': 4.5,
                     'reference': 'ChIJq6oOd61ZwokRYLmMUZxbrFg',
                     'types': ['lodging',
                               'point_of_interest',
                               'establishment'],
                     'user_ratings_total': 49},
                    {'formatted_address': '221 E 44th St, New York, NY 10017, USA',
                     'geometry': {'location': {'lat': 40.7518354,
                                               'lng': -73.9723757},
                                  'viewport': {'northeast': {'lat': 40.75308647989271,
                                                             'lng': -73.97108677010728},
                                               'southwest': {'lat': 40.75038682010727,
                                                             'lng': -73.97378642989273}}},
                     'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                     'id': '5a48f9b8f78962e31397314fe0f56a564abf108a',
                     'name': 'EVEN Hotel New York - Midtown East',
                     'opening_hours': {'open_now': True},
                     'photos': [{'height': 2671,
                                 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/112283332958060867517/photos">A Google User</a>'],
                                 'photo_reference': 'CmRaAAAA5Zd14i0itxHiOQvZFB61VKsOKXFYMZNVKHeRAVKl3tgRdDbhPUGw_ZSM7I9MwHPuzxpJPSjIcpUrPPgJ_NXBtp-yFeYmJk25FuK34rOquGzfDFd9yart0p96iabxFPsNEhBkXJk3z822PttAttvR7HBuGhSB0_NdS--3TfPtH73Y6xB575cFVQ',
                                 'width': 4000}],
                     'place_id': 'ChIJxWdiwwJZwokRWbr59FIxWhU',
                     'plus_code': {'compound_code': 'Q22H+P2 New York, USA',
                                   'global_code': '87G8Q22H+P2'},
                     'rating': 4.4, 'reference': 'ChIJxWdiwwJZwokRWbr59FIxWhU',
                     'types': ['spa',
                               'lodging',
                               'point_of_interest',
                               'establishment'],
                     'user_ratings_total': 779},
                    {'formatted_address': '60 E 54th St, New York, NY 10022, USA',
                     'geometry': {'location': {'lat': 40.7599065,
                                               'lng': -73.9732006},
                                  'viewport': {'northeast': {'lat': 40.76134012989272,
                                                             'lng': -73.97178827010728},
                                               'southwest': {'lat': 40.75864047010728,
                                                             'lng': -73.97448792989273}}},
                     'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                     'id': 'b39c645711bc5e45762067149a8a7769a1268625',
                     'name': 'Hotel Elysee by Library Hotel Collection',
                     'opening_hours': {'open_now': True},
                     'photos': [{'height': 1366,
                                 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/104135074538139664474/photos">Hotel Elysee by Library Hotel Collection</a>'],
                                 'photo_reference': 'CmRaAAAAzEF7e2Dk9G5KcXs36MYxo4hguO_i-hG_zCWf8oqre5xAMtSjGQXtIV-dMjJ76GrinPJxh_Ncqq2_39_LtvJakuLVpd0dAzmglinKfKryKO8bhFEqOR9mu57G71hDzgn-EhBy2UYK1_LcAO3nH9yVTcqDGhR4PyVtC16Cf-YXxAkCAfb0fHg5FA',
                                 'width': 2048}], 'place_id': 'ChIJPyNgE_tYwokRI5vRxa_eSTs',
                     'plus_code': {'compound_code': 'Q25G+XP New York, USA',
                                   'global_code': '87G8Q25G+XP'},
                     'rating': 4.6,
                     'reference': 'ChIJPyNgE_tYwokRI5vRxa_eSTs',
                     'types': ['lodging',
                               'point_of_interest',
                               'establishment'],
                     'user_ratings_total': 188},
                    {'formatted_address': '226 W 52nd St, New York, NY 10019, USA',
                     'geometry': {'location': {'lat': 40.762738,
                                               'lng': -73.983656},
                                  'viewport': {'northeast': {'lat': 40.76415822989272,
                                                             'lng': -73.98228777010728},
                                               'southwest': {'lat': 40.76145857010727,
                                                             'lng': -73.98498742989271}}},
                     'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                     'id': '7fdda201dfd5b451e92cc0dda3e79fbec26975a0',
                     'name': 'Novotel New York Times Square',
                     'opening_hours': {'open_now': True},
                     'photos': [{'height': 1367,
                                 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/113335589562963828073/photos">Novotel New York Times Square</a>'],
                                 'photo_reference': 'CmRaAAAArx_u9AKRA5mox4wH-jali654J5C1THW5y1I4HlXqav4sHc3XxQ7ZLJYKEPfTXZO9ubAu0iqr5JUA2O1nevhsAXpGS4-Fa9tCipat79PEquCutuJqwY9AzSisaE9msjUOEhBXB-AQJQhoYJCgl02yyudZGhRU-3YS4J9JB0UttRXbAlNdlbIYPg',
                                 'width': 2048}],
                     'place_id': 'ChIJr9cp0ldYwokRxolUb1zQPzE',
                     'plus_code': {'compound_code': 'Q278+3G New York, USA',
                                   'global_code': '87G8Q278+3G'},
                     'rating': 4.3,
                     'reference': 'ChIJr9cp0ldYwokRxolUb1zQPzE',
                     'types': ['lodging',
                               'point_of_interest',
                               'establishment'],
                     'user_ratings_total': 2827},
                    {'formatted_address': '371 7th Ave, New York, NY 10001, USA',
                     'geometry': {'location': {'lat': 40.7487055,
                                               'lng': -73.9916558},
                                  'viewport': {'northeast': {'lat': 40.75014892989272,
                                                             'lng': -73.99023957010728},
                                               'southwest': {'lat': 40.74744927010728,
                                                             'lng': -73.99293922989273}}},
                     'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                     'id': '66c68e431afcc549506940f69977b2bf5bf00126', 'name': 'Stewart Hotel New York',
                     'opening_hours': {'open_now': True},
                     'photos': [{'height': 3122,
                                 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/102161264584301355832/photos">Stewart Hotel New York</a>'],
                                 'photo_reference': 'CmRaAAAAG80cIIXtb47VrBMlFbRBTOcLbMkRmKlADvh4RpxVL7V9hjU6N0npgNlyKXLB_G0eTekbIuxAOrsSeSEFX5vFQT3DCp0Fx1z4jBt-fqjLz2NHq50kbTaQu0PaV4p6J_AgEhDoZeSAfa5_8pv3fh0CiP-qGhQK2E_gygIqf4VnKBbDfXSThQRNRg',
                                 'width': 5549}], 'place_id': 'ChIJE8nmAK9ZwokRt9a0QLhSUDE',
                     'plus_code': {'compound_code': 'P2X5+F8 New York, USA',
                                   'global_code': '87G8P2X5+F8'},
                     'rating': 3.9, 'reference': 'ChIJE8nmAK9ZwokRt9a0QLhSUDE',
                     'types': ['lodging',
                               'point_of_interest',
                               'establishment'],
                     'user_ratings_total': 1508},
                    {'formatted_address': '11 E 31st St, New York, NY 10016, USA',
                     'geometry': {'location': {'lat': 40.7463,
                                               'lng': -73.9849632},
                                  'viewport': {'northeast': {'lat': 40.74757907989272,
                                                             'lng': -73.98366422010727},
                                               'southwest': {'lat': 40.74487942010727,
                                                             'lng': -73.98636387989272}}},
                     'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                     'id': '824d533fe67d2437b7181943ac08108ee00930c0',
                     'name': 'Arlo NoMad',
                     'opening_hours': {'open_now': True},
                     'photos': [{'height': 3036,
                                 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/102213955618839347196/photos">A Google User</a>'],
                                 'photo_reference': 'CmRaAAAA0oh6QSSQ176hFIEnMOi76GHLZH-EPgSt7-UOlSZROJmv5JiKYxGVZjXEV7AAlUvPlywla-x9wWR7ZSAoX_EPuHD4GeIGHWQTCcjnokYU7kDeMNZ-JKKLNkmS1WlWhnblEhAwPWuW-Kc9spNt7rEZMqiCGhSCC5-qqTqWErpfewjpR8Wcr7essg',
                                 'width': 4048}],
                     'place_id': 'ChIJVTHBbqhZwokReeUu4-30qMg',
                     'plus_code': {'compound_code': 'P2W8+G2 New York, USA',
                                   'global_code': '87G8P2W8+G2'},
                     'rating': 4.4, 'reference': 'ChIJVTHBbqhZwokReeUu4-30qMg',
                     'types': ['lodging',
                               'point_of_interest',
                               'establishment'],
                     'user_ratings_total': 1019},
                    {'formatted_address': '29 E 29th St, New York, NY 10016, USA',
                     'geometry': {'location': {'lat': 40.74448,
                                               'lng': -73.98463},
                                  'viewport': {'northeast': {'lat': 40.74577612989271,
                                                             'lng': -73.98335762010728},
                                               'southwest': {'lat': 40.74307647010727,
                                                             'lng': -73.98605727989273}}},
                     'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                     'id': 'b968b21b859ece92e39aaf541e8fb2d7173e0884',
                     'name': 'The Redbury New York',
                     'opening_hours': {'open_now': True},
                     'photos': [{'height': 800,
                                  'html_attributions': ['<a href="https://maps.google.com/maps/contrib/116366181659378718714/photos">Martha Washington</a>'],
                                  'photo_reference': 'CmRaAAAABxpu7RmtaqC0t1bXThEKD4NxoQLOodH_RoQKk5aQGotkgBq-yGnQrpVxdJiwyKLg0nftOZSaz9ZpCbh2pLQrkaLE9g46NekNN30bjkoVSPMu7BKO4fjCSxd7meFoOsdfEhCq-I4clxBXNbo38pkjcqVaGhTZdqisqAKJ2nsJNTBsuPLM1sVLuA',
                                 'width': 1600}], 'place_id': 'ChIJW48HxKdZwokRJl80L3KXcYA',
                     'plus_code': {'compound_code': 'P2V8+Q4 New York, USA',
                                   'global_code': '87G8P2V8+Q4'},
                     'rating': 4.1, 'reference': 'ChIJW48HxKdZwokRJl80L3KXcYA',
                     'types': ['lodging', 'point_of_interest', 'establishment'],
                     'user_ratings_total': 954},
                    {'formatted_address': '44 W 29th St, New York, NY 10001, USA',
                     'geometry': {'location': {'lat': 40.74629350000001,
                                               'lng': -73.9896373},
                                  'viewport': {'northeast': {'lat': 40.74771552989272,
                                                             'lng': -73.98823452010727},
                                               'southwest': {'lat': 40.74501587010727,
                                                             'lng': -73.99093417989272}}},
                     'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                     'id': '54960ebdce34fde3f3b53f22e6ab1ce62bfd3c7a',
                     'name': 'MADE Hotel',
                     'opening_hours': {'open_now': True},
                     'photos': [{'height': 2001,
                                 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/103224200720047893350/photos">A Google User</a>'],
                                 'photo_reference': 'CmRaAAAABdoOIXOS5vLs0PeRsmX3mv3gMjkYBCC6p--VydOo9dXP6BoH_kWfsvXs8bm9IeqKtZe7mZLYIck3C_hyjBnbXq1I7yZSGua713-rAJUYqzDeq7n6psDz8NKfHsUjbYUNEhAErcrg4vJEupzsOzMqth2HGhRclo5c4P8u8MFCtWieyQH1YaIEqA',
                                 'width': 3000}], 'place_id': 'ChIJAQAsWK9ZwokRVNJ_cGoFFIE',
                     'plus_code': {'compound_code': 'P2W6+G4 New York, USA',
                                   'global_code': '87G8P2W6+G4'},
                     'rating': 4.4,
                     'reference': 'ChIJAQAsWK9ZwokRVNJ_cGoFFIE',
                     'types': ['lodging',
                               'point_of_interest',
                               'establishment'], 'user_ratings_total': 329},
                    {'formatted_address': '781 Prospect Pl, Brooklyn, NY 11216, USA',
                     'geometry': {'location': {'lat': 40.6743599, 'lng': -73.9507078},
                                  'viewport': {'northeast': {'lat': 40.67572697989272,
                                                             'lng': -73.94935647010728},
                                               'southwest': {'lat': 40.67302732010727,
                                                             'lng': -73.95205612989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': '64258d800c48adfadc1f1c94d1e87be22ba00c56', 'name': 'The Brooklyn Riviera Hostel', 'photos': [{'height': 3456, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109159326999556824821/photos">stefano antonio arcoleo</a>'], 'photo_reference': 'CmRaAAAAjQ-mKKe2Ceq0MA4yaOJbMM0MpuH9AuxN3qnvnHyg1ues6GSpDIFhECCkNbrpVvao6Q3xOHNM08NDHJR33DJu2gn_Oe-mwq8u6qL9DNt-Cpfv3-2GZn3Qc4ZeRQ442HuDEhDqkw-iFqsy2JJXvn9pv5NTGhRVYe7lkkPuHpXwPnaHTZzgR3wG1A', 'width': 3456}], 'place_id': 'ChIJSxHTV5xbwokRNFanSov7jL8', 'plus_code': {'compound_code': 'M2FX+PP New York, USA', 'global_code': '87G8M2FX+PP'}, 'rating': 4.1, 'reference': 'ChIJSxHTV5xbwokRNFanSov7jL8', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 49}, {'formatted_address': '401 7th Ave, New York, NY 10001, USA', 'geometry': {'location': {'lat': 40.7497723, 'lng': -73.9906244}, 'viewport': {'northeast': {'lat': 40.75124772989273, 'lng': -73.98915617010728}, 'southwest': {'lat': 40.74854807010728, 'lng': -73.99185582989273}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': '6be005e9fd8d964521cf491c570ad709b2b5d97c', 'name': 'Hotel Pennsylvania', 'opening_hours': {'open_now': True}, 'photos': [{'height': 831, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/112194499307933867865/photos">Hotel Pennsylvania</a>'], 'photo_reference': 'CmRaAAAAfdTztIyg_heahBfEVw_Z-RoisNXbNZmqimZox5HnME580YID02CfWOKZEz_59OMVizYdmLK7MaotNrkAW9t7aF5HvvuO737jIgBnKhMVohZqWyQPQRGCMhso58Exm5kXEhBSUIxVav_N6wZOfM-uWM8NGhT_u28XVXtaec0jumSt2lCbgUHL2A', 'width': 1252}], 'place_id': 'ChIJWbSN8q5ZwokRpLN00upxy8g', 'plus_code': {'compound_code': 'P2X5+WQ New York, USA', 'global_code': '87G8P2X5+WQ'}, 'rating': 2.7, 'reference': 'ChIJWbSN8q5ZwokRpLN00upxy8g', 'types': ['political', 'lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 14239}, {'formatted_address': '515 9th Ave, New York, NY 10018, USA', 'geometry': {'location': {'lat': 40.7565546, 'lng': -73.9943253}, 'viewport': {'northeast': {'lat': 40.75769387989272, 'lng': -73.99289157010728}, 'southwest': {'lat': 40.75499422010728, 'lng': -73.99559122989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': 'f8dcea10bfc45c7ac444dc12dc173b540cd7875f', 'name': 'Cassa Times Square', 'opening_hours': {'open_now': True}, 'photos': [{'height': 3708, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/110257704151452855601/photos">A Google User</a>'], 'photo_reference': 'CmRaAAAAynmiifNxm8IBNGz6ZgBTdsKzTM0dNrnIElBjHOHu-UBkS9gVkNVyZPxzqPH34qcx0wN-x9bTLwTAFVU5XQr4i3PkVJEc8R1pSDfNDEK5sUBXtPISyO1FruI9dJLDA4BtEhDa2Hg7RRVbVUtj7cHSg9v2GhQ87AOTTQH8_jH3WpbDVqqS-YXdAQ', 'width': 5414}], 'place_id': 'ChIJG5BtVK1ZwokR9mHk8UmezSE', 'plus_code': {'compound_code': 'Q244+J7 New York, USA', 'global_code': '87G8Q244+J7'}, 'rating': 4.1, 'reference': 'ChIJG5BtVK1ZwokR9mHk8UmezSE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 570}, {'formatted_address': '317 W 14th St, New York, NY 10014, USA', 'geometry': {'location': {'lat': 40.74029180000001, 'lng': -74.0034123}, 'viewport': {'northeast': {'lat': 40.74157947989272, 'lng': -74.00210692010728}, 'southwest': {'lat': 40.73887982010728, 'lng': -74.00480657989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': '3b4ce24dba31bc2f1a638bbba07b45c376447362', 'name': 'Chelsea Pines Inn', 'photos': [{'height': 2240, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/112587334528157008579/photos">Grzegorz Juraszek</a>'], 'photo_reference': 'CmRaAAAAobCnWCVIkk33oPc6UL81QFLZLHkxd8Bqe4Bd1YzfNDdFvAGnbCgTZo_p1LOZZf9HSE6Ik1ZLyLoaOljncaCdNUUWCYDJkqFedg3pOozTB3N1g7ZKAwyUEazW7-anHJLtEhCJn570IcuJHgYko8ycbIxqGhSWwV8gR1efcaneLa0YmddPblNzeQ', 'width': 4000}], 'place_id': 'ChIJnYYGU75ZwokRFQBV3A_Jlnk', 'plus_code': {'compound_code': 'PXRW+4J New York, USA', 'global_code': '87G7PXRW+4J'}, 'rating': 4.3, 'reference': 'ChIJnYYGU75ZwokRFQBV3A_Jlnk', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 161}, {'formatted_address': '234 W 42nd St, New York, NY 10036, USA', 'geometry': {'location': {'lat': 40.7565671, 'lng': -73.98876790000001}, 'viewport': {'northeast': {'lat': 40.75801167989272, 'lng': -73.98734772010728}, 'southwest': {'lat': 40.75531202010728, 'lng': -73.99004737989273}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': '44501036c6abb0529221482fb722affb1af723c7', 'name': 'Hilton Times Square', 'opening_hours': {'open_now': True}, 'photos': [{'height': 596, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/101502062173947730432/photos">Hilton Times Square</a>'], 'photo_reference': 'CmRZAAAAQSH8FAKg-YNlGo3JSYdcrzdtldiiM5o1DWEB2NFbLj0C5ybS372xeS2C9qMiwc98tHDu5-G-znLL0uj0tG0UAswnvA9R20XnbRcAgxDDYldvj748UYqhzi3nBmb4O0JnEhAFb6H-fUmMUzeu5F5ImUAwGhQJtRWBo9aG6THGzlS3wB4vltPTHw', 'width': 1053}], 'place_id': 'ChIJ7yGup1RYwokRnGBh8EluQWs', 'plus_code': {'compound_code': 'Q246+JF New York, USA', 'global_code': '87G8Q246+JF'}, 'rating': 4.3, 'reference': 'ChIJ7yGup1RYwokRnGBh8EluQWs', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 2900}, {'formatted_address': '455 Madison Ave, New York, NY 10022, USA', 'geometry': {'location': {'lat': 40.75801999999999, 'lng': -73.9749775}, 'viewport': {'northeast': {'lat': 40.75930542989272, 'lng': -73.97367412010728}, 'southwest': {'lat': 40.75660577010727, 'lng': -73.97637377989273}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': '6f58d9b4a4f4148ec3ae34f5fcbf609c53de78d7', 'name': 'Lotte New York Palace', 'opening_hours': {'open_now': True}, 'photos': [{'height': 2969, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/107617744778595205558/photos">John Raudat</a>'], 'photo_reference': 'CmRaAAAA6h2H1uRcOqGaouBBBjOdVb_UKKnm_MUeW3aMDnwCbioV0BcQzyUXOuVel0WScIJgfEM3UepeIyhC9rXN54T_PbgHUcKxOeyMwdzCQHIlLt_IsNKAvEhy8YcsB-aJ_K8qEhD04Kkf6sDMUjun_PGAF6U3GhSKuqwbruWbW1sxIPDMUqgcEbQiew', 'width': 3968}], 'place_id': 'ChIJu6kY43RawokRnmczCmSH-_s', 'plus_code': {'compound_code': 'Q25G+62 New York, USA', 'global_code': '87G8Q25G+62'}, 'rating': 4.5, 'reference': 'ChIJu6kY43RawokRnmczCmSH-_s', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 2171}, {'formatted_address': '151 E Houston St, New York, NY 10002, USA', 'geometry': {'location': {'lat': 40.72292100000001, 'lng': -73.989362}, 'viewport': {'northeast': {'lat': 40.72434597989272, 'lng': -73.98797912010728}, 'southwest': {'lat': 40.72164632010728, 'lng': -73.99067877989273}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': '6c8570c4a1fef73994aeebf72d37b7d1848eabd1', 'name': 'The Ridge Hotel', 'opening_hours': {'open_now': True}, 'photos': [{'height': 1080, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/104504186944343174974/photos">A Google User</a>'], 'photo_reference': 'CmRaAAAAkqjtJLXNuoDgcL2TtYukWoPjkjn4jwCTqa5m2FbvmJ0DykUPO15onhG1LEMmWXbeo3AwdTQwh0XRZvPOp5BKm2z5xZwi-EDwfE2_IvcImrjqgTMe_sWYGHjt3jrGysQxEhABXO15bFJws9Uq9MmFIz5IGhRwazuPQRcqB91UaQofZveO3JruVg', 'width': 1080}], 'place_id': 'ChIJ81Hnc4RZwokRfWWztzfiGu0', 'plus_code': {'compound_code': 'P2F6+57 New York, USA', 'global_code': '87G8P2F6+57'}, 'rating': 4.1, 'reference': 'ChIJ81Hnc4RZwokRfWWztzfiGu0', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 247}, {'formatted_address': '30 W 46th St, New York, NY 10036, USA', 'geometry': {'location': {'lat': 40.756437, 'lng': -73.9806461}, 'viewport': {'northeast': {'lat': 40.75789442989272, 'lng': -73.97921767010727}, 'southwest': {'lat': 40.75519477010728, 'lng': -73.98191732989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': '7f0b96df6db029e76e986b8d9e8e8191171a0391', 'name': 'Cambria Hotel New York - Times Square', 'opening_hours': {'open_now': True}, 'photos': [{'height': 1192, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/104814869727120140955/photos">CAMBRiA hotel &amp; suites New York Times Square</a>'], 'photo_reference': 'CmRaAAAAkSjUcYysjOMuw8SWAKDLXCAdrb9_mKEq44_7RKXRobpHWYJu4RGRozXDCuppgdNnyKT11KDUqn4u8G4GHd4IHN1rJOS1BVhLMSpoKVwlvNHULj1FfgfcdAwgyNgaBHcxEhCdXr3BpGwaoE9VgJJpM53lGhSqgjO54WxUdvZJfM4XQcfHLD4aPg', 'width': 2119}], 'place_id': 'ChIJuUJUsP9YwokRwZudos--ChE', 'plus_code': {'compound_code': 'Q249+HP New York, USA', 'global_code': '87G8Q249+HP'}, 'rating': 4.3, 'reference': 'ChIJuUJUsP9YwokRwZudos--ChE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 909}, {'formatted_address': '321 W 35th St, New York, NY 10001, USA', 'geometry': {'location': {'lat': 40.7534672, 'lng': -73.9938981}, 'viewport': {'northeast': {'lat': 40.75473682989272, 'lng': -73.99262297010728}, 'southwest': {'lat': 40.75203717010728, 'lng': -73.99532262989271}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': 'a49afae293e42b256c92fd74be55464dbcc957cf', 'name': 'EVEN Hotel New York - Times Square South', 'opening_hours': {'open_now': True}, 'photos': [{'height': 2678, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/107381052293953026195/photos">Even Hotels New York - Times Square South</a>'], 'photo_reference': 'CmRaAAAAMt3azhSePxPzlPlKGyPAuz8nO0NfAUENrYAPWIi5dQTwAEEz_-6i_KP7jgJCj20m3cMeoig_DUw8A95sVjElvdldBqQbcepvT1ASlU1mMZQXgy0gw1AofW5P1lIpjCHHEhAIgB6NmNJXWlMsw6Lrg2RWGhSP_uY3J2-Kg2BxYEQtwb8XmocVCg', 'width': 4000}], 'place_id': 'ChIJs7KKkK1ZwokRr0u0PJsZNJ4', 'plus_code': {'compound_code': 'Q234+9C New York, USA', 'global_code': '87G8Q234+9C'}, 'rating': 4.6, 'reference': 'ChIJs7KKkK1ZwokRr0u0PJsZNJ4', 'types': ['spa', 'lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 790}, {'formatted_address': '224 W 49th St, New York, NY 10019, USA', 'geometry': {'location': {'lat': 40.7609782, 'lng': -73.9855103}, 'viewport': {'northeast': {'lat': 40.76241302989271, 'lng': -73.98407692010728}, 'southwest': {'lat': 40.75971337010727, 'lng': -73.98677657989273}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': 'a7160671eba571bfcb30c5d44174e519e252281f', 'name': 'The Time New York', 'opening_hours': {'open_now': True}, 'photos': [{'height': 654, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/112386577757083374643/photos">A Google User</a>'], 'photo_reference': 'CmRaAAAAgr55RykDlMCP7dhTczT3ga9SuruAkHCGJjbElVhJNWwCqV8GjgpCQ_pSmTcXxZVOuz-xD15ceEMPcmZWM3Cep81oJiTOL0g6x2fnJR3JcugDZEaT352a3-qdl73peZYLEhDslMreF6KkRzsYCCsxb4c5GhRY9OT2LGuvBRgR8o9KespNmljG1Q', 'width': 980}], 'place_id': 'ChIJGSNzZVZYwokRJWw6Ji1jta0', 'plus_code': {'compound_code': 'Q267+9Q New York, USA', 'global_code': '87G8Q267+9Q'}, 'rating': 4.1, 'reference': 'ChIJGSNzZVZYwokRJWw6Ji1jta0', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 618},
                    {'formatted_address': '305 W 46th St, New York, NY 10036, USA',
                     'geometry': {'location': {'lat': 40.7602404,
                                               'lng': -73.98845109999999},
                                  'viewport': {'northeast': {'lat': 40.76142042989272,
                                                             'lng': -73.98697062010729},
                                               'southwest': {'lat': 40.75872077010727,
                                                             'lng': -73.98967027989272}}},
                     'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                     'id': '3b022b23d5e59b9c104a70803b2fd37f6a44dca1',
                     'name': 'Hotel Riu Plaza New York Times Square',
                     'opening_hours': {'open_now': True},
                     'photos': [{'height': 1364,
                                 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/100489364747737267031/photos">Hotel Riu Plaza</a>'],
                                 'photo_reference': 'CmRaAAAAd8QfXhHrivsHVC5mXJfyIVrPY4DJ-P5VbYAvRAjmbKFbzrwYNYqAc4Jkmpe81ia0JTi76DWH2efW8w3BRabEA9WWdaq2xOUj-4YXjljHM2Z-NAYM1nic-EnNLEPqkWnbEhB1GmPBOO9t3r6L15XUAK6QGhQXCK1az8PRqdDR_C-QN1SLgjY2Pw',
                                 'width': 2048}], 'place_id': 'ChIJDwzsBVRYwokRvSHYftloJ1I',
                     'plus_code': {'compound_code': 'Q266+3J New York, USA',
                                   'global_code': '87G8Q266+3J'},
                     'rating': 4.4,
                     'reference': 'ChIJDwzsBVRYwokRvSHYftloJ1I',
                     'types': ['lodging',
                               'point_of_interest',
                               'establishment'],
                     'user_ratings_total': 3815},
                    {'formatted_address': '768 5th Ave, New York, NY 10019, USA', 'geometry': {'location': {'lat': 40.7644691, 'lng': -73.9744877}, 'viewport': {'northeast': {'lat': 40.76584697989271, 'lng': -73.97295707010728}, 'southwest': {'lat': 40.76314732010727, 'lng': -73.97565672989272}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png', 'id': '0a42d8834dd2ce588bb7aa6a11f2aad5669f3a1a', 'name': 'The Plaza', 'photos': [{'height': 773, 'html_attributions': ['<a href="https://maps.google.com/maps/contrib/118299923841167087445/photos">The Plaza</a>'], 'photo_reference': 'CmRaAAAA1aK4cXq4lH75U4EhX1KbSHIPYyHTs2jl64tE8nxinP18kMBQ0Zsnu5hPHgN9xDhDM3bNN0XL28yLHB9OdfbTie3KnUkVynZdLy_lnepj6k5DWM23h2_xb3Aq8A72eAxGEhCp7402Gvx4lghLMWfaoRWSGhQ2cykm-BlCrQgTs1qMpEHD0X-tOg', 'width': 773}], 'place_id': 'ChIJYaVdffBYwokRnTOoCzCq9mE', 'plus_code': {'compound_code': 'Q27G+Q6 New York, USA', 'global_code': '87G8Q27G+Q6'}, 'rating': 4.5, 'reference': 'ChIJYaVdffBYwokRnTOoCzCq9mE', 'types': ['lodging', 'point_of_interest', 'establishment'], 'user_ratings_total': 6621}], 'status': 'OK'}

data_places_details = {'html_attributions': [],
                       'result': {'address_components': [{'long_name': '337',
                                                          'short_name': '337',
                                                          'types': ['street_number']},
                                                         {'long_name': 'West 36th Street',
                                                          'short_name': 'W 36th St',
                                                          'types': ['route']},
                                                         {'long_name': 'Manhattan',
                                                          'short_name': 'Manhattan',
                                                          'types': ['sublocality_level_1',
                                                                    'sublocality',
                                                                    'political']},
                                                         {'long_name': 'New York',
                                                          'short_name': 'New York',
                                                          'types': ['locality',
                                                                    'political']},
                                                         {'long_name': 'New York County',
                                                          'short_name': 'New York County',
                                                          'types': ['administrative_area_level_2',
                                                                    'political']},
                                                         {'long_name': 'New York',
                                                          'short_name': 'NY',
                                                          'types': ['administrative_area_level_1',
                                                                    'political']},
                                                         {'long_name': 'United States',
                                                          'short_name': 'US',
                                                          'types': ['country',
                                                                    'political']},
                                                         {'long_name': '10018',
                                                          'short_name': '10018',
                                                          'types': ['postal_code']}],
                                  'adr_address': '<span class="street-address">337 W 36th St</span>, <span class="locality">New York</span>, <span class="region">NY</span> <span class="postal-code">10018</span>, <span class="country-name">USA</span>',
                                  'formatted_address': '337 W 36th St, New York, NY 10018, USA',
                                  'formatted_phone_number': '(866) 866-7977',
                                  'geometry': {'location': {'lat':
                                                                40.7543486,
                                                            'lng': -73.993907},
                                               'viewport': {'northeast': {'lat': 40.75558618029149,
                                                                          'lng': -73.99263996970848},
                                                            'southwest': {'lat': 40.7528882197085,
                                                                          'lng': -73.9953379302915}}},
                                  'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/lodging-71.png',
                                  'id': '2dc83236faeb2afd7f226ca467111a2439ed428a',
                                  'international_phone_number': '+1 866-866-7977',
                                  'name': 'Staypineapple, An Artful Hotel, Midtown New York',
                                  'photos': [{'height': 1992,
                                              'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'],
                                              'photo_reference': 'CmRaAAAAThQnnI1BpKSxM-sF2OszNcYdQZal-SGhhHDTohZwwQ0p89TcN3649dMh0WB-7BtunC1d9ywu3AxoZY5tg3VmWOjHFFjGXR1_8m0QQ-mMKoGxIeOfiqELc2p9NGsTA4kxEhAXFif_NkTMr6p_mZHWmjOgGhSw7YsQgz3X7VrKmJI1Rd_gDxVEBA',
                                              'width': 5087},
                                             {'height': 2333,
                                              'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'], 'photo_reference': 'CmRaAAAAecfLnB_Nvroocz_XmeSbt7MlWS8lq73kwZ-XzFxV2vKG3H24qTtefEfnQ9x8sBuPwD2RHecpSkZgVXY_iYNBQPAmnHcMnuJok5cpqNwCIgkAGQGMzOcKutn-khXN5rx6EhAIZcsr87Ks836-6_iRQn7pGhRt0cQPBcbcSwfY6BExTZhvGaQtQA',
                                              'width': 3500},
                                             {'height': 2333,
                                              'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'],
                                              'photo_reference': 'CmRaAAAA0IqMYIJ6vxyl0fJUqpVnbKi5V6igf-CFGhn06c0LBHMZ5kONalIGVNFtXDUBVwNoJKHYtH0XyUgoNW1cZozYmq1QLsqDWBvVW3pVPXX3-HxVMdezmz_to9QlwNR1RvqsEhCVVtTqrhFYpy8jhOSlRiMkGhQcE9-dR192HRzJ3ANs4cknh0tG2Q',
                                              'width': 3500},
                                             {'height': 3500,
                                              'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'],
                                              'photo_reference': 'CmRaAAAAztzsvlIa9AgbCS8qzzp4oxMGQfVEnS3-gIUzf_Y0lCoLxeM5mf4lfgkLgumt_EGMu4bfQByerapTBYGZChoXEL4TTKuq-bMueHQGgcGFn8s4Md7iagh2ptuY92EUuyqBEhBMLY6WsrzGHwIGr0yoi-gvGhQgJtHOxEy3T_vIjHvs8SEFLiIG3w',
                                              'width': 5250},
                                             {'height': 2333,
                                              'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'],
                                                               'photo_reference': 'CmRaAAAA9TRKwGLeu2VSvR01pTaKpRIbFQFuCcQIwzVnGWIOFGDNhrUTSuZgsqfLBwsla1Nv4-F5IJhC2vFvd12JVyDsxQ1dLhqS2cl6B4cw11_SWXNNmJ1AbQC-ftuLeHLKzN5_EhCJSolqLB69jHXgULCMMC4EGhQ4CwdMImXPpA_i8h3LLDCs5G_Aqw',
                                              'width': 3500},
                                             {'height': 3500,
                                              'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'],
                                              'photo_reference': 'CmRaAAAADP_chhgCOub-35xqa9UMOTtyvQs4yvLUS0yJVYDD-uCgYweRppZZ7CEBPWa5kd76Jx0tAMsdKcSDSwPt3AE55Kgj-DaYIvYh2zzq3rvSZc5NSfCO8BBZti2C8gym7NnfEhBruC3lr32sRBrwvj3BL8GNGhTp3afqPYQwihFdwly94mwR9oZuNw',
                                              'width': 5250},
                                             {'height': 2333,
                                              'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'],
                                              'photo_reference': 'CmRaAAAAhphzRW5GW89UiEXgTna4jpTYsjtA4fmPvyIefkoQp3GHeY7A06feUcofacTNK5xWllktjLEyuQPsxfcVqb1D2XHUyR1c7XJsqs072Bm3sZJUu_oQ0TcJaexO4DrGp6zUEhC0rnkAg-REFW2_kmKUemVkGhTFxONYostRwcftqHUO1o0pJWrmpw',
                                              'width': 3500},
                                             {'height': 3500,
                                              'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'],
                                              'photo_reference': 'CmRaAAAAGdlEvSSWaLLA72fQYoT8VpxKHmOxLz17Z0y_h7MUxAoo_AiBirrvuDDVQ4G3VM9Upm2adCEkpCXy6PoFBKcGvmWKaqGJh6iPEAiYqWRROnQldaiPCr2SGUqMJV3j9NOsEhBcYQXN0snAwmWUIVVKSEHhGhQOgT8uq66qgfDKEeRX4-0P0Yjh4Q',
                                              'width': 5250}, {'height': 3500,
                                                               'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'],
                                                               'photo_reference': 'CmRaAAAAIlorY_SwBe5-WphFyAprfkWoybh_ndLeGwkZyZ-5WBLbGh0w8DoPzxs4q0bJwshCfPZr7u4PhYjK7ZvKk5UEtCiROoeCfeYtbYyfqsE-geWEE3qNcc6ugHC5x50YobM2EhD1TO0l-KgAN-7inpPklF4UGhRjvV2wndD9SP1GraHGoHoFERTO5Q',
                                                               'width': 5250},
                                             {'height': 2333,
                                              'html_attributions': ['<a href="https://maps.google.com/maps/contrib/109772271407337854767/photos">Staypineapple, An Artful Hotel, Midtown New York</a>'],
                                              'photo_reference': 'CmRaAAAAmKAu-4yMODOCcfcplKialQrvdKVCuK89d9LKg5xB_pEl9_3W2ThB57ppLcy_qvv37PfNPipt3YkB-aV0hOAto-ihkEO2MR9uRnx3RK583gKfwCpAOMaqUYbjlOa2lfUqEhA_FMJ7cjV4pqgR_YrC0YPQGhTg_SqIKFm-d_DxMFjGkieIOuRsFQ',
                                              'width': 3500}],
                                  'place_id': 'ChIJq6oOd61ZwokRYLmMUZxbrFg',
                                  'plus_code': {'compound_code': 'Q234+PC New York, United States',
                                                'global_code': '87G8Q234+PC'},
                                  'rating': 4.5, 'reference':
                                      'ChIJq6oOd61ZwokRYLmMUZxbrFg',
                                  'reviews': [{'author_name': 'September Búho',
                                               'author_url': 'https://www.google.com/maps/contrib/109212276694726298473/reviews',
                                               'language': 'en',
                                               'profile_photo_url': 'https://lh5.googleusercontent.com/-WzSI37GMcxU/AAAAAAAAAAI/AAAAAAAAs04/X4UMO8DNh5o/s128-c0x00000000-cc-rp-mo-ba4/photo.jpg',
                                               'rating': 5,
                                               'relative_time_description': 'in the last week',
                                               'text': 'Room 2404 is beautiful! Beds and pillows amazingly comforting! Water pressure super hot water always. I was with my 13 yr old daughter she loved the place. Employees super nice and maintain everything under control during the Sat blackout!! Fun adventure! Also the hotel super clean everywhere.',
                                               'time': 1563211620},
                                              {'author_name': 'Dave Vandesype',
                                               'author_url': 'https://www.google.com/maps/contrib/102627616049242717189/reviews',
                                               'language': 'en',
                                               'profile_photo_url': 'https://lh4.googleusercontent.com/-fC7xYCwb-jE/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rftbB5tMwIoB6YyCtyT98GSvn_xxA/s128-c0x00000000-cc-rp-mo-ba3/photo.jpg',
                                               'rating': 4,
                                               'relative_time_description': '3 weeks ago',
                                               'text': 'Cozy, close to transit (Pennsylvania Station) and friendly staff. Tiny room filled by the comfortable bed but just sleeping there anyway. Same theme for bathroom, just big enough but all you need. Clean and works. Just what a pair of first timers to NYC needed.',
                                               'time': 1561659602},
                                              {'author_name': 'Marie DeLorenzo',
                                               'author_url': 'https://www.google.com/maps/contrib/115387964151205073822/reviews',
                                               'language': 'en',
                                               'profile_photo_url': 'https://lh6.googleusercontent.com/-K-rNKtg8KHI/AAAAAAAAAAI/AAAAAAAAAHE/zaENZ-OXyWY/s128-c0x00000000-cc-rp-mo/photo.jpg',
                                               'rating': 5,
                                               'relative_time_description': '3 months ago',
                                               'text': "Friendly staff and clean rooms. \nI stayed for a business trip and was very impressed. \nUpon arrival I was greeted warmly and was offered cupcakes.\nCheck in and check out were smooth and quick. I did have a minor wait at check in but it didn't take long before I was given my room key.  \nThe staff were all extremely courteous and warmly greeted you each and every time you walked through the door. \nThe rooms were modern and clean. They were small but perfect for a single person. Also this is to be expected in NYC so close to Penn MSG, Empire State Building, etc.\nThe bed and duvet were super comfortable and the voice activated concierge was convenient.  \nI would definitely stay again.",
                                               'time': 1555108846},
                                              {'author_name': 'Neha Mac',
                                               'author_url': 'https://www.google.com/maps/contrib/103185227233940305962/reviews',
                                               'language': 'en',
                                               'profile_photo_url': 'https://lh4.googleusercontent.com/-yjqc4F5mK2Q/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rcuACOOJg7c7ogZxMMOW3-0cfJT1w/s128-c0x00000000-cc-rp-mo-ba5/photo.jpg',
                                               'rating': 4,
                                               'relative_time_description': '3 months ago',
                                               'text': 'Great location and very clean hotel. The room is no frills but very cute. You’ll get what you need but not really more than that. The staff is very attentive, which was really helpful. I’d go back for business travel and stay here again.',
                                               'time': 1555366070},
                                              {'author_name': 'Ellen Peters',
                                               'author_url': 'https://www.google.com/maps/contrib/113347867729575887301/reviews',
                                               'language': 'en',
                                               'profile_photo_url': 'https://lh4.googleusercontent.com/-iHcU9ma6Yzc/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rc6_TTGG6qffwe3S6UlVwHxsrDP0Q/s128-c0x00000000-cc-rp-mo/photo.jpg',
                                               'rating': 5,
                                               'relative_time_description': '2 months ago',
                                               'text': 'The location was good, the decore was contemporary, and tastefully done.  Muffins in the a.m. cupcakes in the p.m. Beds were comfortable and the rooms were nice and clean.  The best part was the hospitable staff.  They couldn’t have been nicer and very helpful.',
                                               'time': 1556503366}],
                                  'scope': 'GOOGLE',
                                  'types': ['lodging',
                                            'point_of_interest',
                                            'establishment'],
                                  'url': 'https://maps.google.com/?cid=6389582698273093984',
                                  'user_ratings_total': 49,
                                  'utc_offset': -240,
                                  'vicinity': '337 West 36th Street, New York',
                                  'website': 'https://www.staypineapple.com/midtown-new-york?utm_source=google-my-business&utm_medium=organic&utm_campaign=GMB&utm_term=tany'},
                       'status': 'OK'}

