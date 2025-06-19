# 🎵 Musician Network Analysis

An interactive visualization tool that analyzes musician collaborations from vinyl record collection data, creating a comprehensive network graph with detailed insights.

## 🌟 Features

- **Interactive Network Visualization**: Explore musician-artist connections with ECharts
- **Advanced Filtering**: Filter by genres, styles, roles, and connection count
- **Top Musicians Analysis**: Charts and rankings by record appearances
- **Session Musicians Discovery**: Find the unsung heroes with high session work ratios
- **Debug Tools**: Search and analyze specific musicians in detail
- **Responsive Design**: Works on desktop and mobile devices

## 📁 Project Structure

```
musician-network-analysis/
├── main.py                 # Main orchestration script
├── data_processor.py       # Data loading and processing functions
├── analysis.py            # Musician statistics and analysis
├── html_generator.py      # HTML visualization generation
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── vinyl-collection.csv   # Your input data (required)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- A CSV file with your vinyl collection data

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your data**: Ensure you have a CSV file with at least these columns:
   - `Artist`: Main artist name
   - `Album`: Album title
   - `Musicians`: Structured musician data (see format below)
   - `Genres`: Comma-separated genres (optional)
   - `Styles`: Comma-separated styles (optional)

### Usage

**Basic usage**:
```bash
python main.py
```

**With custom input/output files**:
```bash
python main.py --input my-collection.csv --output my-analysis.html
```

**With verbose output and CSV exports**:
```bash
python main.py --verbose --save-csvs
```

**Command line options**:
- `--input, -i`: Input CSV file path (default: `vinyl-collection.csv`)
- `--output, -o`: Output HTML file path (default: `musician_network_complete_analysis.html`)
- `--save-csvs`: Save intermediate CSV files (network data and triples)
- `--verbose, -v`: Enable detailed progress output

## 📊 Data Format

Your CSV file should contain musician data in this format in the `Musicians` column:

```
Musician Name (Role1, Role2); Another Musician (Role3); Third Musician (2) (Role4, Role5)
```

**Examples**:
- `John Coltrane (Tenor Saxophone); McCoy Tyner (Piano); Jimmy Garrison (Bass)`
- `Miles Davis (Trumpet, Leader); Bill Evans (Piano); Paul Chambers (3) (Double Bass)`

**Key points**:
- Musicians separated by semicolons (`;`)
- Roles in parentheses, comma-separated
- Optional numbers for disambiguation: `Name (2) (Roles)`
- Genres and Styles should be comma-separated if provided

## 🎨 Generated Visualizations

The tool creates an interactive HTML file with four main tabs:

### 1. 🌐 Network Tab
- Interactive network graph of all musicians and artists
- Filters for genres, styles, roles, and connection thresholds
- Click nodes for detailed information
- Drag, zoom, and explore connections

### 2. 🏆 Top Musicians Tab
- Bar chart of most active musicians
- Scatter plot showing main artist vs session work
- Detailed musician rankings

### 3. 🎭 Session Musicians Tab
- Focus on musicians who appear on many records but rarely as main artist
- Discover the "hidden gems" of your collection
- Click for detailed album lists

### 4. 🔍 Debug Musician Tab
- Search functionality for specific musicians
- Complete statistics and network verification
- Detailed collaboration information

## ⚙️ Configuration

Modify `config.py` to customize:

- **File paths**: Default input/output locations
- **Analysis parameters**: Session musician thresholds, limits
- **Visualization settings**: Node sizes, colors
- **Feature toggles**: Enable/disable specific functionality

## 🔧 Extending the Analysis

The modular structure makes it easy to extend:

### Adding New Analysis Functions

1. Add functions to `analysis.py`
2. Import and call from `main.py`
3. Optionally add to HTML generation in `html_generator.py`

### Customizing Visualizations

1. Modify HTML template in `html_generator.py`
2. Update JavaScript functions for new interactive features
3. Adjust styling in the CSS section

### Processing Different Data Formats

1. Modify parsing functions in `data_processor.py`
2. Update the `parse_musicians()` function for your format
3. Adjust configuration in `config.py`

## 🐛 Troubleshooting

**Common issues**:

1. **"Input file not found"**: Ensure your CSV file exists and path is correct
2. **"No musicians found"**: Check your Musicians column format matches the expected pattern
3. **Empty visualization**: Verify your data has the required columns
4. **JavaScript errors**: Check browser console for specific error messages

**Debug tips**:
- Use `--verbose` flag to see detailed processing steps
- Use `--save-csvs` to inspect intermediate data files
- Check the Debug Musician tab in the generated HTML

## 📈 Performance Notes

- The tool handles hundreds of musicians and artists efficiently
- Large datasets (1000+ musicians) may take longer to render
- Browser performance depends on network complexity
- Consider filtering for very large networks

## 🎯 Use Cases

- **Music Collection Analysis**: Understand your listening patterns
- **Artist Discovery**: Find new artists through musician connections
- **Session Musician Research**: Identify prolific session players
- **Genre Analysis**: See how musicians cross genre boundaries
- **Collaboration Mapping**: Visualize musical partnerships

## 🤝 Contributing

The modular design welcomes contributions:

1. **Bug reports**: Use the Debug tab to gather information
2. **Feature requests**: Describe your use case
3. **Code contributions**: Follow the existing module structure
4. **Data format support**: Add parsers for different CSV formats

## 📝 License

This project is provided as-is for educational and personal use.

---

**Generated files**:
- `musician_network_complete_analysis.html`: Main interactive visualization
- `musician_network.csv`: Processed network data (if `--save-csvs` used)
- `musician_graph_triples.csv`: Graph triples format (if `--save-csvs` used) 
