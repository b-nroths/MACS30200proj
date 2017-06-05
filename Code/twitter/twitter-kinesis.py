## Example to use twitter api and feed data into kinesis

from TwitterAPI import TwitterAPI
import boto3
import json
import twitterCreds
import pprint
from google.cloud import language
import uuid

def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area


language_client = language.Client()


## twitter credentials
consumer_key 		= twitterCreds.consumer_key
consumer_secret 	= twitterCreds.consumer_secret
access_token_key 	= twitterCreds.access_token_key
access_token_secret = twitterCreds.access_token_secret

# print twitterCreds.consumer_key, twitterCreds.consumer_secret, twitterCreds.access_token_key, twitterCreds.access_token_secret

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

kinesis = boto3.client('firehose')
# -74,40,-73,41
r = api.request('statuses/filter', {'locations':'-87.940267,41.644335,-87.523661,42.023131'})
# print r
for item in r:
	area = PolygonArea(item['place']['bounding_box']['coordinates'][0])
	print "area", area
	if area < 0.05:
		try:
			res = {}
			print "\n"
			text = item['text'].encode('utf-8').strip()
			res['text'] = text
			document = language_client.document_from_text(text)
			sentiment = document.analyze_sentiment().sentiment
			res['s_score'] = sentiment.score
			res['s_magnitude'] = sentiment.magnitude
			lats = []
			lngs = []
			res['place_name'] = str(item['place']['name'])
			for point in item['place']['bounding_box']['coordinates'][0]:
				lats.append(point[1])
				lngs.append(point[0])
			lat = sum(lats)/len(lats)
			lng = sum(lngs)/len(lngs)
			res['lat'] = lat
			res['lng'] = lng
			res['created_at'] = item['created_at']
			res['id'] = str(uuid.uuid4())
			record = json.dumps(res) + "\n"
			print record
			kinesis.put_record(DeliveryStreamName="twitter", Record={'Data': bytes(record)})
		except:
			pass

