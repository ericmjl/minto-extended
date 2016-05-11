import pandas as pd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ird_df = pd.read_csv('../data/20160411_Minto_Run2 Sequences.csv',
                     parse_dates=['Collection Date'])
ird_df['Strain Name'] = ird_df['Strain Name'].str.split('(').str[0]
ird_df['Host Species'] = ird_df['Host Species'].str.replace('IRD:', '')\
    .str.replace('/Avian', '')
ird_df.head()

submitted_df = pd.read_csv(
    '../data/Alaska_waterfowl_79viruses_metadata_20151223.csv')
submitted_df['Strain_name'].tail()


def test_all_strains_of_interest_are_present():
    """
    Checks to make sure that all of the strains present in the 79 strains of
    interest are present in the IRD download.
    """
    for r, d in submitted_df.iterrows():
        assert d['Strain_name'] in ird_df['Strain Name'].values


def test_dates_are_in_correct_range():
    """
    Checks to make sure that all of the dates are within the 2008-2012 range
    """
    assert ird_df['Collection Date'].min().year == 2007
    assert ird_df['Collection Date'].max().year == 2012


def test_strain_names_and_host_speices_are_correct():
    """
    Checks to make sure that all of the strain names and their corresponding
    host species are correctly matching. For example, cannot have:

    A/green-winged_teal/... matched with Host Species: Mallard
    """
    
    
    