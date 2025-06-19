"""
Configuration settings for musician network analysis.
"""

# File paths
DEFAULT_CSV_PATH = 'vinyl-collection.csv'
DEFAULT_OUTPUT_PATH = 'musician_network_complete_analysis.html'
NETWORK_CSV_PATH = 'musician_network.csv'
TRIPLES_CSV_PATH = 'musician_graph_triples.csv'

# Analysis parameters
SESSION_MUSICIAN_MIN_RECORDS = 2
SESSION_MUSICIAN_MIN_RATIO = 0.7
TOP_MUSICIANS_LIMIT = 20
SEARCH_RESULTS_LIMIT = 10

# Network visualization parameters
MAX_ARTIST_SYMBOL_SIZE = 35
MIN_ARTIST_SYMBOL_SIZE = 12
MAX_MUSICIAN_SYMBOL_SIZE = 25
MIN_MUSICIAN_SYMBOL_SIZE = 8
ARTIST_SIZE_MULTIPLIER = 1.5
MUSICIAN_SIZE_MULTIPLIER = 2

# Colors
MUSICIAN_COLOR = '#ff7f0e'  # Orange
ARTIST_COLOR = '#1f77b4'   # Blue

# HTML generation settings
ENABLE_DEBUG_MODE = True
INCLUDE_CHARTS = True
INCLUDE_SESSION_ANALYSIS = True 
