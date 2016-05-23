import pandas as pd
from Bio import SeqIO
from tqdm import tqdm

ird_df = pd.read_csv(
    '../data/20160411_Minto_Run2 Sequences.backup_20160518.csv')
ird_df['Sequence Accession'] = ird_df['Sequence Accession'].str.strip('*')
ird_df.set_index('Sequence Accession', inplace=True)

corrected_df = pd.read_csv(
    '../data/20160411_Minto_Run2 Sequences.corrected_dates_20160506.csv',
    index_col=0)
# corrected_df[corrected_df['Dates_Corrected_By_Brandt']]
corrected_df['Sequence Accession'] = corrected_df['Sequence Accession']\
    .str.strip('*')
corrected_df.set_index('Sequence Accession', inplace=True)
corrected_df = corrected_df[corrected_df['Date_Corrected_By_Brandt'] == '*']
corrected_df.shape


def clean_strains_with_bad_dates(ird_df):
    """
    Removes strains that have bad dates (i.e. only MM-YYYY or YYYY).
    """
    ird_df['date_length'] = ird_df['Collection Date'].str.split('/').str.len()
    ird_df = ird_df[ird_df['date_length'] == 3]

    return ird_df


def correct_dates_provided_by_brandt(corrected_df, ird_df):
    """
    Brandt has provided a set of dates that are corrected. This function will
    modify the dates in ird_df using the dates in corrected_df.
    """
    print('Correcting dates provided by Brandt...')
    for r, d in tqdm(corrected_df.iterrows()):
        ird_df.set_value(r, 'Collection Date', d['Collection Date'])

    return ird_df


def filter_sequences_to_match_ird_data(ird_df):
    """
    Because of the data removal involved in cleaning strains with bad dates, I
    need another function that ensures that only the strains left behind are
    present in the dataset used for reconstruction.
    """
    ird_sequences = SeqIO.to_dict(
        SeqIO.parse(
            '../data/20160411_Minto_Run2 Sequences.backup_20160518.fasta',
            'fasta'))

    print('Filtering sequences...')
    filtered_sequences = dict()
    for k, v in tqdm(ird_sequences.items()):
        if k in ird_df.index:
            filtered_sequences[k] = v

    print('Final number of sequences:')
    print(len(filtered_sequences))
    SeqIO.write(filtered_sequences.values(),
                '../data/20160411_Minto_Run2 Sequences.fasta',
                'fasta')


def save_data(ird_df):
    ird_df.reset_index(inplace=True)
    ird_df.to_csv('../data/20160411_Minto_Run2 Sequences.csv')


if __name__ == '__main__':
    ird_df = correct_dates_provided_by_brandt(corrected_df, ird_df)
    ird_df = clean_strains_with_bad_dates(ird_df)
    filter_sequences_to_match_ird_data(ird_df)
    save_data(ird_df)
