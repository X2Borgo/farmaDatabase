# farmaDatabase - Pharmacy Inventory Management System

A comprehensive pharmacy inventory management system built with Python and Tkinter, featuring a user-friendly GUI for managing pharmaceutical products, quantities, and pricing information stored in a SQLite database.

## 🚀 Features

- **Interactive GUI Interface**: Clean, intuitive Tkinter-based interface with table view
- **Product Management**: Add new pharmaceutical products with name, price, and quantity
- **Inventory Control**: Modify quantities of existing products with real-time updates
- **Smart Sorting**: Click column headers to sort by product name, price, or quantity
- **Data Persistence**: SQLite database ensures data is saved between sessions
- **Input Validation**: Comprehensive error handling and data validation
- **Pre-loaded Data**: Comes with 31 common pharmaceutical products
- **Visual Feedback**: Refresh button with icon and intuitive dialog boxes

## 🏗️ Architecture

The application follows a modular architecture with clear separation of concerns:

### **Database Layer (`database/`)**
- **DatabaseManager**: Centralized database operations with connection management
- **Transaction Safety**: Automatic commit/rollback handling
- **Query Abstraction**: Clean API for common database operations

### **GUI Layer (`gui/`)**  
- **MainWindow**: Primary application interface with table management
- **Dialog System**: Modular dialogs for add/modify operations
- **Component Separation**: UI logic separated from business logic

### **Data Layer (`data/`)**
- **Sample Data**: Pre-defined pharmaceutical inventory
- **Structured Format**: Consistent data format for easy extension

### **Utilities (`utils/`)**
- **Validation**: Comprehensive input validation with error handling
- **GUI Helpers**: Reusable UI component creation functions
- **Type Safety**: Strong typing for better code reliability

### **Benefits of This Architecture**
- **Maintainability**: Each module has a single responsibility
- **Testability**: Components can be tested independently  
- **Extensibility**: Easy to add new features without affecting existing code
- **Code Reuse**: Common functionality extracted into utilities

## 📋 Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux with GUI support
- **Dependencies**:
  - `tkinter` (usually included with Python)
  - `pandas` 
  - `sqlite3` (included with Python)

## 🛠️ Installation

### Method 1: Using Conda (Recommended)
```bash
# Clone the repository
git clone https://github.com/X2Borgo/farmaDatabase.git
cd farmaDatabase

# Create and activate environment, install dependencies, and run
make run
```

### Method 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/X2Borgo/farmaDatabase.git
cd farmaDatabase

# Install dependencies
pip install pandas

# Run the application
python main.py
```

### Method 3: Using Virtual Environment
```bash
# Clone the repository
git clone https://github.com/X2Borgo/farmaDatabase.git
cd farmaDatabase

# Create virtual environment
python -m venv farmaEnv
source farmaEnv/bin/activate  # On Windows: farmaEnv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🎮 Usage

### Starting the Application
Run `python main.py` to launch the pharmacy inventory system. The main window will display:

- A table showing all pharmaceutical products
- Control buttons: Refresh (🔄), Add Drug, and Modify Quantity
- Sortable columns (click headers to sort)

### Adding New Products
1. Click the **"Add Drug"** button
2. Fill in the product information:
   - **Drug Name**: Name of the pharmaceutical product
   - **Price**: Cost in dollars (must be positive)
   - **Quantity**: Number of units in inventory (must be non-negative)
3. Click **"Save"** to add the product or **"Cancel"** to abort

### Modifying Quantities
1. Click the **"Modify Quantity"** button
2. Select a drug from the dropdown menu
3. View the current quantity (displayed automatically)
4. Enter the new quantity in the text field
5. Click **"Save"** to update or **"Cancel"** to abort

### Sorting and Navigation
- Click any column header to sort the table
- Click the same header again to reverse the sort order
- Use the refresh button (🔄) to reload data from the database
- Press **Escape** to close the application

## 📁 Project Structure

```
farmaDatabase/
├── main.py                      # Application entry point
├── classes.py                   # Product data model class
├── database/
│   ├── __init__.py
│   └── db_manager.py           # Database operations and management
├── gui/
│   ├── __init__.py
│   ├── main_window.py          # Main application window
│   └── dialogs.py              # Add/modify product dialogs
├── data/
│   ├── __init__.py
│   └── sample_data.py          # Sample pharmaceutical products
├── utils/
│   ├── __init__.py
│   ├── validation.py           # Input validation utilities
│   ├── gui_helpers.py          # GUI utility functions
│   └── config.py               # Application configuration settings
├── requirements.txt             # Python dependencies
├── Makefile                     # Build automation with conda
├── demo_gui_simulation.py       # Text-based feature demonstration
├── icons/
│   └── refresh-button.png       # GUI icon assets
├── test_*.py                    # Test files for various features
├── .gitignore                   # Git ignore rules
└── README.md                    # Project documentation
```

### Key Modules Description

- **`main.py`**: Application entry point that initializes components and starts the GUI
- **`classes.py`**: Simple Product data model class
- **`database/db_manager.py`**: DatabaseManager class handling all SQLite operations
- **`gui/main_window.py`**: MainWindow class for the primary application interface
- **`gui/dialogs.py`**: Dialog classes for adding products and modifying quantities
- **`data/sample_data.py`**: Pre-defined pharmaceutical products for database initialization
- **`utils/validation.py`**: Input validation functions for form data
- **`utils/gui_helpers.py`**: Utility functions for consistent GUI component creation
- **`utils/config.py`**: Centralized application configuration and constants

## 🧪 Development & Testing

### Running Tests
```bash
# Run basic tests (requires GUI environment)
make test

# Or run individual test files
python test_sorting.py
python test_quantity_modification.py

# Run new integration tests for refactored code
python test_refactored_integration.py
```

### Available Make Commands
```bash
make run     # Create environment, install deps, and run
make req     # Install requirements only
make test    # Run tests
make clean   # Remove virtual environment
make val     # Run with valgrind (for memory debugging)
```

### GUI Simulation Demo
To see a text-based demonstration of the application features without running the GUI:
```bash
python demo_gui_simulation.py
```

## 💊 Sample Data

The application comes pre-loaded with 31 pharmaceutical products including:
- Common medications (Lisinopril, Metformin, Omeprazole)
- Supplements (Vitamin D3, Multivitamin, Calcium Carbonate)
- Over-the-counter drugs (Acetaminophen, Ibuprofen, Aspirin)
- Antibiotics (Amoxicillin, Azithromycin, Ciprofloxacin)

## 🎯 Use Cases

- **Pharmacy Management**: Track inventory levels and pricing for pharmaceutical products
- **Educational Tool**: Learn database operations and GUI development with Python
- **Inventory Tracking**: Monitor stock levels and update quantities as needed
- **Price Management**: Maintain current pricing information for all products

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is available for educational and personal use. Please check with the repository owner for commercial use permissions.

## 🛡️ Data Privacy

- All data is stored locally in SQLite database files
- No external connections or data transmission
- Database files are excluded from version control (`.gitignore`)

## 🐛 Troubleshooting

**Common Issues:**
- **"No module named 'tkinter'"**: Install tkinter or use a Python distribution that includes it
- **"No module named 'pandas'"**: Run `pip install pandas`
- **Database errors**: Ensure write permissions in the application directory
- **GUI not displaying**: Verify you're running in an environment with GUI support