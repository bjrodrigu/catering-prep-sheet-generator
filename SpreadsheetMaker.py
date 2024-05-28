import pandas as pd
import openpyxl
from openpyxl.styles import Alignment, PatternFill, Border, Side
 

# Create a new workbook and select the active sheet
workbook = openpyxl.Workbook()
sheet = workbook.active

# Define placeholder values
quantities = [""] + [0] * 14 # placeholder value
trays_of_15 = 0 # placeholder value
total_extra_trays = 0 # placeholder value
total_pickles = 0 # placeholder value
num_of_gh_wraps = 0 # placeholder value
num_of_gh_wraps_packs = 0 # placeholder value
num_of_flour_wraps = 0 # placeholder value
num_of_flour_wraps_packs = 0 # placeholder value
projection = 0 # placeholder value
projection_with_catering = 0 # placeholder value

# Define sandwich totals, with placeholder values MUST CHANGE TO ACTUAL VALUES USING THE DATA FROM THE RECEIPT
sandwich_totals = [
    ["What are the sandwiches", 1, 0],
    ["", 2, 0],
    ["", 3, 0],
    ["", 4, 0],
    ["", 5, 0],
    ["", 6, 0],
    ["", 7, 0],
    ["", 8, 0],
    ["", 9, 0],
    ["", 10, 0],
    ["", 11, 0],
    ["", 12, 0],
    ["", 13, 0],
    ["", 14, 0],
    ["", 15, 0],
    ["", 16, 0],
    ["", 17, 0],
    ["", "BLT", 0],
    ["", "Caesar", 0],
    ["", "Jal Ranch", 0],
    ["", "Tuscan", 0],
    ["", "LTO Sandwich/Wrap", 0],
    []
]

# Define the data to be added to the sheet
data = [
    ["List Each Order and it's time starting with the earliest"],
    ["Total Quantities:", "Little Johns", "Wraps", "Sandwiches", "Giants", "30 Piece", "Box Lunches", "12 Pack", "18 Pack", "Wrap Box", "Small Bundle", "Large Bundle", "Drink Bundle", "Dessert Bundle", "Chip Bundle"],
    quantities,
    [],
    ["Trays of 15 for little johns", trays_of_15],
    ["Lay out extra trays of bread", total_extra_trays, "", "Pickles to slice for Box Lunch", total_pickles],
    ["Number of G/H wraps needed", num_of_gh_wraps, "", "G/H Wrap packs needed for order", num_of_gh_wraps_packs],
    ["Number of Flour wraps needed", num_of_flour_wraps, "", "Flour Wrap packs needed for order", num_of_flour_wraps_packs],
    ["Projection for shift w/out catering", projection],
    ["New projection with catering", projection_with_catering],
    [],
]



# Add main data to the sheet
for row in data:
    sheet.append(row)

# Add sandwich totals to the sheet
for row in sandwich_totals:
    sheet.append(row)

# Totals for slicing prep
# 0's HARDCODED CURRENTLY, WILL CHANGE TO VARIABLES WITH ACTUAL VALUES
sheet['E12'] = "Cheese"
sheet['F12'] = 0 
sheet['E13'] = "Ham"
sheet['F13'] = 0
sheet['E14'] = "Turkey"
sheet['F14'] = 0
sheet['E15'] = "Beef"
sheet['F15'] = 0
sheet['E16'] = "Vito"
sheet['F16'] = 0
sheet['E17'] = "Tuna"
sheet['F17'] = 0
sheet['E18'] = "Bacon Packs"
sheet['F18'] = 0
sheet['E19'] = "Chicken"
sheet['F19'] = 0

sheet['H11'] = "Slice extra packs"
sheet['H12'] = 0.00
sheet['H13'] = 0.00
sheet['H14'] = 0.00
sheet['H15'] = 0.00
sheet['H16'] = 0.00
sheet['H17'] = 0.00
sheet['H18'] = "# of Chicken bins needed"
sheet['H19'] = 0


# Total sides for catering

sheet['H20'] = "Amount of Sides Needed (Full Boxes)"
sheet['G21'] = "Reg"
sheet['H21'] = 0
sheet['G22'] = "BBQ"
sheet['H22'] = 0
sheet['G23'] = "Jal"
sheet['H23'] = 0
sheet['G24'] = "S/V"
sheet['H24'] = 0
sheet['G25'] = "Thinny"
sheet['H25'] = 0
sheet['G26'] = "CC"
sheet['H26'] = 0
sheet['G27'] = "OR"
sheet['H27'] = 0
sheet['G28'] = "Pickles"
sheet['H28'] = 0
sheet['G29'] = "Brownies"
sheet['H29'] = 0
sheet['G30'] = "Pasta Salad"
sheet['H30'] = 0
sheet['G31'] = "Potato Salad"
sheet['H31'] = 0

sides_section = [ 
    ['', '', 'Reg Chips', 'BBQ Chips', 'Jal Chips', 'S/V Chips', 'Thinny', 'CC Cookies', 'OR Cookies', 'Brownies', 'Pickle Buckets' 'Pasta Sm.', 'Pasta Lg.', 'Potato Sm.', 'Potato Lg.', 'LTO Cookies'],
    ["How many sides do you need?", ''] + [0] * 13,
    ["(Includes what's needed for box lunches)"],
    [],
    ['', '30 pc. Boxes', '18 pc. Boxes', 'Box Lunches', '12 Packs', 'Dasani', 'Coke Bottles', 'D/C Bottles', 'Sprite Bottles', 'G/H Wraps', 'Flour Wraps'],
    ['Do we have enough?']
]

for row in sides_section:
    sheet.append(row)

# Define the range of cells to highlight
highlight_ranges = ["B1:V1", "B3:O3", "B5:B10", "E6:E8", "C12:C33", "F12:F19", "H12:H17", "H19:H19", "H21:H31", "C36:O36", "B40:K40"]

# Set the fill color to orange
fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")

# Set the border style
border = Border(left=Side(style='thin', color='000000'),
                right=Side(style='thin', color='000000'),
                top=Side(style='thin', color='000000'),
                bottom=Side(style='thin', color='000000'))

# Apply the fill color to the range of cells
for highlight_range in highlight_ranges:
    for row in sheet[highlight_range]:
        for cell in row:
            cell.fill = fill
            cell.border = border

# Adjust column widths to fit the content
for column_cells in sheet.columns:
    max_length = 0
    column = column_cells[0].column_letter  # Get the column letter
    for cell in column_cells:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2) 
    sheet.column_dimensions[column].width = adjusted_width

final_questions_section = [
    [],
    ["What time is the opener starting?", ""],
    ["How many trays are needed to complete the order? By what time does this bread need to be out?", ""],
    ["Do we need to bake bread at another location to complete the order on time?", ""],
    ["Do we need extra workers to execute this order? Who have we called? Who is making the food?", ""],
    ["How much extra meat and cheese do we need to slice?", ""],
    ["Do we need extra parm cheese prepped? What about avo, LTO skus, chicken?", ""],
    ["Do we need to order extra produce?", ""],
    ["Do we need to get any additional sides to complete the order?", ""],
    ["Does the order need mayo/mustard packets? Do you have enough?", ""],
    ["Email the completed spreadsheet to your boss once completed."]
]

for row in final_questions_section:
    sheet.append(row)

for row in sheet.iter_rows():
    for cell in row:
        cell.alignment = Alignment(horizontal='left')

# Save the workbook to a file
workbook.save("catering_execution_sheet.xlsx")

# Print a success message
print("Excel file created successfully!")
