import ReceiptScanner
import re
#Create dictonaries(hashmaps) of the items that need to be counted 
boxes = {
    "30Pc Party Box":{"count":0},   "18Pc PartyBox":{"count":0},   "12 pack":{"count":0},
    "Wrapbox":{"count":0}, "(Box)":{"count":0}
}

side_counts ={
    "Regular" :{"count":0},   "BBQ":{"count":0},    "Jalapeno":{"count":0},   "S&V":{"count":0},    "Thinny":{"count":0},
    "PotSalad":{"count":0},   "PastaSalad":{"count":0},     "PotSalad(LG)":{"count":0},   "PastaSalad(LG)":{"count":0},
    "Pickle Bucket":{"count":0},"Chocolatechip":{"count":0},  "Oatmealrasin":{"count":0},   "Brownie":{"count":0}
}
    #the layout for the dic is sandwich name{Num of sandwiches, portion need to make the sandwiches after that}
sandwiches={
    "#1 Pepe": {"count":0, "cheese":1, "ham":1}, "#2 Big John":{"count":0,"roast beef":1},
    "#3 Totally Tuna":{"count":0,"tuna":1}, "#4 Turkey Tom":{"count":0,"turkey":1},
    "#5 Vito":{"count":0,"cheese":1,"vito":1},"#6 The Veggie":{"count":0,"cheese":2},"J.J. BLT":{"count":0,"bacon":6},
    "#7 Spicy Italian":{"count":0,"cheese":1,"vito":2},"#8 Billy Club":{"count":0,"cheese":1,"ham":1,"roast beef":1},
    "#9 Italian Night Club":{"count":0,"cheese":1,"ham":1,"vito":1},"#10 Hunters Club":{"count":0,"cheese":1,"roast beef":2},
    "#11 Country Club":{"count":0,"cheese":1,"ham":1,"turkey":1},"#12 Beach Club":{"count":0,"cheese":2,"turkey":1},
    "#13 Jimmy Cubano":{"count":0,"cheese":1,"ham":1,"bacon":4},"#14 Bootleger":{"count":0,"turkey":1,"roast beef":1},
    "#15 Club Tuna":{"count":0,"cheese":2,"tuna":1},"#16 Club Lulu":{"count":0,"turkey":1,"bacon":3},
    "#17 Ultimate Porker":{"count":0,"ham":1,"bacon":3},
    "J.J. Garganutan":{"count":0,"cheese":1,"ham":1,"roast beef":1,"turkey":1,"vito":1}    
}
wraps={
    "Chicken Ceaser":{"count":0,"chicken":1},"Jalapeno Ranch":{"count":0,"cheese":1,"chicken":1},
    "Tuscan Italian":{"count":0,"vito":1,"ham":1}   
}
portions_per_pack={
    "cheese":60, "vito":25,"roast beef":30, "turkey":25,"ham":25,"chicken":7,"bacon":150
}
items_per_box={
    "Regular":72,   "BBQ":72,    "Jalapeno":72,   "S&V":72, "Thinny":72
    ,"Chocolate Chip":56,"Oatmeal Rasin":56,"Brownies":42,"pasta salad":2041.17,"potato salad":3628.74
}

def process_receipt(receipt, dictionary):
    total_portions={}
    total_packs={}
    total_containers={}
    
    for item, info in dictionary.items():
        count = 0
        occurrences = re.findall(re.escape(item), receipt, re.IGNORECASE)
        count = len(occurrences)
        info["count"] += count

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

    #  Display the updated counts
    for item, info in dictionary.items():
        if info["count"] > 0:  # only print if it is ordered 
            print(f"{item}: {info['count']} ordered")
            
    # Print the total portions of each ingredient greater than 1
    for ingredient, portions in total_portions.items():
        if portions > 0:
            portions_per_pack_ingredient = portions_per_pack.get(ingredient, 0)
            packs_used = (portions / portions_per_pack_ingredient)
            print(f"Packs used for {ingredient}: {packs_used:.2f}")
            
    # Print the total containers of sides used
    total_containers_sum = sum(total_containers.values())
    if total_containers_sum >0:
        print(f"Total containers of sides used: {total_containers_sum:.2f}")
        
    #use the find order time function to find time of order
    ready_time=find_ready_time(receipt)
    print(ready_time)
        
    

def find_ready_time(receipt):
    # Regular expression pattern to find "@ ready at" time in the receipt
    ready_pattern = r'@ (\d{1,2}:\d{2} [AP]M)'

    # Search for the "@ ready at" time pattern in the receipt
    match = re.match(ready_pattern, receipt, re.IGNORECASE)

    if match:
        return match.group(1)  # Return the matched time
    else:
        return None  # Return None if no time is found
    
#get the string from other file 
def read_ocr_output(file_path):
    with open(file_path, "r") as file:
        ocr_text = file.read()
    return ocr_text

def main():
     # Assuming the input file was "Receipt2_processed.txt"
    output_file = "Receipt2_processed.txt"
    ocr_text = read_ocr_output(output_file)
    # Call the function to process the receipt
    process_receipt(ocr_text, boxes)
    process_receipt(ocr_text, sandwiches)
    process_receipt(ocr_text, wraps)
    process_receipt(ocr_text, side_counts)
    
if __name__ == "__main__":
    main()



