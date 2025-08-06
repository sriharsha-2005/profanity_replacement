import os
import logging

logger = logging.getLogger(__name__)

def create_dir_if_not_exists(directory_path: str) -> None:
    """
    Create a directory if it doesn't exist.
    
    Args:
        directory_path (str): Path to the directory to create
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
            logger.info(f"Created directory: {directory_path}")
        else:
            logger.debug(f"Directory already exists: {directory_path}")
    except Exception as e:
        logger.error(f"Failed to create directory {directory_path}: {e}")
        raise

def get_file_extension(file_path: str) -> str:
    """
    Get the file extension from a file path.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: File extension (including the dot)
    """
    return os.path.splitext(file_path)[1]

def get_filename_without_extension(file_path: str) -> str:
    """
    Get the filename without extension from a file path.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Filename without extension
    """
    return os.path.splitext(os.path.basename(file_path))[0]

def ensure_file_exists(file_path: str) -> bool:
    """
    Check if a file exists and is accessible.
    
    Args:
        file_path (str): Path to the file to check
        
    Returns:
        bool: True if file exists and is accessible, False otherwise
    """
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)

def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        int: File size in bytes
    """
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        logger.error(f"Failed to get file size for {file_path}: {e}")
        return 0

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0 Bytes"
    
    size_names = ["Bytes", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"