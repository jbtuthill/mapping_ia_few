import os
import urllib.parse
import urllib.request
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)

env_path = os.path.join(current_directory, '../env')
# Load environment variables from a .env file
load_dotenv(env_path)

# Retrieve the API key from the environment variables
API_key = os.getenv('API_KEY')

class USDAQuickStats:
    """
    A class to interact with the USDA QuickStats API.
    """
    def __init__(self, api_key):
        """
        Initialize the USDAQuickStats object with the provided API key.
        """
        self.api_key = api_key
        self.base_url_api_get = f'http://quickstats.nass.usda.gov/api/api_GET/?key={self.api_key}&'

    def encode_parameters(self, params):
        """
        Encode parameters for the USDA QuickStats API.

        Parameters:
        - params (dict): Dictionary containing query parameters.

        Returns:
        - encoded_params (str): Encoded parameters string.
        """
        return urllib.parse.urlencode(params)

    def get_data(self, parameters):
        """
        Fetch data from the USDA QuickStats API based on the provided parameters.

        Parameters:
        - parameters (str): The parameters to be passed to the API.

        Returns:
        - df (DataFrame): A pandas DataFrame containing the fetched data.
        """
        full_url = self.base_url_api_get + parameters

        # Retrieve data from the Quick Stats server
        with urllib.request.urlopen(full_url) as response:
            s_text = response.read().decode('utf-8')

        # Parse the CSV data into a DataFrame
        df = pd.read_csv(StringIO(s_text))

        return df
