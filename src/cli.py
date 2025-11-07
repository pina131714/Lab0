"""
Command Line Interface (CLI) for the data preprocessing project.

This module uses 'click' to create a CLI that interacts with the
functions defined in 'preprocessing.py'.
"""

import json
import click
# Import the logic functions from preprocessing.py
# We use 'pp' as an alias to keep things tidy
from src import preprocessing as pp

# ----------------------------------------------------------------
# Helper Functions for Input Parsing
# ----------------------------------------------------------------

def _smart_cast(value: str) -> any:
    """
    Tries to cast a string value to its 'correct' type (None, nan, int, float, str).
    """
    val = value.strip()  # Remove leading/trailing whitespace
    
    # Handle special values first
    if val.lower() == 'none':
        return None
    if val.lower() == 'nan':
        return float('nan')
    if val == '""' or val == "''" or val == "":
        return ""  # Keep empty strings as they are

    # Try casting to int, then float
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            # If all fails, return it as a string
            return val

def _parse_list_input(ctx, param, value: str) -> list:
    """
    Click callback to parse a comma-separated string from the CLI
    into a Python list, using _smart_cast for each item.
    """
    if value is None:
        return []
    try:
        # Split the string by commas and cast each item
        return [_smart_cast(item) for item in value.split(',')]
    except Exception as e:
        raise click.BadParameter(f"Could not parse list: {e}")

def _parse_json_input(ctx, param, value: str) -> list:
    """
    Click callback to parse a JSON string (e.g., for list of lists).
    """
    if value is None:
        return []
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        raise click.BadParameter("Input must be a valid JSON string (e.g., '[[1,2],[3,4]]').")

def _validate_numeric_list(values: list) -> list[float]:
    """
    Validates that all items in a list are numeric and converts them to float.
    Raises BadParameter if any value is not numeric.
    """
    try:
        # Convert all parsed values to float for numeric operations
        return [float(v) for v in values]
    except (ValueError, TypeError):
        raise click.BadParameter(f"All values must be numeric. Received: {values}")

# ----------------------------------------------------------------
# Main CLI Group
# ----------------------------------------------------------------

@click.group()
def cli():
    """
    A Command Line Interface for data preprocessing tasks.
    
    This CLI provides access to cleaning, numerical, text, and
    structural data manipulation functions.
    """
    pass

# ----------------------------------------------------------------
# 1. 'clean' Sub-group
# ----------------------------------------------------------------

@cli.group(help="Functions related to data cleaning.")
def clean():
    """Data cleaning commands."""
    pass

@clean.command(
    'remove-missing',
    help="Removes missing values (None, '', nan) from a list.",
    epilog="Example: uv run python src/cli.py clean remove-missing \"1,2,None,hello,,nan,4.5\""
)
@click.argument('values', callback=_parse_list_input)
def remove_missing(values):
    """Removes missing values from a list."""
    result = pp.remove_missing_values(values)
    click.echo(result)

@clean.command(
    'fill-missing',
    help="Fills missing values with a specified value (default: 0).",
    epilog="Example: uv run python src/cli.py clean fill-missing \"1,2,None,,5\" --fill-value 0"
)
@click.argument('values', callback=_parse_list_input)
@click.option(
    '--fill-value', 
    default="0",  # Pass default as string, _smart_cast will handle it
    help="Value to use for filling missing items (e.g., '0', 'mean', 'None')."
)
def fill_missing(values, fill_value):
    """Fills missing values with a given value."""
    # Cast the fill_value itself, so user can pass "0", "hello", "None", etc.
    casted_fill_value = _smart_cast(fill_value)
    result = pp.fill_missing_values(values, casted_fill_value)
    click.echo(result)

# ----------------------------------------------------------------
# 2. 'numeric' Sub-group
# ----------------------------------------------------------------

@cli.group(help="Functions for processing numerical attributes.")
def numeric():
    """Numerical processing commands."""
    pass

@numeric.command(
    'normalize',
    help="Normalizes numerical values to a [min, max] range.",
    epilog="Example: uv run python src/cli.py numeric normalize \"1,2,3,4,5\" --min 0 --max 1"
)
@click.argument('values', callback=_parse_list_input)
@click.option('--min', 'new_min', default=0.0, type=float, help="New minimum value.")
@click.option('--max', 'new_max', default=1.0, type=float, help="New maximum value.")
def normalize(values, new_min, new_max):
    """Normalizes a list of numbers using min-max scaling."""
    try:
        numeric_values = _validate_numeric_list(values)
        result = pp.normalize_min_max(numeric_values, new_min=new_min, new_max=new_max)
        click.echo(result)
    except click.BadParameter as e:
        click.echo(e, err=True)

@numeric.command(
    'standardize',
    help="Standardizes numerical values using z-score.",
    epilog="Example: uv run python src/cli.py numeric standardize \"10,20,30,40,50\""
)
@click.argument('values', callback=_parse_list_input)
def standardize(values):
    """Standardizes a list of numbers using z-score."""
    try:
        numeric_values = _validate_numeric_list(values)
        result = pp.standardize_z_score(numeric_values)
        click.echo(result)
    except click.BadParameter as e:
        click.echo(e, err=True)

