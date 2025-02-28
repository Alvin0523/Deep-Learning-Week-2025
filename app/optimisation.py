import pandas as pd

def find_optimal_batch(df, batch_size):
    """Finds an optimal batch of tools for calibration."""
    # Simple optimization: sort by days until calibration and take the top N
    optimal_batch = df.sort_values(by='days_until_calibration').head(batch_size)
    return optimal_batch

# If you have more complex optimization needs, you can add more functions.
# Example: Grouping tools by type or location.

def group_tools_by_type(df, tool_type_column='tool_type'):
    """Groups tools by their type for efficient calibration."""
    if tool_type_column in df.columns:
        grouped_tools = df.groupby(tool_type_column)
        return grouped_tools
    else:
        return None

def group_tools_by_location(df, tool_location_column = "location"):
    """Groups tools by their location for efficient calibration"""
    if tool_location_column in df.columns:
        grouped_tools = df.groupby(tool_location_column)
        return grouped_tools
    else:
        return None

#Example of a more advanced optimization.
def advanced_optimal_batch(df, batch_size, tool_type_column = "tool_type", tool_location_column = "location"):
    """An example of a more complex optimisation. Groups by type and location, then sorts"""
    if tool_type_column in df.columns and tool_location_column in df.columns:
        grouped_type = df.groupby(tool_type_column)
        best_tools = pd.DataFrame()
        for name, group in grouped_type:
            grouped_location = group.groupby(tool_location_column)
            for name2, group2 in grouped_location:
                best_tools = pd.concat([best_tools, group2.sort_values(by = "days_until_calibration").head(1)])
        return best_tools.sort_values(by = "days_until_calibration").head(batch_size)
    else:
        return find_optimal_batch(df, batch_size) #if either column is missing, run the simple optimisation.