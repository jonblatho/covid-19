import os
import shutil
import boto3
from time import sleep
from utilities import utilities
from argparse import ArgumentParser

if __name__ == "__main__":
    # Argument parsing setup
    parser = ArgumentParser()
    parser.add_argument('date', type=str, default=utilities.data.today["date"], help='The date for which source links should be archived.')
    args = parser.parse_args()
    date = args.date

    month = date[:7]
    month_data = utilities.data.data_for_month(month)
    data = [d for d in month_data if d["date"] == date][0]

    if data["sources"] is not None:
        urls = [u for u in data["sources"] if data["sources"] is not None and "archive" not in u]
    else:
        print(f'No URLs found for {date}.')
        exit(0)
    print(f'Found {len(urls)} URLs to archive for {date}.')
    for url in urls:
        i = data["sources"].index(url)
        url_number = '0'+str(i+1)
        workdir = f'hchd-facebook-archive-{date}-{url_number}'
        print(f'   Archiving {url}...')
        url = url.replace('&', '\&')
        os.system(f'monolith {url} -o ~/hchd-archives/{date}-{url_number}.html -n')
        sleep(1)
        os.system(f'python ~/hchd-archives/cleanup.py ~/hchd-archives/{date}-{url_number}')
        try:
            # Create S3 client
            access_key_id = os.environ.get('AWS_COVID_ACCESS_KEY_ID')
            secret_access_key = os.environ.get('AWS_COVID_SECRET_ACCESS_KEY')
            s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name="us-west-2")
        except Exception:
            print('Error encountered while archiving.')
            exit(1)
        with open(f'/Users/jonblatho/hchd-archives/{date}-{url_number}.html', 'r') as f:
            contents = f.read()
            s3_key = f'public/covid-19/hchd-facebook-archives/{date}-{url_number}.html'
            s3_client.put_object(Bucket='data.jonblatho.com', Key=s3_key, Body=contents, ContentType='text/html')
        # Update the URL in the data
        data["sources"][i] = f'https://data.jonblatho.com/{s3_key}'
    utilities.save_json(month_data, f'daily-data/{month}.json')