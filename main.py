import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz

first_round_df = pd.read_csv('result-1st-round_candidats.csv', encoding='latin1')
second_round_df = pd.read_csv('candidates-2nd-round.csv', delimiter=';', encoding='utf-8')

first_round_df['CodCirElec'] = first_round_df['CodCirElec'].apply(lambda x: str(x).zfill(4))
second_round_df['Code circonscription'] = second_round_df['Code circonscription'].apply(lambda x: str(x).zfill(4))

first_round_df['Key'] = first_round_df['CodCirElec'].astype(str)
second_round_df['Key'] = second_round_df['Code circonscription'].astype(str)

def is_candidate_in_first_round(row):
    for index, first_round_row in first_round_df[first_round_df['Key'] == row['Key']].iterrows():
        if fuzz.token_sort_ratio(row['Nom du candidat'], first_round_row['NomPsn']) > 90 and \
           fuzz.token_sort_ratio(row['Prénom du candidat'], first_round_row['PrenomPsn']) > 90:
            return True
    return False

#unmatched_second_round_candidates = second_round_df[~second_round_df.apply(is_candidate_in_first_round, axis=1)]
#for index, row in unmatched_second_round_candidates.iterrows():
#   print(row["Key"], row["Nom du candidat"], row["Prénom du candidat"])
#
#    for index, first_round_row in first_round_df[first_round_df['Key'] == row['Key']].iterrows():
#        nom = (fuzz.token_sort_ratio(row['Nom du candidat'], first_round_row['NomPsn']))
#        prenom = (fuzz.token_sort_ratio(row['Prénom du candidat'], first_round_row['PrenomPsn']))
#        print("\t",first_round_row['NomPsn'], nom, first_round_row['PrenomPsn'], prenom)
        
third_place_candidates = first_round_df.sort_values(by=['Key', 'NbVoix'], ascending=[True, False]) \
    .groupby('Key') \
    .nth(2) \
    .reset_index()

def is_candidate_in_second_round(row):
    for index, second_round_row in second_round_df[second_round_df['Key'] == row['Key']].iterrows():
        if fuzz.token_sort_ratio(row['NomPsn'], second_round_row['Nom du candidat']) > 90 and \
           fuzz.token_sort_ratio(row['PrenomPsn'], second_round_row['Prénom du candidat']) > 90:
            return True
    return False

third_place_candidates_in_second_round = third_place_candidates[third_place_candidates.apply(is_candidate_in_second_round, axis=1)]
filtered_third_place_candidates = third_place_candidates_in_second_round[
    (third_place_candidates_in_second_round['CodNuaCand'] != 'RN') & 
    (third_place_candidates_in_second_round['CodNuaCand'] != 'UXD')
]
party_counts = filtered_third_place_candidates['CodNuaCand'].value_counts()
total = party_counts.sum()
labels = [f'{party} ({count})' for party, count in party_counts.items()]

colors = {
    'ENS': 'orange',
    'LR': 'deepskyblue',
    'DVD': 'dodgerblue',
    'UG': 'red'
}

# plot 
plt.figure(figsize=(10, 6))
plt.pie(party_counts, labels=labels, autopct='%1.1f%%', startangle=140, colors=[colors.get(party, 'gray') for party in party_counts.index])
plt.title(f'{total} Candidats arrivés en 3ème position qui ne se désistent pas contre le RN/UXD')
plt.savefig('candidats_troisieme_non_desiste.png', bbox_inches='tight')
plt.close()

# print the list
for index, row in filtered_third_place_candidates.iterrows():
    print(f"{row['Key']}, {row['CodNuaCand']}， {row['NomPsn']}, {row['PrenomPsn']}")