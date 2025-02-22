# Moniepoint Analytics Software

## Daniel's DreamDevs Hackathon - Moniepoint Analytics Software

This is a simple analytics software for Moniepoint. It allows you to analyze the sales data of your business.

### Features

- Analyze the sales data of your business.
- Get insights into your business.
- Get the highest sales volume in a day.
- Get the highest sales value in a day.
- Get the most sold product ID by volume.
- Get the highest sales staff ID for each month.
- Get the highest hour of the day by average transaction volume.

### Technologies Used

- Python

## Problem Solving Approach

1. **Understanding the Problem**
   - Analyzed the transaction file format and structure
   - Identified the key metrics needed:
     * Highest sales volume in a day
     * Highest sales value in a day
     * Most sold product ID by volume
     * Highest sales staff ID for each month

2. **Breaking Down the Solution**
   - Created separate functions for each distinct task:
     * `prepare_file()`: Parses individual transaction lines
     * `combine_transaction_products()`: Aggregates product quantities
     * `combine_transaction_sales_amt()`: Collects all sales amounts
     * `combine_staff_sales()`: Tracks staff performance
     * `highest_sales_volume()`: Finds products with maximum sales

3. **Data Processing Strategy**
   - Used dictionaries to efficiently track running totals
   - Implemented file handling with proper reset points
   - Created aggregation functions to combine data across transactions

4. **User Interface Design**
   - Built an interactive menu system for easy access to metrics

5. **Testing and Validation**
   - Tested with sample transaction files


## Future Improvements
- Implement the highest hour by average transaction volume feature


### How to run the software

1. Clone the repository
2. Run the software using the command based on your operating system and python version
   - On Windows: `python main.py`
   - On Linux/MacOS: `python3 main.py`
3. Edit the `directory_path` variable in the `main.py` file to the directory containing the sales data on your local machine.
4. Pls note that the software is designed to work with the sales data in a directory of text files with the following format:
   - salesStaffId
   - transaction time
   - The products sold. (format "[productId1:quantity|productId2:quantity]")
   - sale amount
5. Follow the instructions in the options menu to analyze the sales data.

### How to use the software

1. Select an option from the menu.
2. The software will display the results based on the option you selected.


## Author

This software was developed by Daniel Okpara.




