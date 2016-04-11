import pandas as pd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ird_df = pd.read_csv('../data/20160411_Minto_Run2 Sequences.csv')
ird_df['Strain Name'] = ird_df['Strain Name'].str.split('(').str[0]
ird_df['Host Species'] = ird_df['Host Species'].str.replace('IRD:', '')\
    .str.replace('/Avian', '')
ird_df.head()

submitted_df = pd.read_csv('../data/Alaska_waterfowl_79viruses_metadata_20151223.csv')
submitted_df['Strain_name'].tail()


def test_all_strains_of_interest_are_present():
    """
    Checks to make sure that all of the strains present in the 79 strains of
    interest are present in the IRD download.
    """
    for r, d in submitted_df.iterrows():
        assert d['Strain_name'] in ird_df['Strain Name'].values
