import json
from pyspark.sql import DataFrame
from datetime import datetime, time
from typing import List, Any, Dict, Tuple

def convert_value(value: Any, dtype: str, enable_rounding: bool = True, rounding_precision: int = 6) -> Any:
    """
    Convert Spark SQL types to appropriate Python types for Google Sheets.

    Args:
        value: The value to convert
        dtype: The Spark SQL data type name (case-insensitive)
        enable_rounding: If True, round float/double/decimal values to rounding_precision decimal places
        rounding_precision: Number of decimal places to round to when enable_rounding is True

    Returns:
        Converted value suitable for Google Sheets. Arrays/maps/structs are
        JSON-serialized; any other unrecognised type falls back to str().
    """
    dtype = dtype.lower()

    if value is None:
        return 0 if dtype in ["bigint", "long", "double", "decimal", "float"] else ""

    def convert_float(x):
        v = float(x)
        return round(v, rounding_precision) if enable_rounding else v

    type_handlers = {
        "string": lambda x: str(x),
        "bigint": lambda x: int(x),
        "long": lambda x: int(x),
        "integer": lambda x: int(x),
        "int": lambda x: int(x),
        "tinyint": lambda x: int(x),
        "smallint": lambda x: int(x),
        "short": lambda x: int(x),
        "double": convert_float,
        "float": convert_float,
        "decimal": convert_float,
        "timestamp": lambda x: x.isoformat(),
        "timestamp_ntz": lambda x: x.isoformat(),
        "date": lambda x: datetime.combine(x, time.min).isoformat(),
        "boolean": lambda x: bool(x),
        "daytimeinterval": lambda x: str(x),
        "array": lambda x: json.dumps(x, default=str),
        "map": lambda x: json.dumps(x, default=str),
        "struct": lambda x: json.dumps(x.asDict(), default=str),
    }

    if dtype not in type_handlers:
        return str(value)

    return type_handlers[dtype](value)

def prepare_data(df: DataFrame, keep_header: bool, enable_rounding: bool = True, rounding_precision: int = 6) -> Tuple[List[List[Any]], List[int], List[str]]:
    """
    Convert DataFrame to list of lists with proper type conversion.

    Args:
        df: Spark DataFrame to convert
        keep_header: If True, exclude header from converted data
        enable_rounding: If True, round float/double/decimal values to rounding_precision decimal places
        rounding_precision: Number of decimal places to round to when enable_rounding is True

    Returns:
        Tuple containing:
        - List of lists with converted data
        - List of column indices containing dates
        - List of column headers
    """
    date_columns = [i for i, field in enumerate(df.schema)
                    if field.dataType.typeName().lower() == "date"]

    data = df.collect()
    header = df.columns

    converted_data = [] if keep_header else [header]

    for row in data:
        converted_row = [
            convert_value(value, df.schema[i].dataType.typeName(), enable_rounding, rounding_precision)
            for i, value in enumerate(row)
        ]
        converted_data.append(converted_row)

    return converted_data, date_columns, header