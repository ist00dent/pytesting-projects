# simple_ecommerce/__init__.py

try:
    # Attempt to initialize mock_db from tests.db_simulator
    from testing_simple_ecommerce.tests.db_simulator import MockDatabase

    mock_db = MockDatabase()
except ImportError:
    # Handle ImportError in case tests.db_simulator is not available
    print(
        "Warning: MockDatabase is not available. This may be due to running outside of the test environment."
    )
    mock_db = None  # You can also set it to a fallback value or raise an exception
except Exception as e:
    # Catch any other exceptions and print a detailed message
    print(f"Error initializing mock_db: {e}")
    mock_db = None  # Handle the error gracefully
