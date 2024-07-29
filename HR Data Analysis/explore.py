import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here
    df_office_A = pd.read_xml('../Data/A_office_data.xml')
    df_office_B = pd.read_xml('../Data/B_office_data.xml')
    df_HR = pd.read_xml('../Data/hr_data.xml')

    df_office_A.index = 'A' + df_office_A['employee_office_id'].astype('str')
    df_office_B.index = 'B' + df_office_B['employee_office_id'].astype('str')
    df_HR = df_HR.set_index('employee_id')

    df_office_full = pd.concat([df_office_A, df_office_B])
    df_HR_office = df_office_full.merge(df_HR, left_index=True, right_index=True,
                               how='left', indicator=True)

    df_HR_office = df_HR_office[df_HR_office['_merge'] == 'both']
    df_HR_office.drop(['_merge','employee_office_id'], axis=1, inplace=True)
    df_HR_office.sort_index(inplace=True)

    print(df_HR_office.index.tolist())
    print(df_HR_office.columns.tolist())

    # STAGE 1
    # print(df_office_A.index.to_list())
    # print(df_office_B.index.to_list())
    # print(df_HR.index.to_list())
