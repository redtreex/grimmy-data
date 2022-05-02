class utils:
    def merge_comparator(self, df):
        if len(df) == 2:
            col_1 = set(df[0].columns)
            col_2 = set(df[1].columns)
            return  col_1 == col_2
        else:
            return True
