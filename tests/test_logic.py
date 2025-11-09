"""
Unit tests for the preprocessing logic functions.
"""

import pytest
import math
from src import preprocessing as pp  # Import the logic module

# ----------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------

@pytest.fixture
def sample_numeric_list() -> list:
    """Provides a simple list of numbers for numeric tests."""
    return [10, 20, 30, 40, 50]

@pytest.fixture
def list_with_missing() -> list:
    """Provides a list with various types of missing values."""
    return [1, 2.5, None, "hello", "", 4, float('nan'), 5]

# ----------------------------------------------------------------
# Test Functions
# ----------------------------------------------------------------

# Using parametrize for a simple function
@pytest.mark.parametrize("input_list, expected_output", [
    ([1, 2, None, 3, ''], [1, 2, 3]),
    ([float('nan'), 1, 2], [1, 2]),
    ([1, 2, 3], [1, 2, 3]),
    ([], []),
    ([None, '', float('nan')], [])
])
def test_remove_missing_values(input_list, expected_output):
    """Test the removal of various missing values."""
    assert pp.remove_missing_values(input_list) == expected_output

# Using parametrize for a function with options (defaults)
@pytest.mark.parametrize("fill_value, expected_output", [
    (0, [1, 2.5, 0, "hello", 0, 4, 0, 5]),
    ("NA", [1, 2.5, "NA", "hello", "NA", 4, "NA", 5]),
    (None, [1, 2.5, None, "hello", None, 4, None, 5])
])
def test_fill_missing_values(list_with_missing, fill_value, expected_output):
    """Test filling missing values with different fill values."""
    # We must use math.isclose for nan, as nan != nan
    result = pp.fill_missing_values(list_with_missing, fill_value=fill_value)
    
    # Custom assertion to handle potential 'nan' in results
    if fill_value == 0:
        # 0 was used to replace nan, check normally
         assert result == expected_output
    elif fill_value is None:
         # None was used, check normally
         assert result == expected_output
    else:
        # Check other cases
        assert result == expected_output


def test_remove_duplicates():
    """Test the removal of duplicate values, preserving order."""
    result = pp.remove_duplicates([1, "a", 2, "a", 1, 3, "b", 3])
    assert result == [1, "a", 2, 3, "b"]

def test_normalize_min_max(sample_numeric_list):
    """Test min-max normalization."""
    result = pp.normalize_min_max(sample_numeric_list, new_min=0.0, new_max=1.0)
    expected = [0.0, 0.25, 0.5, 0.75, 1.0]
    # Use approx for floating point comparisons
    assert result == pytest.approx(expected)

def test_standardize_z_score(sample_numeric_list):
    """Test z-score standardization."""
    result = pp.standardize_z_score(sample_numeric_list)
    # Mean=30, StDev=15.811...
    # (10-30)/15.811 = -1.264...
    # (20-30)/15.811 = -0.632...
    expected = [-1.264911, -0.632455, 0.0, 0.632455, 1.264911]
    assert result == pytest.approx(expected, abs=1e-5)

def test_clip_values():
    """Test clipping values to a specified range."""
    result = pp.clip_values([1, 5, 10, 15, 20], min_val=5, max_val=15)
    assert result == [5, 5, 10, 15, 15]

def test_convert_to_integers():
    """Test conversion of strings to integers, skipping non-numeric."""
    result = pp.convert_to_integers(["1", "2.5", "hello", "3.0", "4.9"])
    assert result == [1, 2, 3, 4]

def test_transform_log_scale():
    """Test log transformation, skipping non-positive numbers."""
    result = pp.transform_log_scale([1, 10, 100, 0, -5, math.e])
    expected = [0.0, math.log(10), math.log(100), 1.0]
    assert result == pytest.approx(expected)

def test_tokenize_text():
    """Test text tokenization and lowercasing."""
    result = pp.tokenize_text("Hello world! This is test #1.")
    assert result == "hello world this is test 1"

def test_select_alphanumeric_spaces():
    """Test removal of non-alphanumeric characters (except spaces)."""
    result = pp.select_alphanumeric_spaces("Hello, world! (v2.0) - Hi.")
    assert result == "Hello world v20  Hi"

def test_remove_stop_words():
    """Test removal of stop words (case-insensitive)."""
    text = "This is a Test Sentence about a test."
    stop_words = ["is", "a", "about"]
    result = pp.remove_stop_words(text, stop_words)
    assert result == "this test sentence test."

def test_flatten_list():
    """Test flattening a list of lists."""
    result = pp.flatten_list([[1, 2], [3, 4, 5], [], [6]])
    assert result == [1, 2, 3, 4, 5, 6]

def test_shuffle_list():
    """Test shuffling with a seed for reproducibility."""
    original_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    shuffled_list_1 = pp.shuffle_list(original_list, seed=42)
    shuffled_list_2 = pp.shuffle_list(original_list, seed=42)
    
    # The two shuffled lists should be identical
    assert shuffled_list_1 == shuffled_list_2
    # The shuffled list should be different from the original (statistically likely)
    assert shuffled_list_1 != original_list
    # The original list should not be modified
    assert original_list == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
