import re
import math
import os
from datetime import datetime

#Create dictonaries(hashmaps) of the items that need to be counted 
boxes = {
    "30Pc Party Box":{"count":0},   "18Pc Party Box":{"count":0},   "12 Half Sandwiches":{"count":0},
    "12 Half Wraps":{"count":0}, "(Box)":{"count":0}, "Bottled Drink Bundle":{"count":0},"Chips Bundle":{"count":0},
    "Desserts Bundle":{"count":0},"GIANT":{"count":0},"Lil John":{"count":0}
}

side_counts ={
    "Regular Chips" :{"count":0},   "BBQ Chips":{"count":0},    "Jalapeno Chips":{"count":0},   "Salt Vin Chips":{"count":0},"Thinny Chips":{"count":0},
    "PotSalad":{"count":0},   "PastaSalad":{"count":0},     "PotSalad (LG)":{"count":0},   "PastaSalad (LG)":{"count":0}, "Pickles":{"count":0},
    "Pickle Bucket":{"count":0},"Choc Chip Cookie":{"count":0},  "Oatmeal Rasin Cookie":{"count":0},   "Fudge Choc Brownie":{"count":0},
    "Coke(Bottle)":{"count":0},"Sprite(Bottle)":{"count":0},"Diet Coke(Bottle)":{"count":0}
}
    #the layout for the dic is sandwich name{Num of sandwiches, portion need to make the sandwiches after that}
sandwiches={
    "Slim 1":{"count":0,"cheese":1,"ham":1}, "Slim 2":{"count":0,"roast beef":1},"Slim 3":{"count":0,"tuna":1},
    "Slim 4":{"count":0,"turkey":1}, "Slim 5":{"count":0,"cheese":1,"vito":1},"Slim 6":{"count":0,"cheese":2},"Slim Bacon":{"count":0,"bacon":6},
    "#1 Pepe": {"count":0,"cheese":1, "ham":1}, "#2 Big John":{"count":0,"roast beef":1},
    "#3 Totally Tuna":{"count":0,"tuna":1}, "#4 Turkey Tom":{"count":0,"turkey":1},
    "#5 Vito":{"count":0,"cheese":1,"vito":1},"#6 The Veggie":{"count":0,"cheese":2},"J.J. BLT":{"count":0,"bacon":6},
    "#7 Spicy Italian":{"count":0,"cheese":1,"vito":2},"#8 Billy Club":{"count":0,"cheese":1,"ham":1,"roast beef":1},
    "#9 Italian Club":{"count":0,"cheese":1,"ham":1,"vito":1},"#10 Hunters Club":{"count":0,"cheese":1,"roast beef":2},
    "#11 Country Club":{"count":0,"cheese":1,"ham":1,"turkey":1},"#12 Beach Club":{"count":0,"cheese":2,"turkey":1},
    "#13 Jimmy Cubano":{"count":0,"cheese":1,"ham":1,"bacon":4},"#14 Bootlegger":{"count":0,"turkey":1,"roast beef":1},
    "#15 Club Tuna":{"count":0,"cheese":2,"tuna":1},"#16 Club Lulu":{"count":0,"turkey":1,"bacon":3},
    "#17 Ultimate Porker":{"count":0,"ham":1,"bacon":3},
    "J.J. Garganutan":{"count":0,"cheese":1,"ham":1,"roast beef":1,"turkey":1,"vito":1}    
}
wraps={
    "Chicken Caesar":{"count":0,"chicken":1,"garlic herb wrap":1},"Jalapeno Ranch":{"count":0,"cheese":1,"chicken":1,"flour wrap":1},
    "Tuscan Italian":{"count":0,"vito":1,"ham":1,"galric herb wrap":1}   
}
alternate_names ={
    "#9 Italian": "#9 Italian Club",
    "#10 Hunter's": "#10 Hunters Club",
    "#11 Country":"#11 Country Club",
    "#17 Ultimate P":"#17 Ultimate Porker",
    "JJ Garganutan":"J.J. Garganutan",
    "CCW":"Chicken Caesar",
    "JRW":"Jalapeno Ranch",
    "TIW":"Tuscan Italian",
    "Chocolate Chip Cookie":"Choc Chip Cookie",
    "Wrap Box":"12 Half Wraps"
}

portions_per_pack={
    "cheese":60, "vito":25,"roast beef":30, "turkey":25,"ham":25,"chicken":7,"bacon":150,"garlic herb wrap":12,"flour wrap":12
}
items_per_box={
    "Regular":72,   "BBQ":72,    "Jalapeno":72,   "S&V":72, "Thinny":72,"Pickles":60
    ,"Chocolate Chip":56,"Oatmeal Rasin":56,"Brownies":42,"pasta salad":2041.17,"potato salad":2267.96
}
total_grams={
    "PotSalad":142.0,   "PastaSalad":113.0,     "PotSalad(LG)":851,   "PastaSalad(LG)":680
}


