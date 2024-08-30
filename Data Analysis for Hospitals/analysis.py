import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(30)

if __name__ == '__main__':
    pd.set_option('display.max_columns', 8)

    df_general = pd.read_csv('test/general.csv')
    df_prenatal = pd.read_csv('test/prenatal.csv')
    df_sport = pd.read_csv('test/sports.csv')

    # Stage 1
    # print(df_general.head(20))
    # print(df_prenatal.head(20))
    # print(df_sport.head(20))

    # Stage 2
    df_prenatal.columns = df_general.columns
    df_sport.columns = df_general.columns

    df = pd.concat(
        [df_general, df_prenatal, df_sport], ignore_index=True)

    df.drop(columns=['Unnamed: 0'], inplace=True)
    # print(df.sample(20))

    # Stage 3
    df.dropna(thresh=1, inplace=True)
    df.gender = df.gender.apply(lambda x: 'm' if x in ['man', 'male'] else 'f')

    nan_col = ['bmi', 'diagnosis', 'blood_test',
               'ecg', 'ultrasound', 'mri',
               'xray', 'children', 'months']
    df[nan_col] = df[nan_col].apply(lambda x: x.fillna(0))

    # print(df.shape)
    # print(df.sample(20))

    # Stage 4
    # 1. Which hospital has the highest number of patients?
    max_patients = (df.groupby('hospital')
                    .agg({'gender': 'count'})
                    .sort_values('gender', ascending=False).iloc[0].name)

    # print(f'The answer to the 1st question is {max_patients}')

    # 2. What share of the patients in the general hospital suffers from stomach-related issues?
    stomach_share = (df[(df.hospital == 'general') &
                        (df.diagnosis == 'stomach')].shape[0] /
                     df[df.hospital == 'general'].shape[0])

    # print(f'The answer to the 2nd question is {stomach_share:.3}')

    # 3. What share of the patients in the sports hospital suffers from dislocation-related issues?
    dis_share = (df[(df.hospital == 'sports') &
                   (df.diagnosis == 'dislocation')].shape[0] /
                 df[df.hospital == 'sports'].shape[0])

    # print(f'The answer to the 3rd question is {dis_share:.3}')

    # 4. What is the difference in the median ages of the patients in the general and sports hospitals?
    age_differance = (df[df.hospital == 'general'].age.median() -
                      df[df.hospital == 'sports'].age.median())

    # print(f'The answer to the 4th question is {int(age_differance)}')

    # 5. How many blood tests were taken?
    max_test = (
        df[df.blood_test == 't']
        .pivot_table(index='hospital',
                     values='blood_test',
                     aggfunc='count',
                     sort=True).iloc)[-1]

    # print(f'The answer to the 5th question is {max_test.name}, {int(max_test.blood_test)} blood tests')

    # Stage 5

    # What is the most common age of a patient among all hospitals?
    df.age.plot(kind='hist', bins=[0, 15, 35, 55, 70])
    plt.show()

    # What is the most common diagnosis among patients in all hospitals?
    df.diagnosis.value_counts().plot(kind='pie')
    plt.show()

    # Build a violin plot of height distribution by hospitals.
    fig, axes = plt.subplots()
    axes.set_title('Height distribution')
    heights = [df[df.hospital == 'general'].height,
               df[df.hospital == 'prenatal'].height,
               df[df.hospital == 'sports'].height]
    plt.violinplot(heights)
    axes.set_xticks([1, 2, 3])
    axes.set_xticklabels(['general', 'prenatal', 'sports'])
    plt.show()

    print('The answer to the 1st question: 15-35')
    print('The answer to the 2nd question: pregnancy')
    print('The answer to the 3rd question: different measuring system')
