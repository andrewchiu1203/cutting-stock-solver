import os
import csv
import zipfile

import pandas as pd
import xlsxwriter
class Excel:
    def __init__(self):

        df2 = pd.DataFrame([1,2,3,4,5,6])
        index=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        i=0
        while i in range(len(index)-1):
            self.append_df_to_excel('attempt',df2,index[i]+'1',index[i+1]+'1',i+2)
            i+=2


    def append_df_to_excel(self, filename, df, startCell,endCell,col,sheet_name='Sheet1', startrow=None, truncate_sheet=False, **to_excel_kwargs):
        try:
            # Load the existing workbook

            # Load the existing data into a DataFrame (assuming your data is stored in a DataFrame called df)
            #existing_df = pd.read_excel(filename+'.xlsx',engine='openpyxl')

            # Append new data to the DataFrame

            # Write the updated DataFrame to the worksheet

            writer = pd.ExcelWriter(filename+'.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay')
            #existing_df.to_excel(writer, sheet_name="Sheet1", index=False, header=False,startrow=1, startcol=0)

            df.to_excel(writer, sheet_name="Sheet1", index=False, header=False, startrow=1, startcol=col)
            worksheet = writer.sheets['Sheet1']

            # Merge cells in a range
            print('start:' + startCell.strip())
            print('end:' + endCell.strip())
            worksheet.merge_cells(startCell+ ':' + endCell)
            writer.close()



        # CREATE NEW Excel

        except (FileNotFoundError, zipfile.BadZipFile):

            # File doesn't exist, create a new workbook
            writer = pd.ExcelWriter(filename+'.xlsx', engine='openpyxl',mode='w')
            df.to_excel(writer, sheet_name='Sheet1', index=False,header=False,startrow=1)
            worksheet = writer.sheets['Sheet1']

            # Merge cells in a range
            print('start:' + startCell.strip())
            print('end:' + endCell.strip())
            worksheet.merge_cells(startCell + ':' + endCell)
            print("fuck you entered")
            writer.close()
    def appendCells(self,fileName,startCell,endCell):


        # Read the Excel file
        df = pd.read_excel(fileName)
        print(startCell==endCell)

        # Create a Pandas Excel writer using openpyxl engine
        writer = pd.ExcelWriter(fileName, engine='openpyxl')
        df.to_excel(writer, index=False, header=False ,sheet_name='Sheet1')

        # Access the worksheet object
        worksheet = writer.sheets['Sheet1']

        # Merge cells in a range
        print('start:'+startCell.strip())
        print('end:'+endCell.strip())
        worksheet.merge_cells(startCell.strip()+':'+endCell.strip())  # Merge cells in the range A1:B2

        # Save the changes
        writer.close()
Excel()