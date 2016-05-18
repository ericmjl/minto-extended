import pandas as pd
from Bio import SeqIO

ird_df = pd.read_csv(
    '../data/20160411_Minto_Run2 Sequences.backup_20160518.csv')
ird_df['Sequence Accession'] = ird_df['Sequence Accession'].str.strip('*')


def clean_strains_with_bad_dates(ird_df):
    """
    Removes strains that have bad dates (i.e. only MM-YYYY or YYYY).
    """
    ird_df['date_length'] = ird_df['Collection Date'].str.split('/').str.len()
    ird_df = ird_df[ird_df['date_length'] == 3]

    ird_df.to_csv('../data/20160411_Minto_Run2 Sequences.csv')


def filter_sequences_to_match_ird_data():
    """
    Because of the data removal involved in cleaning strains with bad dates, I
    need another function that ensures that only the strains left behind are
    present in the dataset used for reconstruction.
    """
    ird_sequences = SeqIO.to_dict(
        SeqIO.parse(
            '../data/20160411_Minto_Run2 Sequences.backup_20160518.fasta',
            'fasta'))

    filtered_sequences = dict()
    for k, v in ird_sequences.items():
        if k in ird_df['Sequence Accession'].values:
            filtered_sequences[k] = v

    SeqIO.write(filtered_sequences.values(),
                '../data/20160411_Minto_Run2 Sequences.fasta',
                'fasta')

if __name__ == '__main__':
    clean_strains_with_bad_dates(ird_df)
    filter_sequences_to_match_ird_data()
