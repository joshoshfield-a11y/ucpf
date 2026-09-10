"""
UCPF Utility Functions
======================

Helper functions for validation, visualization, and data handling.
"""

import numpy as np

def validate_positive(value, name):
    """Validate that a value is positive."""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value

def validate_range(value, name, min_val, max_val):
    """Validate that a value is within a range."""
    if not (min_val <= value <= max_val):
        raise ValueError(f"{name} must be in [{min_val}, {max_val}], got {value}")
    return value

def format_scientific(value, unit=""):
    """Format a number in scientific notation with unit."""
    if unit:
        return f"{value:.3e} {unit}"
    return f"{value:.3e}"

def compare_to_threshold(value, threshold, name="value"):
    """Compare a value to a threshold and return status."""
    if value >= threshold:
        return f"✓ {name} = {format_scientific(value)} >= threshold ({format_scientific(threshold)})"
    else:
        return f"✗ {name} = {format_scientific(value)} < threshold ({format_scientific(threshold)})"

def epistemic_tag(status):
    """Return a visual tag for epistemic status."""
    tags = {
        "PROVEN": "[✓✓✓]",
        "THEORETICALLY_CONSISTENT": "[✓✓ ]",
        "SPECULATIVE": "[✓  ]",
        "RULED_OUT": "[✗✗✗]",
        "UNKNOWN": "[?  ]",
    }
    return tags.get(status, "[?  ]")

def print_section(title, width=60):
    """Print a formatted section header."""
    print(f"\n{'='*width}")
    print(f"{title:^{width}}")
    print(f"{'='*width}")

def print_table(headers, rows, width=80):
    """Print a simple text table."""
    col_width = width // len(headers)
    print("-" * width)
    print("".join(f"{h:<{col_width}}" for h in headers))
    print("-" * width)
    for row in rows:
        print("".join(f"{str(v):<{col_width}}" for v in row))
    print("-" * width)
