import os
from datetime import datetime
import json
from typing import List, Dict, Any

class Validation():
    def check_folders(self, folder_path: str) -> bool:
        if os.path.exists(folder_path):
            return True
        return False

    def check_files(self, file_path: str) -> bool:
        if os.path.exists(file_path):
            data = json.load(file_path)
            if len(data) > 27000:
                return True
        return False

class JsonFiles():
    """
        A class for working with JSON files.

        This class provides methods for creating folders and writing JSON files at those folders.

        Attributes:
            principal_folder (str): The root directory for storing JSON files.
            date (str): The current date in the format 'YYYY-MM'.

        Methods:
            folder_creation(): Creates necessary folders for storing JSON files.

    """
    def __init__(self) -> None:
        self.principal_folder = 'include/emplacamentos/data'
        self.date = datetime.now().strftime("%Y-%m")

    def folder_creation(self) -> None:
        """
            Create folders for storing JSON files based on the month.

            This method checks if the required folders exist and creates them if they don't.
        """
        if Validation().check_folders(self.principal_folder) == False:
            os.makedirs(self.principal_folder)
            print(f'{self.principal_folder} folder created!!!')

        files_folder = os.path.join(self.principal_folder, f'{self.date}')

        if Validation().check_folders(files_folder) == False:
            os.makedirs(files_folder)
            print(f'{files_folder} folder created!!!')

    def writing_data(self, data: List[Dict[str, Any]], file_name: str) -> None:
        self.folder_creation()

        date_folder = os.path.join(self.principal_folder, f'{self.date}')
        json_file_path = os.path.join(date_folder, f'{file_name}_{self.date}.json')

        # if Validation().checking_csv_data(file_path=csv_file_path, file_name=file_name) == False:
        if data != {}:
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4, default=str)
