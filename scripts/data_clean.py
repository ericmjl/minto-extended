import pandas as pd

ird_df = pd.read_csv(
    '../data/20160411_Minto_Run2 Sequences.backup_20160518.csv')


def clean_strains_with_bad_dates(ird_df):
    """
    Removes strains that have bad dates (i.e. only MM-YYYY or YYYY).
    """
    ird_df['date_length'] = ird_df['Collection Date'].str.split('/').str.len()
    ird_df = ird_df[ird_df['date_length'] == 3]

    ird_df.to_csv('../data/20160411_Minto_Run2 Sequences.csv')


if __name__ == '__main__':
    clean_strains_with_bad_dates()
