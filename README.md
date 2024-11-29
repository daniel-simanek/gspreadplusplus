# gspreadplusplus

A Python library that enhances Google Sheets operations with additional functionality and improved data type handling.

## Features

- Transfer Spark DataFrames to Google Sheets with proper type conversion
- Intelligent handling of various data types (numbers, dates, timestamps, etc.)
- Preserve or update sheet headers
- Selective column clearing options
- Automatic date formatting
- Sheet dimension management

## Installation

```bash
pip install gspreadplusplus
```

## Requirements

- Python 3.7+
- gspread
- pyspark
- google-auth

## Usage

### Basic DataFrame Export

```python
from gspreadplusplus import GPP
from pyspark.sql import SparkSession

# Initialize Spark and create a DataFrame
spark = SparkSession.builder.appName("example").getOrCreate()
df = spark.createDataFrame([
    ("2024-01-01", 100, "Complete"),
    ("2024-01-02", 150, "Pending")
], ["date", "amount", "status"])

# Your Google Sheets credentials
creds_json = {
    "type": "service_account",
    # ... rest of your service account credentials
}

# Export DataFrame to Google Sheets
GPP.df_to_sheets(
    df=df,
    spreadsheet_id="your_spreadsheet_id",
    sheet_name="Sheet1",
    creds_json=creds_json
)
```

### Advanced Options

```python
GPP.df_to_sheets(
    df=df,
    spreadsheet_id="your_spreadsheet_id",
    sheet_name="Sheet1",
    creds_json=creds_json,
    english_locale=True,  # Use '.' as decimal separator
    keep_header=True,     # Preserve existing header row
    erase_whole=False     # Clear only necessary columns
)
```

## Data Type Support

- Strings
- Integers (regular, long, bigint)
- Floating point numbers (double, float)
- Decimals
- Dates
- Timestamps
- Booleans

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.