"""
Integration tests for the CLI module.
Tests if the CLI commands call the logic functions correctly.
"""

import pytest
from click.testing import CliRunner
from src.cli import cli  # Import the main 'cli' group

# ----------------------------------------------------------------
# Fixture
# ----------------------------------------------------------------

@pytest.fixture
def runner() -> CliRunner:
    """Fixture to create a CliRunner instance for invoking commands."""
    return CliRunner()

# ----------------------------------------------------------------
# Test Functions for each CLI command
# ----------------------------------------------------------------

def test_cli_clean_remove_missing(runner):
    """Test the 'clean remove-missing' command."""
    # We pass the command group, then a list of arguments
    result = runner.invoke(cli, [
        'clean', 
        'remove-missing', 
        "1,2,None,,nan,hello"
    ])
    
    # Check that the command exited successfully
    assert result.exit_code == 0
    # Check that the output printed to the console is correct
    # The output includes a newline character, so we use strip()
    assert result.output.strip() == "[1, 2, 'hello']"

def test_cli_clean_fill_missing(runner):
    """Test the 'clean fill-missing' command with an option."""
    result = runner.invoke(cli, [
        'clean',
        'fill-missing',
        "1,None,3",
        '--fill-value', 'NA'
    ])
    
    assert result.exit_code == 0
    assert result.output.strip() == "[1, 'NA', 3]"

def test_cli_numeric_normalize(runner):
    """Test the 'numeric normalize' command."""
    result = runner.invoke(cli, [
        'numeric',
        'normalize',
        "10,20,30"
        # We don't pass --min or --max to test the defaults (0.0, 1.0)
    ])
    
    assert result.exit_code == 0
    assert result.output.strip() == "[0.0, 0.5, 1.0]"

def test_cli_text_remove_stopwords(runner):
    """Test the 'text remove-stopwords' command."""
    result = runner.invoke(cli, [
        'text',
        'remove-stopwords',
        "this is a test",
        '--stopwords', "is,a"
    ])
    
    assert result.exit_code == 0
    assert result.output.strip() == "this test"

def test_cli_struct_flatten(runner):
    """Test the 'struct flatten' command with JSON input."""
    result = runner.invoke(cli, [
        'struct',
        'flatten',
        "[[1, 2], [3, 4]]"
    ])
    
    assert result.exit_code == 0
    assert result.output.strip() == "[1, 2, 3, 4]"

def test_cli_struct_shuffle(runner):
    """Test the 'struct shuffle' command with a seed."""
    result = runner.invoke(cli, [
        'struct',
        'shuffle',
        "1,2,3,4,5",
        '--seed', "42"
    ])
    
    assert result.exit_code == 0
    # The shuffled list with seed 42 is always the same
    assert result.output.strip() == "[4, 2, 3, 5, 1]"
