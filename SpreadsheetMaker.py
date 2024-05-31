import pandas as pd
import openpyxl
from openpyxl.styles import Alignment, PatternFill, Border, Side
from Organizer import process_receipt, read_ocr_output
from ReceiptScanner import main as receipt_scanner

boxes = {
    "30Pc Party Box": {"count": 0},
    "18Pc PartyBox": {"count": 0},
    "12 pack": {"count": 0},
    "Wrapbox": {"count": 0},
    "(Box)": {"count": 0}
}

side_counts = {
    "Regular": {"count": 0},
    "BBQ": {"count": 0},
    "Jalapeno": {"count": 0},
    "S&V": {"count": 0},
    "Thinny": {"count": 0},
    "PotSalad": {"count": 0},
    "PastaSalad": {"count": 0},
    "PotSalad(LG)": {"count": 0},
    "PastaSalad(LG)": {"count": 0},
    "Pickle Bucket": {"count": 0},
    "Chocolatechip": {"count": 0},
    "Oatmealrasin": {"count": 0},
    "Brownie": {"count": 0}
}

sandwiches = {
    "#1 Pepe": {"count": 0, "cheese": 1, "ham": 1},
    "#2 Big John": {"count": 0, "roast beef": 1},
    "#3 Totally Tuna": {"count": 0, "tuna": 1},
    "#4 Turkey Tom": {"count": 0, "turkey": 1},
    "#5 Vito": {"count": 0, "cheese": 1, "vito": 1},
    "#6 The Veggie": {"count": 0, "cheese": 2},
    "J.J. BLT": {"count": 0, "bacon": 6},
    "#7 Spicy Italian": {"count": 0, "cheese": 1, "vito": 2},
    "#8 Billy Club": {"count": 0, "cheese": 1, "ham": 1, "roast beef": 1},
    "#9 Italian Night Club": {"count": 0, "cheese": 1, "ham": 1, "vito": 1},
    "#10 Hunters Club": {"count": 0, "cheese": 1, "roast beef": 2},
    "#11 Country Club": {"count": 0, "cheese": 1, "ham": 1, "turkey": 1},
    "#12 Beach Club": {"count": 0, "cheese": 2, "turkey": 1},
    "#13 Jimmy Cubano": {"count": 0, "cheese": 1, "ham": 1, "bacon": 4},
    "#14 Bootleger": {"count": 0, "turkey": 1, "roast beef": 1},
    "#15 Club Tuna": {"count": 0, "cheese": 2, "tuna": 1},
    "#16 Club Lulu": {"count": 0, "turkey": 1, "bacon": 3},
    "#17 Ultimate Porker": {"count": 0, "ham": 1, "bacon": 3},
    "J.J. Garganutan": {"count": 0, "cheese": 1, "ham": 1, "roast beef": 1, "turkey": 1, "vito": 1}
}

wraps = {
    "Chicken Ceaser": {"count": 0, "chicken": 1},
    "Jalapeno Ranch": {"count": 0, "cheese": 1, "chicken": 1},
    "Tuscan Italian": {"count": 0, "vito": 1, "ham": 1}
}

portions_per_pack = {
    "cheese": 60,
    "vito": 25,
    "roast beef": 30,
    "turkey": 25,
    "ham": 25,
    "chicken": 7,
    "bacon": 150,
    "tuna": 25,
    "garlic herb wrap": 12,
    "flour wrap": 12
}

items_per_box = {
    "Regular": 72,
    "BBQ": 72,
    "Jalapeno": 72,
    "S&V": 72,
    "Thinny": 72,
    "Chocolate Chip": 56,
    "Oatmeal Rasin": 56,
    "Brownies": 42,
    "pasta salad": 2041.17,
    "potato salad": 3628.74,
    "Pickles": 60
}



