"""
Simple test script to verify the Prolog integration is working correctly.
This test uses a simplified Prolog file to avoid compatibility issues.
"""
import os
import sys
import traceback
from pyswip import Prolog

def simple_prolog_test():
    """A very basic test of Prolog functionality without complex wrappers."""
    print("=== Starting Simple Prolog Test ===")
    
    # Check if the Prolog file exists
    prolog_file = 'ai/invader_ai_simple.pl'
    if not os.path.exists(prolog_file):
        print(f"Error: {prolog_file} not found")
        return False
    
    print(f"Prolog file found: {prolog_file}")
    
    try:
        # Create Prolog instance
        prolog = Prolog()
        print("Created Prolog instance")
        
        # Try to consult the file
        try:
            # Get absolute path
            full_path = os.path.abspath(prolog_file)
            print(f"Using path: {full_path}")
            
            # Try to consult the file
            print("Attempting to consult file...")
            prolog.consult(full_path)
            print("Successfully consulted Prolog file!")
        
            # Try a simple query
            print("\nTesting basic queries:")
            
            # Define some basic facts
            prolog.assertz("player(400, 500)")
            prolog.assertz("alien(1, 400, 100)")
            prolog.assertz("screen_size(800, 600)")
            print("Added test facts to knowledge base")
            
            # Test if the facts were added
            query_result = list(prolog.query("player(X, Y)"))
            if query_result:
                print(f"Player query result: {query_result}")
            else:
                print("Player query returned no results")
            
            # Test a more complex query
            query_result = list(prolog.query("should_fire_direct(1)"))
            print(f"Firing query result: {query_result}")
            
            print("\nBasic Prolog functionality works!")
            return True
        
        except Exception as e:
            print(f"Failed to consult Prolog file: {e}")
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"Error initializing Prolog: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if simple_prolog_test():
        print("\nSUCCESS: Prolog integration is working")
        sys.exit(0)
    else:
        print("\nFAILURE: Prolog integration failed")
        print("Possible reasons:")
        print("1. SWI-Prolog is not properly installed")
        print("2. PySwip is not properly configured")
        print("3. Incompatibility between PySwip and SWI-Prolog versions")
        print("\nSuggested fixes:")
        print("1. Check if SWI-Prolog is installed (run 'swipl --version' in terminal)")
        print("2. Reinstall PySwip with 'pip install -U pyswip'")
        print("3. Make sure environment variables are properly set (PATH includes SWI-Prolog)")
        sys.exit(1) 