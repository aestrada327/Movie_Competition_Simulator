file_name =  # path to file + file name
sheet =  # sheet name or sheet number or list of sheet numbers and names

import pandas as pd
df = pd.read_excel(io=file_name, sheet_name=sheet)
print(df.head(5))  # print first 5 rows of the dataframe