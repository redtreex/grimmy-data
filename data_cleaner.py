from cleaning_methods import cleaning_methods


class data_cleaner:
    def clean_data(self, task, csv_files):
        cm = cleaning_methods()
        # merging csv files if both of them similar otherwise selecting the first one
        result = cm.merge_df(csv_files)

        # conditional
        if task['dedup']:
            # removing duplicated values
            result = cm.deduplicated_df(result)

        if task['rem-null']:
            # removing null values
            result = cm.null_removed_df(result)

        # statistical analysis
        result['desc'] = result['file'].describe()

        if task['scale']:
            # scaling values
            result = cm.scaled_df(0, 1, result)
        return result



























