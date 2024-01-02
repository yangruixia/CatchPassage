# import pandas as pd

# # 读取两个 Excel 文件
# df1 = pd.read_excel('Code.xlsx')
# df2 = pd.read_excel('output.xlsx')

# # 获取第一个文件的'A'列的独特值
# unique_to_df1 = set(df1['编码']) - set(df2['作文编码'])

# # 输出结果
# print("只出现在第一个文件的'A'列而不在第二个文件中的数据：")
# print(unique_to_df1)

import pandas as pd

# 读取两个 Excel 文件
df_code = pd.read_excel('Code.xlsx')
df_output = pd.read_excel('output.xlsx')

merged_df = pd.merge(df_output, df_code[['编码', '性别']], how='left', left_on='作文编码', right_on='编码')
merged_df.rename(columns={'性别': '性别新'}, inplace=True)


# 将合并后的结果保存回 output.xlsx
merged_df.to_excel('output.xlsx', index=False)
