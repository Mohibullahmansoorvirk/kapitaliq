"""
The conftest.py file in Pytest is a local configuration file used to define, share, and reuse fixtures and hooks across multiple test files within a directory

Before running any tests, pytest automatically finds and executes conftest.py in the root directory
"""
#Global setup and environment variables available to all tests
from dotenv import load_dotenv
load_dotenv()