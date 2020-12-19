import numpy as np
import pandas as pd

def transform_age(df, age_column):
    df = df.loc[df.loc[:, age_column] != 'NULL']
    range_column = age_column + '_Period Range'
    df[age_column + '_Periods'], df[range_column] = df.loc[:, age_column].str.split(' ').str[0].fillna(0).astype(int), df.loc[:, age_column].str.split(' ').str[1].fillna(0)
    df[range_column] = np.where(df[range_column].str.contains('day'), 1, 
                                  np.where(df[range_column].str.contains('week'), 7, 
                                           np.where(df[range_column].str.contains('month'), 30, 
                                                    np.where(df[range_column].str.contains('year'), 365, 0)))).astype(int)
    df[age_column + '_(days)'] = df[range_column] * df[age_column + '_Periods']
    df[age_column + '_(years)'] = df[age_column + '_(days)'] / 365
    df[age_column + '_age_group'] = pd.cut(df[age_column + '_(years)'], 10)
    return df

def transform_date(df, event):
    event_date = event + '_datetime'
    df[event_date] = pd.to_datetime(df['datetime'])
    df[event + '_month'] = df[event_date].dt.month
    df[event + '_year'] = df[event_date].dt.year
    df[event + '_monthyear'] = df[event + '_datetime'].dt.to_period('M')
    df[event + '_weekday'] = df[event_date].dt.day_name()
    df[event + '_hour'] = df[event_date].dt.hour
    df.rename(columns={event + '_name': 'name'}, inplace=True)
    return df

def create_unique_id(df, event):
    df.reset_index(inplace=True)

    df[event + '_number'] = df.groupby(['animal_id'])[event + '_time'].rank(method='dense', ascending=False)
    df['animal_id_new'] = df['animal_id'] + '_' + df[event + '_number'].astype(int).astype(str)

    return df