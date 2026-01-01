#Product Scraper

This Python project scrapes product information from Ecommerence web pages. It extracts product names and prices from web pages and saves the data into an Excel file using `pandas`.

---

## Step 1: Install Required Libraries

Make sure you have Python 3.8 or higher installed.  
Then install the necessary libraries:

```bash
pip install requests beautifulsoup4 pandas
requests – for sending HTTP requests to web pages

beautifulsoup4 – for parsing HTML and extracting information

pandas – for storing and exporting data into Excel

Step 2: Run the Script
Run your Python script in the terminal:

bash
Copy code
python your_script_name.py
The script will:

Collect all product pages in the category.

Extract product names and prices from each page.

Save the data into an Excel file in the same folder, e.g.,

css
Copy code
CityMall_YYYY-MM-DD-HH-MM-SS.xlsx
Step 3: Output
The resulting Excel file contains:

Product Name	Product Price
Example 1	2500
Example 2	4000

Notes
Use responsibly: do not overload the website with too many requests.

This project is for educational purposes only.
