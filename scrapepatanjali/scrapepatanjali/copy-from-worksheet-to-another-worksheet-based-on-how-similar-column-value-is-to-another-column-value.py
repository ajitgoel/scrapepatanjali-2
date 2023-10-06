import pandas as pd
from difflib import SequenceMatcher 

file_path = '/home/ajitgoel/Downloads/LatestInvoice-WorkingCopy-09262023.xlsx'

df1 = pd.read_excel(file_path, sheet_name='BuyerInvoiceWithIngredientsList', skiprows=1, engine='openpyxl')  
df2 = pd.read_excel(file_path, sheet_name='Website-Products-10052023', skiprows=1, engine='openpyxl')

col_e_idx = 2 
col_c_idx = 2

col_e = df1.iloc[:, col_e_idx].str.lower().str.replace('[^a-z0-9]', ' ').str.strip().values
col_c = df2.iloc[:, col_c_idx].str.lower().str.replace('[^a-z0-9]', ' ').str.strip().values

for e in col_e:
    for c in col_c:
        seq = SequenceMatcher(None, e, c)
        if seq.ratio() > 0.7:
            
            idx = df2[df2.iloc[:, col_c_idx] == c].index[0]
            
            df1.iat[idx, 7] = df2.iat[idx, 3]
            df1.iat[idx, 8] = df2.iat[idx, 4] 
            df1.iat[idx, 9] = df2.iat[idx, 5]
            df1.iat[idx, 10] = df2.iat[idx, 6]
            df1.iat[idx, 11] = df2.iat[idx, 7]
            df1.iat[idx, 12] = df2.iat[idx, 8]
            df1.iat[idx, 13] = df2.iat[idx, 9]
            df1.iat[idx, 14] = df2.iat[idx, 10]
            
writer = pd.ExcelWriter('/home/ajitgoel/Downloads/LatestInvoice-WorkingCopy-09262023-New.xlsx', engine='openpyxl')
df1.to_excel(writer, sheet_name='Website-Products-10052023-new', header=False, index=False)  
writer.close()