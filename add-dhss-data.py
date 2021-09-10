import os
from argparse import ArgumentParser

if __name__ == "__main__":
    # Argument parsing setup
    parser = ArgumentParser()
    parser.add_argument('--path', type=str, default='~/Downloads', help='The path to the directory where data files are stored. Defaults to ~/Downloads.')
    args = parser.parse_args()

    data_path = args.path

    __expected_doses_file__ = "/Total_Doses_by_County_data.csv"
    __expected_initiated_file__ = "/Initiated_Vaccinations_by_Sex_data.csv"
    __expected_completed_file__ = "/Completed_Vaccinations_by_Sex_data.csv"
    __expected_testing_file__ = "/Metrics_by_Test_Date_by_County_data.csv"
    __expected_filenames__ = [__expected_doses_file__, __expected_initiated_file__, __expected_completed_file__, __expected_testing_file__]

    # If the path includes ~ for the user's home directory, expand it
    if '~' in data_path:
        data_path = os.path.expanduser(data_path)

    for filename in __expected_filenames__:
        path = f"{data_path}/{filename}".replace("//", "/")
        if "doses" in filename.lower() or "vaccinations" in filename.lower():
            data_type = "vaccine"
        elif "metrics" in filename.lower():
            data_type = "test"
        if os.path.exists(path):
            os.system(f"python add-{data_type}-data.py {path} --quiet")
        else:
            print(f"{path} does not exist. Skipping.")