@numeric.command(
    'clip',
    help="Clips numerical values to a specified range.",
    epilog="Example: uv run python src/cli.py numeric clip \"1,5,10,15,20\" --min 5 --max 15"
)
@click.argument('values', callback=_parse_list_input)
@click.option('--min', 'min_val', default=0.0, type=float, help="Minimum value to clip to.")
@click.option('--max', 'max_val', default=1.0, type=float, help="Maximum value to clip to.")
def clip(values, min_val, max_val):
    """Clips a list of numbers to a min/max range."""
    try:
        numeric_values = _validate_numeric_list(values)
        result = pp.clip_values(numeric_values, min_val=min_val, max_val=max_val)
        click.echo(result)
    except click.BadParameter as e:
        click.echo(e, err=True)

@numeric.command(
    'to-int',
    help="Converts a list of string values to integers.",
    epilog="Example: uv run python src/cli.py numeric to-int \"1.0,2.5,hello,3\""
)
@click.argument('values', callback=_parse_list_input)
def to_int(values):
    """Converts list of strings to integers, skipping non-numeric values."""
    # The logic function pp.convert_to_integers already handles
    # filtering non-numeric values, so no extra validation is needed here.
    result = pp.convert_to_integers(values)
    click.echo(result)

@numeric.command(
    'log-transform',
    help="Transforms numerical values to a logarithmic scale.",
    epilog="Example: uv run python src/cli.py numeric log-transform \"1,10,100,0,-5\""
)
@click.argument('values', callback=_parse_list_input)
def log_transform(values):
    """Transforms a list of numbers to log scale, skipping non-positive values."""
    try:
        numeric_values = _validate_numeric_list(values)
        result = pp.transform_log_scale(numeric_values)
        click.echo(result)
    except click.BadParameter as e:
        click.echo(e, err=True)

# ----------------------------------------------------------------
# 3. 'text' Sub-group
# ----------------------------------------------------------------

@cli.group(help="Functions to deal with textual information.")
def text():
    """Text processing commands."""
    pass

@text.command(
    'tokenize',
    help="Tokenizes text, keeping only alphanumeric chars and lowercasing.",
    epilog="Example: uv run python src/cli.py text tokenize \"Hello world! This is 1 test.\""
)
@click.argument('input_text', type=str)
def tokenize(input_text):
    """Tokenizes text to alphanumeric words."""
    result = pp.tokenize_text(input_text)
    click.echo(result)

@text.command(
    'remove-punctuation',
    help="Selects only alphanumeric characters and spaces.",
    epilog="Example: uv run python src/cli.py text remove-punctuation \"Hello, world! (v2.0)\""
)
@click.argument('input_text', type=str)
def remove_punctuation(input_text):
    """Removes non-alphanumeric characters (except spaces)."""
    # This command maps to the `select_alphanumeric_spaces` function
    result = pp.select_alphanumeric_spaces(input_text)
    click.echo(result)

@text.command(
    'remove-stopwords',
    help="Removes stop-words from text (case-insensitive).",
    epilog="Example: uv run python src/cli.py text remove-stopwords \"this is a test sentence\" --stopwords \"is,a,this\""
)
@click.argument('input_text', type=str)
@click.option(
    '--stopwords',
    callback=_parse_list_input,
    help="Comma-separated list of stopwords to remove (e.g., \"is,a,the\")."
)
def remove_stopwords(input_text, stopwords):
    """Removes a given list of stop-words from text."""
    # The callback will provide a list of strings
    result = pp.remove_stop_words(input_text, stopwords)
    click.echo(result)

# ----------------------------------------------------------------
# 4. 'struct' Sub-group
# ----------------------------------------------------------------

@cli.group(help="Functions related to the structure of data.")
def struct():
    """Data structure manipulation commands."""
    pass

@struct.command(
    'unique-values',
    help="Removes duplicated values from a list, preserving order.",
    epilog="Example: uv run python src/cli.py struct unique-values \"a,b,a,c,b,a\""
)
@click.argument('values', callback=_parse_list_input)
def unique_values(values):
    """Removes duplicate values from a list."""
    # This command maps to the `remove_duplicates` function
    result = pp.remove_duplicates(values)
    click.echo(result)

@struct.command(
    'flatten',
    help="Flattens a list of lists into a single list.",
    epilog="Example: uv run python src/cli.py struct flatten \"[[1,2],[3,4],[5]]\""
)
@click.argument('values', callback=_parse_json_input)
def flatten(values):
    """Flattens a list of lists (passed as a JSON string)."""
    # Basic validation that we got a list of lists
    if not isinstance(values, list) or (values and not all(isinstance(i, list) for i in values)):
         click.echo(f"Error: Input must be a list of lists. e.g., '[[1,2],[3,4]]'", err=True)
         return
    result = pp.flatten_list(values)
    click.echo(result)

@struct.command(
    'shuffle',
    help="Randomly shuffles a list of values.",
    epilog="Example: uv run python src/cli.py struct shuffle \"1,2,3,4,5\" --seed 42"
)
@click.argument('values', callback=_parse_list_input)
@click.option(
    '--seed', 
    default=None, 
    type=int, 
    help="Seed to ensure reproducibility."
)
def shuffle(values, seed):
    """Shuffles a list, with an optional seed for reproducibility."""
    result = pp.shuffle_list(values, seed=seed)
    click.echo(result)

# ----------------------------------------------------------------
# Entry point for running the CLI
# ----------------------------------------------------------------

if __name__ == "__main__":
    cli()