def process_receipt(receipt, dictionary):
    total_portions={}
    total_packs={}
    total_containers={}

    ready_time = None
    
    for item, info in dictionary.items():
        count = 0
        occurrences = re.findall(re.escape(item), receipt, re.IGNORECASE)
        count = len(occurrences)
        
        for alt_name, primary_name in alternate_names.items():
            if primary_name == item:
                occurrences = re.findall(re.escape(alt_name), receipt, re.IGNORECASE)
                count += len(occurrences)
                
        info["count"] += count
    
    if dictionary is boxes:
        extract_box_quantities(receipt,boxes)
        ready_time = find_ready_time(receipt)
        
    if dictionary is side_counts:
        extract_dessert_quantities(receipt, side_counts)
        extract_chip_quantities(receipt,side_counts)
        extract_pickle_quantities(receipt, side_counts)
    
    if dictionary is sandwiches:
        extract_sandwich_quantities(receipt,sandwiches)

    if dictionary is wraps:
        extract_wrap_quantities(receipt,wraps)
    
    # Iterate through each sandwich
    for item, info in dictionary.items():
        count = info["count"]  # Get the count of this sandwich

        # Iterate through each ingredient in the sandwich
        for ingredient, portions in info.items():
            if ingredient != "count":  # Skip the "count" key
                # Calculate the total portions of this ingredient required
                total_portions[ingredient] = total_portions.get(ingredient, 0) + portions * count
                
     # Calculate the total containers of sides used
    for item, portions in total_portions.items():
        if item in items_per_box:
            items_per_box_item = items_per_box[item]
            containers_used = portions / items_per_box_item
            total_containers[item] = round(containers_used, 2)
            # Calculate total grams of potato and pasta salad used
    if dictionary is side_counts:
        total_potato_salad_grams = (side_counts["PotSalad"]["count"] * total_grams["PotSalad"] +
                                    side_counts["PotSalad(LG)"]["count"] * total_grams["PotSalad(LG)"])
        total_pasta_salad_grams = (side_counts["PastaSalad"]["count"] * total_grams["PastaSalad"] +
                                side_counts["PastaSalad(LG)"]["count"] * total_grams["PastaSalad(LG)"])
        
        # Calculate the number of full containers needed for potato and pasta salad
        potato_salad_container_size = items_per_box["potato salad"]
        pasta_salad_container_size = items_per_box["pasta salad"]
        
        potato_salad_containers_needed = total_potato_salad_grams / potato_salad_container_size
        pasta_salad_containers_needed = total_pasta_salad_grams / pasta_salad_container_size
        
        total_containers["PotSalad"] = round(potato_salad_containers_needed, 2)
        total_containers["PastaSalad"] = round(pasta_salad_containers_needed, 2)
         

    
    processed_data = {
        "counts": dictionary,
        "total_portions": total_portions,
        "total_containers": total_containers,
        "ready_time":ready_time
    }
    
    return processed_data

def extract_box_quantities(text,boxes):
    # Define a list of possible party box names
    party_box_names = [
        "30Pc Party Box", "18Pc Party Box", "12 Half Sandwiches", "Wrap Box"
    ]
    
    # Join the party box names into a single string separated by '|'
    party_box_names_pattern = '|'.join(map(re.escape, party_box_names))
    
    # Construct the regular expression pattern dynamically
    party_box_pattern = r'(\d+)\s+(?:{})'.format(party_box_names_pattern)

    # Find all matches of the party box pattern in the text
    matches = re.findall(party_box_pattern, text)

    # Update counts of specific party boxes in the party_boxes dictionary
    for match in matches:
        quantity, party_box_name = match
        if party_box_name in boxes:
            party_boxes[party_box_name]["count"] += int(quantity)-1

def extract_sandwich_quantities(text,sandwiches):
    # Define a list of possible sandwich names
        sandwich_names = [
        "#1 Pepe", "#2 Big John", "#3 Totally Tuna", "#4 Turkey Tom", "#5 Vito", "#6 The Veggie","J.J. B.L.T.", "#7 Spicy Italian","#8 Billy Club",
        "#9 Italian Club","#10 Hunters Club","#11 Country Club","#12 Beach Club","#13 Jimmy Cubano","#14 Bootlegger Club",
        "#15 Club Tuna","#16 Club Lulu","#17 Ultimate Porker","J.J. Gargatuan"
        
        ]
    
        # Join the sandwich names into a single string separated by '|'
        sandwich_names_pattern = '|'.join(map(re.escape, sandwich_names))
    
        # Construct the regular expression pattern dynamically
        sandwich_pattern = r'(\d+)\s+({})'.format(sandwich_names_pattern)


        # Find all matches of the sandwich pattern in the text
        matches = re.findall(sandwich_pattern, text)

        for match in matches:
            quantity, sandwich_name = match
            if sandwich_name in sandwiches:
                sandwiches[sandwich_name]["count"] += int(quantity) - 1
