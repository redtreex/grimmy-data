import pandas as pd
from utils import utils

utils = utils()

class cleaning_methods:
    # Merged DF return type structure
    # {
    # 'file': merged_file,
    # 'merge_success': merge_success,
    # 'file_count': file_count
    # }
    def merge_df(self, df_files):
        file_count = len(df_files)
        merged_file = "this is merged file"
        merge_success = utils.merge_comparator(df_files)
        if file_count == 2 and merge_success:
            merged_file = pd.concat(df_files, ignore_index=True)
        else:
            merged_file = df_files[0]
        return {'file': merged_file}

    def deduplicated_df(self, df):
        df['file'] = df['file'].drop_duplicates()
        return df

    def null_removed_df(self, df):
        df['file'] = df['file'].dropna()
        return df


    def scaled_df(self, min_b, max_b, df):

        def Scaler(min_value, max_value, value):
            return (max_value - min_value) * ((value - min(value)) / (max(value) - min(value))) + min_value

        ary = list(df['file'].columns)
        scaled_df = df['file']
        for i in ary:
            if df['file'][i].dtype == 'int64':
                df['file'][i] = df['file'][i].astype('float64')

        for i in ary:
            if df['file'][i].dtype == 'float64':
                if float(df['file'][i].max()) > 1.0:
                    scaled_df[i] = Scaler(min_b, max_b, df['file'][i])
        df['file'] = scaled_df
        return df