def create_spreadsheet():
    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Define placeholder values
    quantities = [""] + [0] * 14 # placeholder value
    trays_of_15 = 0 # placeholder value
    total_extra_trays = 0 # placeholder value
    total_pickles = 0 # placeholder value
    num_of_gh_wraps = 0 # placeholder value
    num_of_flour_wraps = 0 # placeholder value
    projection = 0 # placeholder value
    projection_with_catering = 0 # placeholder value

    # Define sandwich totals
    sandwich_totals = [
        ["What are the sandwiches", 1, sandwiches["#1 Pepe"]["count"]],
        ["", 2, sandwiches["#2 Big John"]["count"]],
        ["", 3, sandwiches["#3 Totally Tuna"]["count"]],
        ["", 4, sandwiches["#4 Turkey Tom"]["count"]],
        ["", 5, sandwiches["#5 Vito"]["count"]],
        ["", 6, sandwiches["#6 The Veggie"]["count"]],
        ["", 7, sandwiches["#7 Spicy Italian"]["count"]],
        ["", 8, sandwiches["#8 Billy Club"]["count"]],
        ["", 9, sandwiches["#9 Italian Night Club"]["count"]],
        ["", 10, sandwiches["#10 Hunters Club"]["count"]],
        ["", 11, sandwiches["#11 Country Club"]["count"]],
        ["", 12, sandwiches["#12 Beach Club"]["count"]],
        ["", 13, sandwiches["#13 Jimmy Cubano"]["count"]],
        ["", 14, sandwiches["#14 Bootleger"]["count"]],
        ["", 15, sandwiches["#15 Club Tuna"]["count"]],
        ["", 16, sandwiches["#16 Club Lulu"]["count"]],
        ["", 17, sandwiches["#17 Ultimate Porker"]["count"]],
        ["", "BLT", sandwiches["J.J. BLT"]["count"]],
        ["", "Caesar", wraps["Chicken Ceaser"]["count"]],
        ["", "Jal Ranch", wraps["Jalapeno Ranch"]["count"]],
        ["", "Tuscan", wraps["Tuscan Italian"]["count"]],
        ["", "LTO Sandwich/Wrap", 0]
        ]

    # Define the data to be added to the sheet
    data = [
        ["List Each Order and it's time starting with the earliest"],
        ["Total Quantities:", "Little Johns", "Wraps", "Sandwiches", "Giants", "30 Piece", "Box Lunches", "12 Pack", "18 Pack", "Wrap Box", "Small Bundle", "Large Bundle", "Drink Bundle", "Dessert Bundle", "Chip Bundle"],
        quantities,
        [],
        ["Trays of 15 for little johns", trays_of_15],
        ["Lay out extra trays of bread", total_extra_trays, "", "Pickles to slice for Box Lunch", total_pickles],
        ["Number of G/H wraps needed", num_of_gh_wraps, "", "G/H Wrap packs needed for order", num_of_gh_wraps / portions_per_pack["garlic herb wrap"]],
        ["Number of Flour wraps needed", num_of_flour_wraps, "", "Flour Wrap packs needed for order", num_of_flour_wraps / portions_per_pack["flour wrap"]],
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
    sheet['E12'] = "Cheese"
    cheese_total = sum(sandwiches[sandwich].get("cheese", 0) * sandwiches[sandwich]["count"] for sandwich in sandwiches) + sum(wraps[wrap].get("cheese", 0) * wraps[wrap]["count"] for wrap in wraps)
    sheet['F12'] = cheese_total

    sheet['E13'] = "Ham"
    ham_total = sum(sandwiches[sandwich].get("ham", 0) * sandwiches[sandwich]["count"] for sandwich in sandwiches) + sum(wraps[wrap].get("ham", 0) * wraps[wrap]["count"] for wrap in wraps)
    sheet['F13'] = ham_total

    sheet['E14'] = "Turkey"
    turkey_total = sum(sandwiches[sandwich].get("turkey", 0) * sandwiches[sandwich]["count"] for sandwich in sandwiches)
    sheet['F14'] = turkey_total

    sheet['E15'] = "Beef"
    beef_total = sum(sandwiches[sandwich].get("roast beef", 0) * sandwiches[sandwich]["count"] for sandwich in sandwiches)
    sheet['F15'] = beef_total

    sheet['E16'] = "Vito"
    vito_total = sum(sandwiches[sandwich].get("vito", 0) * sandwiches[sandwich]["count"] for sandwich in sandwiches) + sum(wraps[wrap].get("vito", 0) * wraps[wrap]["count"] for wrap in wraps)
    sheet['F16'] = vito_total

    sheet['E17'] = "Tuna"
    tuna_total = sum(sandwiches[sandwich].get("tuna", 0) * sandwiches[sandwich]["count"] for sandwich in sandwiches)
    sheet['F17'] = tuna_total

    sheet['E18'] = "Bacon Packs"
    bacon_total = sum(sandwiches[sandwich].get("bacon", 0) * sandwiches[sandwich]["count"] for sandwich in sandwiches) / portions_per_pack["bacon"]
    sheet['F18'] = bacon_total

    sheet['E19'] = "Chicken"
    chicken_total = sum(wraps[wrap].get("chicken", 0) * wraps[wrap]["count"] for wrap in wraps)
    sheet['F19'] = chicken_total

    sheet['H11'] = "Slice extra packs"
    sheet['H12'] = round(chicken_total / portions_per_pack["chicken"], 2)
    sheet['H13'] = round(ham_total / portions_per_pack["ham"], 2)
    sheet['H14'] = round(turkey_total / portions_per_pack["turkey"], 2)
    sheet['H15'] = round(beef_total / portions_per_pack["roast beef"], 2)
    sheet['H16'] = round(vito_total / portions_per_pack["vito"], 2)
    sheet['H17'] = round(tuna_total / portions_per_pack["tuna"], 2)
    sheet['H18'] = "# of Chicken bins needed"
    sheet['H19'] = round(chicken_total / portions_per_pack["chicken"], 2)


    # Total sides for catering
    sheet['H20'] = "Amount of Sides Needed (Full Boxes)"
    sheet['G21'] = "Reg"
    sheet['H21'] = round(side_counts["Regular"]["count"] / items_per_box["Regular"], 2)
    sheet['G22'] = "BBQ"
    sheet['H22'] = round(side_counts["BBQ"]["count"] / items_per_box["BBQ"], 2)
    sheet['G23'] = "Jal"
    sheet['H23'] = round(side_counts["Jalapeno"]["count"] / items_per_box["Jalapeno"], 2)
    sheet['G24'] = "S/V"
    sheet['H24'] = round(side_counts["S&V"]["count"] / items_per_box["S&V"], 2)
    sheet['G25'] = "Thinny"
    sheet['H25'] = round(side_counts["Thinny"]["count"] / items_per_box["Thinny"], 2)
    sheet['G26'] = "CC"
    sheet['H26'] = round(side_counts["Chocolatechip"]["count"] / items_per_box["Chocolate Chip"], 2)
    sheet['G27'] = "OR"
    sheet['H27'] = round(side_counts["Oatmealrasin"]["count"] / items_per_box["Oatmeal Rasin"], 2)
    sheet['G28'] = "Pickles"
    sheet['H28'] = round(side_counts["Pickle Bucket"]["count"] / items_per_box["Pickles"], 2)
    sheet['G29'] = "Brownies"
    sheet['H29'] = round(side_counts["Brownie"]["count"] / items_per_box["Brownies"], 2)
    sheet['G30'] = "Pasta Salad"
    sheet['H30'] = round(side_counts["PastaSalad"]["count"] / items_per_box["pasta salad"], 2)
    sheet['G31'] = "Potato Salad"
    sheet['H31'] = round(side_counts["PotSalad"]["count"] / items_per_box["potato salad"], 2)

    sides_section = [ 
        ['', '', 'Reg Chips', 'BBQ Chips', 'Jal Chips', 'S/V Chips', 'Thinny', 'CC Cookies', 'OR Cookies', 'Brownies', 'Pickle Buckets', 'Pasta Sm.', 'Pasta Lg.', 'Potato Sm.', 'Potato Lg.'],
        ["How many sides do you need?", '', side_counts["Regular"]["count"], side_counts["BBQ"]["count"], side_counts["Jalapeno"]["count"], side_counts["S&V"]["count"], side_counts["Thinny"]["count"], side_counts["Chocolatechip"]["count"], side_counts["Oatmealrasin"]["count"], side_counts["Brownie"]["count"], side_counts["Pickle Bucket"]["count"], side_counts["PastaSalad"]["count"], side_counts["PastaSalad(LG)"]["count"], side_counts["PotSalad"]["count"], side_counts["PotSalad(LG)"]["count"]],
        ["(Includes what's needed for box lunches)"],
        [],
        ['', '30 pc. Boxes', '18 pc. Boxes', 'Box Lunches', '12 Packs', 'Dasani', 'Coke Bottles', 'D/C Bottles', 'Sprite Bottles', 'G/H Wraps', 'Flour Wraps'],
        ['Do we have enough?']
    ]

    for row in sides_section:
        sheet.append(row)

    # Define the range of cells to highlight
    highlight_ranges = ["B1:V1", "B3:O3", "B5:B10", "E6:E8", "C12:C33", "F12:F19", "H12:H17", "H19:H19", "H21:H31", "C35:O35", "B39:K39"]

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

def main():
    receipt_scanner()
     # Assuming the input file was "Receipt2_processed.txt"
    output_file = "Receipt2_processed.txt"
    ocr_text = read_ocr_output(output_file)
    # Call the function to process the receipt
    process_receipt(ocr_text, boxes)
    process_receipt(ocr_text, sandwiches)
    process_receipt(ocr_text, wraps)
    process_receipt(ocr_text, side_counts)

    create_spreadsheet()

if __name__ == "__main__":
    main()