def extract_dessert_quantities(text,side_counts):
    # Define regular expression pattern for cookies
    dessert_pattern = r'(\d+)\s+(Oatmeal Raisin Cookie|Choc Chip Cookie|Fudge Choc Brownie)\b'

        # Find all matches of the cookie pattern in the text
    matches = re.findall(dessert_pattern, text)

        # Extract quantities from the matches
    for match in matches:
        quantity, dessert = match
        if dessert in side_counts:
            side_counts[dessert]["count"] += int(quantity) -1

def extract_chip_quantities(text, chips):
    # Define a list of possible chip names
    chip_names = [
        "Regular Chips", "BBQ Chips", "Jalapeno Chips", "Salt Vin Chips", "Thinny Chips"
    ]
    
    # Join the chip names into a single string separated by '|'
    chip_names_pattern = '|'.join(map(re.escape, chip_names))
    
    # Construct the regular expression pattern dynamically
    chip_pattern = r'(\d+)\s+((?:{}))'.format(chip_names_pattern)

    # Find all matches of the chip pattern in the text
    matches = re.findall(chip_pattern, text)

    # Check if there's a variety option
    variety_quantity = 0
    new_matches = []
    for quantity, chip_name in matches:
        if chip_name.lower() == "variety":
            variety_quantity = int(quantity)
        else:
            new_matches.append((quantity, chip_name))


    # If there's a variety option, distribute quantities evenly among chip types
    if variety_quantity:
        total_chip_types = len(chip_names)
        chips_per_type = variety_quantity // total_chip_types
        extra_chips = variety_quantity % total_chip_types

        # Update counts for each chip type
        for i, chip_name in enumerate(chip_names):
            quantity = chips_per_type + (1 if i < extra_chips else 0)
            chips[chip_name]["count"] += quantity

    # Update counts for each chip type from the matches
    for quantity, chip_name in matches:
        if chip_name in chips:
            chips[chip_name]["count"] += int(quantity) -1

def extract_wrap_quantities(text,wraps):
    # Define a list of possible wrap names
    wrap_names = [
        "Chicken Caesar Wrap", "Jalpeno Ranch Wrap", "Tuscan Italian Wrap"
    ]
    
    # Join the wrap names into a single string separated by '|'
    wrap_names_pattern = '|'.join(map(re.escape, wrap_names))
    
    # Construct the regular expression pattern dynamically
    wrap_pattern = r'(\d+)\s+(?:{})'.format(wrap_names_pattern)

    # Find all matches of the wrap pattern in the text
    matches = re.findall(wrap_pattern, text)

    # Update counts of specific wraps in the wraps dictionary
    for match in matches:
        quantity, wrap_name = match
        if wrap_name in wraps:
            wraps[wrap_name]["count"] += int(quantity)

def extract_pickle_quantities(text, pickles):
    # Define regular expression patterns for pickles and pickle buckets
    pickle_pattern = r'(\d+)\s+(?:Pickles)'
    pickle_bucket_pattern = r'(\d+)\s+(Pickle\sBucket)'

    # Find all matches of pickle pattern in the text
    pickle_matches = re.findall(pickle_pattern, text)
    for quantity, _ in pickle_matches:
        pickles["Pickles"]["count"] += int(quantity)

    # Find all matches of pickle bucket pattern in the text
    pickle_bucket_matches = re.findall(pickle_bucket_pattern, text)
    for quantity, _ in pickle_bucket_matches:
        pickles["Pickle Bucket"]["count"] += int(quantity)
        
def print_processed_data(processed_data):
    counts = processed_data["counts"]
    total_portions = processed_data["total_portions"]
    total_containers = processed_data["total_containers"]


    for item, info in counts.items():
        if info["count"] > 0:
            print(f"{item}: {info['count']} ordered")

    for ingredient, portions in total_portions.items():
        if portions > 0:
            portions_per_pack_ingredient = portions_per_pack.get(ingredient, 0)
            packs_used = (portions / portions_per_pack_ingredient)
            print(f"Packs used for {ingredient}: {packs_used:.2f}")

    total_containers_sum = sum(total_containers.values())
    if total_containers_sum > 0:
        for item, amount in total_containers.items():
            if amount > 0:
                print(f"{item}: {amount:.2f} containers")


