import gspread
from gspread import service_account_from_dict


class GPP:

    @staticmethod
    def clear_sheet_except_header(sheet_id, sheet_name, creds_json):
        """Clears all data from a Google Sheets sheet, keeping the header intact.
        
        Args:
            sheet_id (str): The ID of the Google Sheets document.
            sheet_name (str): The name of the sheet to clear.
            creds_json (dict): A dictionary containing the service account credentials.
        """
        # Authorize the client using the credentials dictionary
        client = service_account_from_dict(creds_json)

        # Open the specified sheet
        sheet = client.open_by_key(sheet_id).worksheet(sheet_name)

        # Get the number of rows and columns
        num_rows = sheet.row_count
        num_cols = sheet.col_count

        # Clear the data while leaving the header intact (assumed to be the first row)
        if num_rows > 1:  # Ensure there are rows to clear
            sheet.batch_clear([f"A2:{gspread.utils.rowcol_to_a1(num_rows, num_cols)}"])  # Clear from row 2 to the last

        print("Cleared all data except the header.")

    @staticmethod
    def update_sheet_from_dataframe_except_header(pandas_df, sheet_id, sheet_name, creds_json):
        """Clears the specified Google Sheets sheet data and copies data from a Pandas DataFrame.
        
        Args:
            pandas_df (pd.DataFrame): The DataFrame containing data to be copied to the sheet.
            sheet_id (str): The ID of the Google Sheets document.
            sheet_name (str): The name of the sheet to update.
            creds_json (dict): A dictionary containing the service account credentials.
        """
        # Clear the existing data in the sheet while keeping the header
        GPP.clear_sheet_except_header(sheet_id, sheet_name, creds_json)

        # Authorize the client using the credentials dictionary
        client = service_account_from_dict(creds_json)

        # Open the specified sheet
        sheet = client.open_by_key(sheet_id).worksheet(sheet_name)

        # Get the number of rows in the DataFrame
        num_rows = len(pandas_df)

        # If the DataFrame is not empty, write the new data below the header
        if num_rows > 0:
            # Append the data starting from the second row (row 2 in the sheet)
            sheet.update('A2', pandas_df.values.tolist())  # Update starting from cell A2
            
    @staticmethod
    def debug(text="This is debug"):
        print(text)


