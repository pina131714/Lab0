"""
Core processing logic for the project.
This module contains all the data preprocessing functionalities.
"""

import math
import random
import re
import statistics
from typing import Any, List, Optional

# ----------------------------------------------------------------
# Data Cleaning Functions
# ----------------------------------------------------------------

def remove_missing_values(values: List[Any]) -> List[Any]:
    """
    Removes missing values (None, '', and nan) from a list.
    
    Args:
        values: A list of values that may contain missing ones.
    
    Returns:
        A new list with missing values removed.
    """
    output = []
    for v in values:
        # Check for None or empty string
        if v is None or v == '':
            continue
        # Check for float 'nan'
        if isinstance(v, float) and math.isnan(v):
            continue
        output.append(v)
    return output


def fill_missing_values(values: List[Any], fill_value: Any = 0) -> List[Any]:
    """
    Fills missing values (None, '', nan) with a specified default value.
    
    Args:
        values: A list of values.
        fill_value: The value to use for replacement (default is 0).
    
    Returns:
        A new list with missing values replaced.
    """
    output = []
    for v in values:
        is_missing = (
            v is None or 
            v == '' or
            (isinstance(v, float) and math.isnan(v))
        )
        if is_missing:
            output.append(fill_value)
        else:
            output.append(v)
    return output


# ----------------------------------------------------------------
# Data Structure Functions
# ----------------------------------------------------------------

def remove_duplicates(values: List[Any]) -> List[Any]:
    """
    Removes duplicate values from a list while preserving the original order.
    
    Args:
        values: A list of values.
    
    Returns:
        A new list with unique values, in order of first appearance.
    """
    # dict.fromkeys preserves insertion order in modern Python (3.7+)
    return list(dict.fromkeys(values))


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """
    Flattens a list of lists into a single list.
    
    Args:
        nested_list: A list where each element is itself a list.
    
    Returns:
        A single list containing all items from the sublists.
    """
    return [item for sublist in nested_list for item in sublist]


def shuffle_list(values: List[Any], seed: Optional[int] = None) -> List[Any]:
    """
    Shuffles a list randomly. Uses a seed for reproducible results if provided.
    
    Args:
        values: The list to shuffle.
        seed: An optional integer seed for the random number generator.
    
    Returns:
        A new list with elements in a random order.
    """
    if seed is not None:
        random.seed(seed)
    # We must copy the list, as random.shuffle works in-place
    shuffled_values = values.copy()
    random.shuffle(shuffled_values)
    return shuffled_values


# ----------------------------------------------------------------
# Numerical Processing Functions
# ----------------------------------------------------------------

def normalize_min_max(
    values: List[float], 
    new_min: float = 0.0, 
    new_max: float = 1.0
) -> List[float]:
    """
    Normalizes numerical values to a new range using the min-max method.
    
    Args:
        values: List of numerical values.
        new_min: The minimum value of the new range (default 0.0).
        new_max: The maximum value of the new range (default 1.0).
    
    Returns:
        A list of normalized values.
    """
    if not values:
        return []

    min_val = min(values)
    max_val = max(values)
    val_range = max_val - min_val
    
    if val_range == 0:
        # All values are the same, return the midpoint or min
        return [new_min] * len(values)
        
    new_range = new_max - new_min
    return [
        new_min + ((v - min_val) * new_range / val_range) 
        for v in values
    ]


def standardize_z_score(values: List[float]) -> List[float]:
    """
    Standardizes numerical values using the z-score method (mean=0, stdev=1).
    
    Args:
        values: List of numerical values.
    
    Returns:
        A list of standardized values.
    """
    if len(values) < 2:
        # Cannot calculate stdev with fewer than 2 values
        return [0.0] * len(values)
        
    mean_val = statistics.mean(values)
    stdev_val = statistics.stdev(values)
    
    if stdev_val == 0:
        # All values are the same, z-score is 0
        return [0.0] * len(values)
        
    return [(v - mean_val) / stdev_val for v in values]


def clip_values(
    values: List[float], 
    min_val: float, 
    max_val: float
) -> List[float]:
    """
    Clips numerical values to a specified minimum and maximum range.
    
    Args:
        values: List of numerical values.
        min_val: The minimum value to clip to.
        max_val: The maximum value to clip to.
    
    Returns:
        A list of clipped values.
    """
    output = []
    for v in values:
        if v < min_val:
            output.append(min_val)
        elif v > max_val:
            output.append(max_val)
        else:
            output.append(v)
    return output


def convert_to_integers(values: List[str]) -> List[int]:
    """
    Converts a list of strings to integers.
    Non-numerical strings are excluded from the output.
    
    Args:
        values: A list of strings.
    
    Returns:
        A list of integers.
    """
    output = []
    for v in values:
        try:
            # Use float first to handle strings like "10.0"
            num = float(v)
            output.append(int(num))
        except (ValueError, TypeError):
            # Skip values that cannot be converted (e.g., 'hello', None)
            continue
    return output


def transform_log_scale(values: List[float]) -> List[float]:
    """
    Transforms numerical values to a logarithmic scale.
    Only processes positive numbers.
    
    Args:
        values: List of numerical values.
    
    Returns:
        A list of log-transformed values.
    """
    output = []
    for v in values:
        if v > 0:
            output.append(math.log(v))
    return output


# ----------------------------------------------------------------
# Text Processing Functions
# ----------------------------------------------------------------

def tokenize_text(text: str) -> str:
    """
    Tokenizes text into words, keeping only alphanumeric characters
    and lowercasing.
    
    Note: The prompt specifies "Output: Processed text", so this
    returns a space-separated string of tokens.
    
    Args:
        text: The input string to process.
    
    Returns:
        A processed string of space-separated tokens.
    """
    # Find all sequences of alphanumeric characters (words)
    words = re.findall(r'\b\w+\b', text.lower())
    return ' '.join(words)


def select_alphanumeric_spaces(text: str) -> str:
    """
    Removes all characters from text except alphanumeric (a-z, A-Z, 0-9)
    and spaces.
    
    Args:
        text: The input string to process.
    
    Returns:
        A processed string with only alphanumeric chars and spaces.
    """
    # Create a regex pattern to match anything NOT alphanumeric or a space
    pattern = r'[^a-zA-Z0-9 ]'
    return re.sub(pattern, '', text)


def remove_stop_words(text: str, stop_words: List[str]) -> str:
    """
    Removes a list of stop-words from a text. The text is lowercased first.
    
    Args:
        text: The input string to process.
        stop_words: A list of stop-words to remove.
    
    Returns:
        A processed string with stop-words removed.
    """
    text_lower = text.lower()
    words = text_lower.split()
    
    # Using a set for stop_words gives faster lookup
    stop_words_set = set(stop_words)
    
    filtered_words = [w for w in words if w not in stop_words_set]
    return ' '.join(filtered_words)