def calculate_total_sandwiches_and_bread(sandwiches):
    total_sandwiches = 0
    total_bread_usage = 0
    total_trays = 0
    

    for item, info in sandwiches.items():
        count = info["count"]
        total_sandwiches += count
        if "GAINT" in item:
            total_bread_usage += count  # GAINT sandwiches use 1 whole stick each
        elif "UNWICH" in item:
            total_bread_usage -= count/2 # unwich don't use any bread 
        else:
            total_bread_usage += count / 2  # Assuming half a stick per sandwich
        
    total_trays = round(total_bread_usage/15,2)

    print(f"{total_bread_usage} sticks of bread, {total_trays} trays of bread")
    return total_sandwiches, total_bread_usage, total_trays       

def find_ready_time(receipt):
    # Regular expression pattern to find the date at the top of the receipt (e.g., "2024-06-22")
    date_pattern = r'^(\d{2}-\d{2}-\d{4})'  # Assuming the date format is DD-MM-YYYY
    
    # Regular expression pattern to find "ready at" time in the receipt (e.g., "@ 2:30 PM")
    ready_pattern = r'@ (\d{1,2}:\d{2}(?:\s*[APM]{2})?)'  # Adjusted for optional AM/PM

    # Search for the date pattern in the receipt
    date_match = re.search(date_pattern, receipt, re.IGNORECASE | re.MULTILINE)

    # Search for the "ready at" time pattern in the receipt
    time_match = re.search(ready_pattern, receipt, re.IGNORECASE)

    if date_match and time_match:
        date_str = date_match.group(1)  # Get the matched date string
        time_str = time_match.group(1)  # Get the matched time string

        # Combine the date and time strings
        combined_str = f"{date_str} {time_str}"

        # Parse the combined date and time string into a datetime object
        try:
            # If AM/PM is present, use 12-hour format, otherwise assume 24-hour format
            if 'AM' in time_str.upper() or 'PM' in time_str.upper():
                ready_time = datetime.strptime(combined_str, "%d-%m-%Y %I:%M %p")
            else:
                ready_time = datetime.strptime(combined_str, "%d-%m-%Y %H:%M")
            
            return ready_time
        except ValueError as e:
            print(f"Error parsing date and time: {e}")
            return None
    else:
        return None  # Return None if no date or time is found
    
#get the string from other file 
def read_ocr_output(file_path):
    with open(file_path, "r") as file:
        ocr_text = file.read()
    return ocr_text

def process_multiple_receipts(folder_path, boxes, sandwiches, wraps, side_counts):
    processed_receipts = []  # List to store processed receipt information

    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            ocr_text = read_ocr_output(file_path)
            
            processed_receipts.append(process_receipt(ocr_text, boxes))
            processed_receipts.append(process_receipt(ocr_text, sandwiches))
            processed_receipts.append(process_receipt(ocr_text, wraps))
            processed_receipts.append(process_receipt(ocr_text, side_counts))
            
        
    orders_list =[]            
    
    for receipt_data in processed_receipts:
        order = create_order_from_processed_data(processed_data)
        orders_list.append(order) 
    
    grand_total =0.0
    
    total_pattern = re.compile(r'Total\s*\s*\$([0-9]+(?:\.[0-9]{2})?)')

    # Process each receipt
    for receipt in processed_receipts:
        match = total_pattern.search(receipt)
        if match:
            total_amount = float(match.group(1))
            grand_total += total_amount    
    
    calculate_total_sandwiches_and_bread(sandwiches)
    
def create_order_from_processed_data(processed_data):
    counts = processed_data["counts"]
    total_portions = processed_data["total_portions"]
    total_containers = processed_data["total_containers"]
    ready_time = processed_data["ready_time"]
    order = Order(ready_time, counts, total_portions, total_containers)
    return order    
    
def main():
    folder_path = "receipt_text_files"
    process_multiple_receipts(folder_path, boxes, sandwiches, wraps, side_counts)
    
    
if __name__ == "__main__":
    main()
    
class Order:
    def __init__(self, ready_time, counts=None, total_portions=0, total_containers=0):
        if isinstance(ready_time, str):
            self.ready_time = datetime.strptime(ready_time, "%Y-%m-%d %H:%M:%S")
        else:
            self.ready_time = ready_time
        self.counts = counts if counts is not None else {}
        self.total_portions = total_portions
        self.total_containers = total_containers

    def __str__(self):
        items_str = ', '.join(f"{key}: {value}" for key, value in self.counts.items())
        return (f"Order Ready Time: {self.ready_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Items: {items_str}\n"
                f"Total Portions: {self.total_portions}\n"
                f"Total Containers: {self.total_containers}")