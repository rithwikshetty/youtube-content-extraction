"""
Data Processing Module

This module provides functionality for processing and exporting YouTube data.
"""

import pandas as pd
from typing import Dict
import logging

logger = logging.getLogger(__name__)

def export_to_excel(video_data: Dict[str, pd.DataFrame], output_file: str) -> None:
    """
    Export video data to Excel file with multiple sheets.
    
    Args:
        video_data (dict): Dictionary of DataFrames containing video data
        output_file (str): Path to output Excel file
    """
    try:
        with pd.ExcelWriter(output_file) as writer:
            for channel_name, df in video_data.items():
                sheet_name = channel_name[:31]  # Excel sheet names limited to 31 chars
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        logger.info(f"Data successfully exported to {output_file}")
    except Exception as e:
        logger.error(f"Error exporting data to Excel: {str(e)}") 