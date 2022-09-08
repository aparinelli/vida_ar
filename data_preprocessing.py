from hashlib import new
import pandas as pd
import plotly.express as px

def get_count_dataframe(df, col_name, new_name):
    count = df[col_name].value_counts()
    return pd.DataFrame({new_name: count.index, 'count': count.values})

df = pd.read_csv('raw_data.csv')
physical_df = get_count_dataframe(df, 'texto_q49', 'Sport per week')
physical_df = physical_df.replace({'Sport per week': {
                            '0 días': '0 days',
                            '1 día': '1 day',
                            '2 días': '2 days',
                            '3 días': '3 days',
                            '4 días': '4 days',
                            '5 días': '5 days',
                            '6 días': '6 days',
                            '7 días': '7 days'
}})
physical_df = physical_df.drop([8])

fruits_df = get_count_dataframe(df, 'texto_q61', 'fruit')
fruits_df = fruits_df.replace({'fruit': {
                            '1 a 3 veces durante los últimos 7 días': '1 to 3 times in the last week',
                            'No comí frutas durante los últimos 7 días': 'I didn\'t eat fruit in the last week',
                            '1 vez al día': 'Once a day',
                            '4 a 6 veces durante los últimos 7 días': '4 to 6 times in the last week',
                            '2 veces al día': 'Twice a day',
                            '4 o más veces al día': '4 or more times a day',
                            '3 veces al día': 'Three times a day'
}})
fruits_df = fruits_df.drop([7])


# select soda and veg columns
soda_vegs_df = df.iloc[:, [105, 107]]

# get unique column combinations and convert to dataframe
soda_vegs_df = soda_vegs_df.groupby(['texto_q63', 'texto_q62']).size().to_frame().reset_index()


# rename columns
soda_vegs_df = soda_vegs_df.rename(columns={soda_vegs_df.columns[0]: 'Soda',soda_vegs_df.columns[1]: 'Vegs', soda_vegs_df.columns[2]: 'count'})

soda_vegs_df = soda_vegs_df.drop(soda_vegs_df.loc[soda_vegs_df['Soda']=='Dato perdido'].index)
soda_vegs_df = soda_vegs_df.drop(soda_vegs_df.loc[soda_vegs_df['Vegs']=='Dato perdido'].index)
soda_vegs_df = soda_vegs_df.set_index('Vegs')



ordered_index = ['No comí verduras ni hortalizas durante los últimos 7 días', '1 a 3 veces durante los últimos 7 días', '4 a 6 veces durante los últimos 7 días', '1 vez al día', '2 veces al día', '3 veces al día', '4 o más veces al día']
new_df = soda_vegs_df.iloc[0:7].reindex(ordered_index)

# grab each interval with a unique value in 'Soda' and reindex it
new_df = new_df.append(soda_vegs_df.iloc[7:14].reindex(ordered_index))
new_df = new_df.append(soda_vegs_df.iloc[14:21].reindex(ordered_index))
new_df = new_df.append(soda_vegs_df.iloc[21:28].reindex(ordered_index))
new_df = new_df.append(soda_vegs_df.iloc[28:35].reindex(ordered_index))
new_df = new_df.append(soda_vegs_df.iloc[35:42].reindex(ordered_index))
new_df = new_df.append(soda_vegs_df.iloc[42:49].reindex(ordered_index))

new_df['Vegs'] = new_df.index
new_df = new_df.reset_index(drop=True)



soda_vegs_df = new_df

# Translate to english
soda_vegs_df = soda_vegs_df.replace({
                        'Soda': {
                            '1 a 3 veces durante los últimos 7 días': '1 to 3 times in the last week',
                            '4 a 6 veces durante los últimos 7 días': '4 to 6 times in the last week',
                            '1 vez al día': 'Once a day',
                            '2 veces al día': 'Twice a day',
                            '3 veces al día': 'Three times a day',
                            '4 o más veces al día': '4 or more times a day',
                            'No tomé gaseosas en los últimos 7 días': 'I didn\'t drink any soda in the last week'
                        }})

# Translate to english
soda_vegs_df = soda_vegs_df.replace({
                        'Vegs': {
                            '1 a 3 veces durante los últimos 7 días': '1 to 3 times in the last week',
                            '4 a 6 veces durante los últimos 7 días': '4 to 6 times in the last week',
                            '1 vez al día': 'Once a day',
                            '2 veces al día': 'Twice a day',
                            '3 veces al día': 'Three times a day',
                            '4 o más veces al día': '4 or more times a day',
                            'No comí verduras ni hortalizas durante los últimos 7 días': 'I didn\'t eat any vegetables in the last week'
                        }})




alcohol_df = df.groupby(['texto_q2', 'texto_q34']).size().to_frame().reset_index()

# Remove 'Dato perdido' rows
alcohol_df.drop(alcohol_df[alcohol_df['texto_q2']=='Dato perdido'].index, axis=0, inplace=True)
alcohol_df.drop(alcohol_df[alcohol_df['texto_q34']=='Dato perdido'].index, axis=0, inplace=True)


# Rename columns
alcohol_df = alcohol_df.rename(columns={
                        alcohol_df.columns[0]: 'sex',
                        alcohol_df.columns[1]: 'alcohol',
                        alcohol_df.columns[2]: 'count'
})

# Translate
alcohol_df = alcohol_df.replace({
                        'sex': {
                            'Femenino': 'Female',
                            'Masculino': 'Male'
                        }
})

# Translate
alcohol_df = alcohol_df.replace({
                        'alcohol': {
                            '10 o 11 años': '10 or 11 years old',
                            '12 o 13 años': 'Between 12 and 15 years old',
                            '14 o 15 años': 'Between 12 and 15 years old',
                            '16 o 17 años': '16 or 17 years old',
                            '18 años o más': '18 years old',
                            '7 años o menos': '7 years old or less',
                            '8 o 9 años': '8 or 9 years old',
                            'Nunca tomé alcohol más que unos pocos sorbos': 'I never drank more than a few sips'
                        }
})


print(df.groupby(['texto_q28']).size())


# TODO:
# - add alcohol df (texto_q34)
# - add cigarrettes df (texto_q28)