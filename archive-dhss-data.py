import os
import boto3
from zipfile import ZIP_DEFLATED, ZipFile
from tempfile import NamedTemporaryFile
from argparse import ArgumentParser
from utilities import utilities

if __name__ == "__main__":
    # Argument parsing setup
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', type=str, default='~/Downloads', help='The path to the directory where data files are stored. Defaults to ~/Downloads.')
    parser.add_argument('-d', '--date', type=str, default=utilities.data.today["date"], help='The date to which the files should be added. Defaults to the latest day in the dataset.')
    parser.add_argument('-f', '--force', action='store_true', help='Upload the archive to S3 even if the associated key already exists, overwriting the existing file on S3.')
    parser.add_argument('--keep_files', action='store_true', help='Retain the original data files after successful upload.')
    args = parser.parse_args()

    # Get the latest date in the dataset
    date = args.date

    # Create S3 client
    access_key_id = os.environ.get('AWS_COVID_ACCESS_KEY_ID')
    secret_access_key = os.environ.get('AWS_COVID_SECRET_ACCESS_KEY')
    s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name="us-west-2")

    # Set up variables with our expected file names
    __expected_doses_file__ = "/Total_Doses_by_County_data.csv"
    __expected_initiated_file__ = "/Initiated_Vaccinations_by_Sex_data.csv"
    __expected_completed_file__ = "/Completed_Vaccinations_by_Sex_data.csv"
    __expected_testing_file__ = "/Metrics_by_Test_Date_by_County_data.csv"
    __expected_filenames__ = [__expected_doses_file__, __expected_initiated_file__, __expected_completed_file__, __expected_testing_file__]

    data_path = args.path
    # If the path includes ~ for the user's home directory, expand it
    if '~' in data_path:
        data_path = os.path.expanduser(data_path)
        
    # Create file paths list
    paths = []
    for filename in __expected_filenames__:
        path = f"{data_path}/{filename}".replace("//", "/")
        if os.path.exists(path):
            paths.append(path)

    if len(paths) != 4:
        print('Could not find all four files in their expected locations. Exiting.')
        exit(1)

    s3_prefix = 'public/covid-19/dhss-archives/'
    s3_key = f'{s3_prefix}{date}.zip'
    
    with NamedTemporaryFile('w+') as temp, ZipFile(temp.name, 'w', compression=ZIP_DEFLATED) as zip:
        for path in paths:
            dir, filename = os.path.split(path)
            zip.write(path, filename)
        zip.close()
        # Get existing S3 keys to check whether we would be overwriting an existing key
        objects = s3_client.list_objects_v2(Bucket='data.jonblatho.com', Prefix=f"{s3_prefix}{date[:4]}")
        keys = [o["Key"] for o in objects["Contents"]]
        if s3_key not in keys or args.force:
            # Only upload if the key is not already present
            s3_client.upload_file(temp.name, 'data.jonblatho.com', s3_key)

    # Check for the completed upload and, if successful, add the URL as a source URL
    try:
        s3_client.get_object(Bucket='data.jonblatho.com', Key=s3_key)
        url = f"https://data.jonblatho.com/{s3_key}"
        os.system(f"python add-source-url.py {url} -d {date}")

        # Unless told not to, delete the original data files.
        if not args.keep_files:
            for path in paths:
                os.remove(path)
    except s3_client.exceptions.NoSuchKey:
        print(f"Expected key {s3_key} was not found in S3 bucket. Try again.")
        exit(1)