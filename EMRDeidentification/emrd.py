import pandas as pd
import hashlib

class EMRDeidentification:
    def __init__(self, file_name, deid_path,  type, hash_columns, drop_columns, categorical_columns,
                  date_columns, hash_key = '123'):
        """
        Arguments:

        1. file_name: str - Path to the file
        2. type: str - Type of the file (e.g. Encounter, Patient, etc.)
        3. hash_columns: list - List of identifiers to hash
        4. drop_columns: list - List of columns to drop
        5. categorical_columns: list - List of columsn to convert to categorical
        6. date_columns: list - List of date/time columns to shift by a random number

        """
        self.type = type
        self.hash_columns = hash_columns
        self.drop_columns = drop_columns
        self.categorical_columns = categorical_columns
        self.date_columns = date_columns
        self.file_name = file_name
        #Check if file exists
        if not self.file_name.exists():
            raise FileNotFoundError(f'{self.file_name} does not exist')

        self.hash_key = hash_key
        self.path_to_deid_data = deid_path

    def read_file(self):
        self.df = pd.read_csv(self.file_name, sep = '|', nrows = 100)
        
    def hash_identifiers(self, save = False):
        """
        hash identifiers in the dataframe, and save the matching list if save is True
        """
        for column in self.hash_columns:
            if column in self.df.columns:
                self.df[column] = self.df[column].apply(lambda x: hash_value(x, self.hash_key))
            elif column.upper() in self.df.columns:
                self.df[column] = self.df[column].apply(lambda x: hash_value(x, self.hash_key))
            else:
                print(column + ' does not exist in ' + str(self.file_name))
        
        if save:
            for column in self.hash_columns:
                matching_list = pd.DataFrame( columns= [column, column + '_deid'])
                matching_list[column] = self.df[column].unique()
                matching_list[column + '_deid'] = matching_list[column].apply(lambda x: hash_value(x, self.hash_key))
                matching_list.to_csv(self.file_name.parent / ('matching_list_' + column + '.csv'), index = False)
                print(column + " matching list saved")
    
    def drop_identifiers(self):
        """
        Drop columns in the dataframe if they exist
        """
        for column in self.drop_columns:
            if column in self.df.columns:
                self.df.drop(columns=[column], inplace = True)
            elif column.upper() in self.df.columns:
                self.df.drop(columns=[column.upper()], inplace = True)
            else:
                print(column + ' does not exist in ' + str(self.file_name))
    
    def convert_to_categorical(self):
        """
        Convert columns to categorical
        """
        for column in self.categorical_columns:
            if column in self.df.columns:
                self.df[column] = self.df[column].astype('category')
            elif column.upper() in self.df.columns:
                self.df[column.upper()] = self.df[column.upper()].astype('category')
            else:
                print(column + ' does not exist in ' + str(self.file_name))
    
    def shift_dates(self):
        """
        Shift dates by a random number
        """
        for column in self.date_columns:
            if column in self.df.columns:
                self.df[column] = self.df[column].apply(lambda x: self.shift_date_unix(x))
            elif column.upper() in self.df.columns:
                self.df[column.upper()] = self.df[column.upper()].apply(lambda x: self.shift_date_unix(x))
            else:
                print(column + ' does not exist in ' + str(self.file_name))
    
    def shift_date_hash(self, date, hash_key):
        return (pd.to_datetime(date) + pd.DateOffset(days = deterministic_random_number(date, 300))).strftime('%Y-%m-%d')
    
    def shift_date_unix(self, date):
        """
        Convert date to unix timestamp and drop the first digit
        """
        if pd.isnull(date):
            return date
        date_utc = pd.to_datetime(date).tz_localize('UTC')
        date_unix = date_utc.timestamp()
        date_unix_deid = float('0' + str(date_unix)[1:])
        return pd.to_datetime(date_unix_deid, unit = 's').strftime('%Y-%m-%d')
    
    def save_file(self):
        self.df.to_csv(self.path_to_deid_data / (str(self.file_name.stem) + '.dsv'), index = False, sep = '|')
        del self.df

def hash_value(value, hash_key):
    return hashlib.sha256((str(value) + hash_key).encode()).hexdigest()

def deterministic_random_number(value, max_value=300):
    """
    Random Number Generator, deterministic given a string input
    """
    hash_value = hashlib.sha256(value.encode()).hexdigest()
    random_number = int(hash_value[:8], 16)
    random_number = random_number % (max_value + 1)
    
    return random_number