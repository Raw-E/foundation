from typing import List

# IDEA: Consider adding more string matching utilities like fuzzy matching or Levenshtein distance
def parts_match_in_order(sequence_parts: List[str], pattern_parts: List[str]) -> bool:
    """
    Checks if a pattern sequence appears within a larger sequence while maintaining order.
    This is useful for matching naming patterns, template parts, or any ordered sequence matching.
    
    Args:
        sequence_parts: List of parts from the full sequence to search within
        pattern_parts: List of parts to find in order
            
    Examples:
        sequence_parts = ['meal', 'plan', 'data', 'handler']
        pattern_parts = ['data', 'handler']
        -> Returns True (pattern found in order)
            
        sequence_parts = ['handler', 'data']
        pattern_parts = ['data', 'handler']
        -> Returns False (wrong order)
        
        sequence_parts = ['user', 'profile', 'view']
        pattern_parts = ['user', 'view']
        -> Returns True (pattern found in order, even with gaps)
    
    Returns:
        bool: True if pattern_parts are found in sequence_parts in the same order
    """
    if not pattern_parts:
        return False
            
    current_pos = 0
    for pattern_part in pattern_parts:
        # Find the next occurrence of the pattern part
        while current_pos < len(sequence_parts):
            if sequence_parts[current_pos] == pattern_part:
                current_pos += 1
                break
            current_pos += 1
        else:
            # Pattern part not found
            return False
    
    return True