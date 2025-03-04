```markdown
# Auto Tax Statement Processor

This repository contains a Python script designed to automatically process CSV statements of financial transactions, classify them into income and expenses, and generate a comprehensive Markdown report. This tool is especially useful for individuals struggling with the manual work of classifying transactions for tax filing purposes.

## Features

- **Robust CSV Parsing:**  
  Handles CSV files with inconsistent field counts by using the `on_bad_lines` parameter to discard or truncate malformed rows.

- **Data Processing & Classification:**  
  - Converts date fields to proper datetime objects.
  - Classifies transactions by type (e.g., Payment, Deposit, Authorization).
  - Aggregates monthly net amounts.
  - Groups and summarizes income (transactions with positive amounts) and expenses (transactions with negative amounts) by company.

- **Markdown Report Generation:**  
  Automatically creates a detailed Markdown report that includes:
  - A summary of the overall transaction period and count.
  - Transaction counts grouped by type.
  - Monthly net totals.
  - Detailed tables for income and expenses by company.

## Requirements

- Python 3.x
- [pandas](https://pandas.pydata.org/)  
- [tkinter](https://docs.python.org/3/library/tkinter.html) (usually comes pre-installed with Python)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies:**

   Install the required Python packages using pip:

   ```bash
   pip install pandas
   ```

## Usage

1. **Run the Script:**

   Execute the main script (e.g., `finance-report-gen.py`):

   ```bash
   python finance-report-gen.py
   ```

2. **Select Your CSV File:**

   A file dialog will open. Select the CSV file that contains your financial statement.

3. **Review the Generated Report:**

   The script will process the file and generate a Markdown report in the same directory as the CSV file. The report file is named with the original file's base name and the suffix `_reporte.md` (e.g., `your_statement_reporte.md`).

## How It Works

- **CSV Loading and Cleanup:**  
  The script reads the CSV file and manages rows with extra fields by truncating them to the expected number of columns.

- **Data Conversion:**  
  It converts the `Date` column to datetime format and ensures numerical fields (like `Gross` and `Net`) are correctly formatted for calculations.

- **Classification and Aggregation:**  
  - **Transactions by Type:** Groups and counts transactions based on their description.
  - **Monthly Net Totals:** Aggregates the net transaction amounts for each month.
  - **Income and Expenses by Company:** Filters transactions where `Gross` is positive (income) or negative (expenses) and groups them by company name, summarizing the totals.

- **Report Generation:**  
  The script compiles all the processed information into a Markdown formatted report that is easy to read and share.

## Contributing

Contributions, bug fixes, and enhancements are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This tool is provided "as-is" for informational purposes only and is not intended to replace professional tax advice. Users should consult a tax professional regarding their specific tax situations.
```
