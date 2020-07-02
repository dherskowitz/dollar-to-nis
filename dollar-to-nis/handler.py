import boto3
import json
import urllib
from datetime import datetime, timedelta

bucket_name = "dh-app-static-storage"
data_file = "currency.json"
urls = {
    "USD": "https://api.exchangeratesapi.io/latest?base=USD&symbols=USD,ILS",
    "ILS": "https://api.exchangeratesapi.io/latest?base=ILS&symbols=USD,ILS"
}

s3 = boto3.client('s3')
now = datetime.utcnow()
now_formatted = datetime.strftime(now, "%a %b %d %Y %H:%M %p")


def get_file():
    response = s3.get_object(Bucket=bucket_name, Key=data_file)
    content = response['Body'].read().decode('utf-8')
    data = json.loads(content)
    return data


def lambda_handler(event, context):
    data = get_file()
    last_updated = datetime.strptime(
        data["last_updated"],
        "%a %b %d %Y %H:%M %p"
    )
    diff_greater_4_hours = (now - last_updated) > timedelta(hours=4)
    if diff_greater_4_hours:
        json_dict = {
            "last_updated": now_formatted
        }
        for url in urls:
            contents = urllib.request.urlopen(urls[url]).read()
            contents_json = json.loads(contents)
            json_dict[url] = contents_json["rates"]

        s3.put_object(
            Body=json.dumps(json_dict),
            Bucket=bucket_name, Key=data_file
        )
        data = get_file()

    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
