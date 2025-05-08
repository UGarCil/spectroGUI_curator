'''
A library of auxiliary methods that help accessing, traversing and retrieving information from the main dataset of
images.npy
labels.npy
'''
import numpy as np 
from os.path import join as jn

# LLM - Jan 28th 2025 - Claude Sonnet v.3.5
# FD. calculate_num_samples()
# Signature: str tuple np.array -> int
# Purpose: to calculate the number of samples in a binary file given the shape of each sample
def calculate_num_samples(file_path, sample_shape, dtype=np.uint8):
    """
    Calculate the number of samples in a binary file given the shape of each sample.
    
    Args:
        file_path (str): Path to the binary file
        sample_shape (tuple): Shape of each sample (excluding batch dimension)
        dtype: Data type of the array (default: np.uint8)
        
    Returns:
        int: Number of samples in the file
    """
    # Get total file size in bytes
    file_size = os.path.getsize(file_path)
    print("file size: ",file_size)
    
    # Calculate size of each sample in bytes
    sample_size = np.prod(sample_shape) * np.dtype(dtype).itemsize
    print("sample size: ",sample_size)
    # Calculate number of samples
    num_samples = file_size // sample_size
    
    return num_samples


def load_main_dataset(path:str)->tuple:
    '''
    Given a path to the main dataset, returns the images, labels and indexes of the dataset
    indexes are recalculated
    '''
    images_path = jn(path, "images.npy")
    labels_path = jn(path, "labels.npy")
    total_samples = calculate_num_samples(images_path, (353, 715, 3))
    images = np.memmap(images_path, dtype=np.uint8, mode='r', shape=(total_samples,353, 715, 3))
    labels = np.memmap(labels_path, dtype=np.uint8, mode='r', shape=(total_samples,24))
    indexes = np.arange(len(images))
    return images, labels, indexes
