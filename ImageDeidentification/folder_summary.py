import os
import sys
import logging
from datetime import datetime
import heapq

def get_dir_size(path):
    """Calculate total size of a directory recursively"""
    total_size = 0
    try:
        # For a faster calculation on Linux systems, use du command
        if os.name == 'posix':
            du_output = os.popen(f'du -sb "{path}"').read()
            if du_output:
                size_str = du_output.split()[0]
                try:
                    return int(size_str)
                except ValueError:
                    pass  # Fall back to manual calculation if du fails
        
        # Manual calculation
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except (FileNotFoundError, PermissionError):
                    continue
    except Exception as e:
        logging.warning(f"Error calculating size for {path}: {e}")
    
    return total_size

def format_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def summarize_folders(base_path):
    # Setup logging
    log_file = os.path.join(os.getcwd(), "folder_summary.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
    
    logging.info(f"Starting folder summary for: {base_path}")
    
    if not os.path.isdir(base_path):
        logging.error(f"Error: {base_path} is not a valid directory")
        return
    
    # Calculate main folder size first
    logging.info(f"Calculating size of main directory ({base_path})...")
    base_size = get_dir_size(base_path)
    logging.info(f"Base directory size: {format_size(base_size)}")
    
    # Use heaps to efficiently track the newest and oldest folders
    newest_folders = []  # min heap for newest folders (we'll invert the time)
    oldest_folders = []  # max heap for oldest folders
    
    all_folders = []  # List to store all folders for writing to file
    
    total_folders = 0
    
    logging.info("Scanning first-level directories...")
    
    # Get first-level subdirectories only
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        
        if os.path.isdir(item_path):
            total_folders += 1
            
            try:
                # Get folder stats
                stat_info = os.stat(item_path)
                mod_time = stat_info.st_mtime
                
                # Count immediate subfolders
                subfolder_count = sum(1 for i in os.listdir(item_path) 
                                     if os.path.isdir(os.path.join(item_path, i)))
                
                # Add to all folders list
                all_folders.append((mod_time, item_path, subfolder_count))
                
                # Track newest folders
                if len(newest_folders) < 5:
                    heapq.heappush(newest_folders, (-mod_time, item_path, subfolder_count))
                elif -mod_time < newest_folders[0][0]:
                    heapq.heapreplace(newest_folders, (-mod_time, item_path, subfolder_count))
                
                # Track oldest folders
                if len(oldest_folders) < 5:
                    heapq.heappush(oldest_folders, (mod_time, item_path, subfolder_count))
                elif mod_time > oldest_folders[0][0]:
                    heapq.heapreplace(oldest_folders, (mod_time, item_path, subfolder_count))
                    
            except Exception as e:
                logging.error(f"Error processing {item_path}: {e}")
                continue
    
    logging.info("=" * 50)
    logging.info(f"Total first-level folders: {total_folders}")
    logging.info(f"Main directory size: {format_size(base_size)}")
    
    # Display newest folders
    logging.info("\nNewest folders:")
    newest_folders.sort()  # Sort by timestamp
    for timestamp, path, subfolder_count in newest_folders:
        date_str = datetime.fromtimestamp(-timestamp).strftime('%Y-%m-%d %H:%M:%S')
        folder_name = os.path.basename(path)
        logging.info(f"{date_str} - {folder_name} - Subfolders: {subfolder_count}")
    
    # Display oldest folders
    logging.info("\nOldest folders:")
    oldest_folders.sort(reverse=True)
    for timestamp, path, subfolder_count in oldest_folders:
        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        folder_name = os.path.basename(path)
        logging.info(f"{date_str} - {folder_name} - Subfolders: {subfolder_count}")
    
    # Write all folders to file
    output_file = os.path.join(os.getcwd(), "folder_list.csv")
    with open(output_file, 'w') as f:
        f.write("Folder Date,Folder Path,Subfolder Count\n")
        # Sort by date before writing
        all_folders.sort(key=lambda x: x[0])
        for timestamp, path, subfolder_count in all_folders:
            date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{date_str},{path},{subfolder_count}\n")
    
    logging.info(f"\nComplete list of folders written to: {output_file}")
    logging.info(f"Log file written to: {log_file}")

if __name__ == "__main__":
    print("sys.argv:", sys.argv)
    if len(sys.argv) != 2:
        print("Usage: python folder_summary.py <base_directory_path>")
        sys.exit(1)
    
    summarize_folders(sys.argv[1])