import os
import glob

def rows_generator(df):
    """
    Helper function for iterating over rows of a dataframe in groups of nrows length
    """
    i = 0
    nrows = 10000
    while (i+nrows) <= df.shape[0]:
        yield df.iloc[i:(i+nrows):1, :]
        i += nrows
    if ((i+nrows) > df.shape[0]):
        yield df.iloc[i:, :]

def get_files_in_path(filepath, extension):
    """
    Get all files from a filepath (recursive) with a given extension
    Returns a list of file paths
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, extension))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    if len(all_files) > 0:
        num_files = len(all_files)
        print('{} files found in {}'.format(num_files, filepath))
    else:
        print("No files found.")

    return all_files