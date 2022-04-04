import os
from typing import Iterable
from datetime import datetime

import pandas as pd


def get_all_files(dir: str) -> Iterable[str]:
    """ Takes a directory and returns all files in it.

    Args:
        dir (str): Directory path

    Returns:
        Iterable[str]: absolute file paths

    Yields:
        Iterator[Iterable[str]]: absolute file paths
    """
    for dir_path, _, files in os.walk(dir):
        for f in files:
            yield os.path.abspath(os.path.join(dir_path, f))


def extract_file_info(files: Iterable[str]) -> pd.DataFrame:
    """ Extracts file information from a list of files. 
        The information is  extracted from the file name.
    
    Args:
        files (Iterable[str]): List of files
    
    Returns:
        pd.DataFrame: DataFrame with file information
    """
    records = []
    for f in files:
        file_stat = os.stat(f)
        c_datetime = datetime.utcfromtimestamp(file_stat.st_ctime)
        m_datetime = datetime.utcfromtimestamp(file_stat.st_mtime)
        record = {
            "path": f,
            "extension": os.path.splitext(f)[-1].replace('.', ''),
            "size": file_stat.st_size,
            "create_date": c_datetime.strftime("%d-%m-%Y"),
            "create_time": c_datetime.strftime("%H:%M:%S"),
            "modify_date": m_datetime.strftime("%d-%m-%Y"),
            "modify_time": m_datetime.strftime("%H:%M:%S")
        }
        records.append(record)

    return pd.DataFrame(records)


def extract_text_from_pdf(file: str) -> str:
    """ Extracts text from a pdf file.
    
    Args:
        file (str): File path
        
    Returns:
        str: Text from pdf file
    """
    from pdfminer import high_level

    with open(file, 'rb') as f:
        return high_level.extract_text(f)
