"""
Test script to verify that our patched os.makedirs function works correctly.
"""

import os

# Test the makedirs function
test_dir = "test_dir"
try:
    os.makedirs(test_dir, exist_ok=True)
    print(f"Successfully created directory: {test_dir}")
    
    # Clean up
    os.rmdir(test_dir)  # Using rmdir instead of removedirs for a simple directory
    print(f"Successfully removed directory: {test_dir}")
except Exception as e:
    print(f"Error: {e}")