import pandas as pd
from openpyxl import load_workbook

# 读取 output.xlsx 文件中的 O 列数据
df = pd.read_excel('output3.xlsx', usecols='O', names=['O'])

# 统一数据类型
df['O'] = df['O'].astype(str)  # 将 O 列的数据类型转换为字符串类型

# 对 O 列数据进行处理（在这里只是简单的删除 {}、()、[] 及其中的内容）
df['A'] = df['O'].replace(to_replace=r'\{.*?\}|\[.*?\]|\(.*?\)', value='', regex=True)

# 将处理后的数据写入 output_modified.xlsx 文件的 A 列
with pd.ExcelWriter('output_modified3.xlsx') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False, columns=['A'])
