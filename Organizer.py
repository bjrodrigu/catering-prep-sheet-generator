import ReceiptScanner
import re
def counting(receipt):
#Create dictonaries(hashmaps) of the items that need to be counted 
    boxes = {
        "30Pc Party Box":0,   "18Pc PartyBox":0,   "12 pack":0,    "Wrapbox":0
    }

    side_counts ={
        "Regular" :0,   "BBQ":0,    "Jalapeno":0,   "S&V":0,    "Thinny":0,
        "PotSalad":0,   "PastaSalad":0,     "PotSalad(LG)":0,   "PastaSalad(LG)":0, "Pickle Bucket":0,
        "Chocolatechip":0,  "Oatmealrasin":0,   "Brownie":0
    }

    sandwiches={
        "#1 Pepe":0, "#2 Big John":0, "#3 Totally Tuna":0, "#4 Turkey Tom":0,"#5 Vito":0,"#6 The Veggie":0,"#7 Spicy Italian":0,"#8 Billy Club":0,"J.J. BLT":0,
        "#9 Italian Night Club":0,"#10 Hunters Club":0,"#11 Country Club":0,"#12 Beach Club":0,"#13 Jimmy Cubano":0,"#14 Bootleger":0,"#15 Club Tuna":0,
        "#16 Club Lulu":0,"#17 Ultimate Porker":0,"J.J Garganutan":0    
    }
    wraps={
        "Chicken Ceaser":0,"Jalapeno Ranch":0,"Tuscan Italian":0   
    }

    #Look for key phrases in the receipt
    for box in boxes:
        occurances = re.findall(re.escape(box),receipt,re.IGNORECASE)
        boxes[box] = len(occurances)
        
    for side in side_counts:
        occurrences = re.findall(re.escape(side), receipt, re.IGNORECASE)
        side_counts[side] = len(occurrences)

    for sandwich in sandwiches:
        occurrences = re.findall(re.escape(sandwich), receipt, re.IGNORECASE)
        sandwiches[sandwich] = len(occurrences)

    for wrap in wraps:
        occurrences = re.findall(re.escape(wrap), receipt, re.IGNORECASE)
        wraps[wrap] = len(occurrences)

    return boxes, side_counts, sandwiches, wraps

#get the string from other file 
def read_ocr_output(file_path):
    with open(file_path, "r") as file:
        ocr_text = file.read()
    return ocr_text

def main():
     # Assuming the input file was "Receipt2_processed.txt"
    output_file = "Receipt2_processed.txt"
    ocr_text = read_ocr_output(output_file)
    
    boxes, side_counts, sandwiches, wraps = counting(ocr_text)
    
    print("Box counts:", boxes)
    print("Side counts:", side_counts)
    print("Sandwich counts:", sandwiches)
    print("Wrap counts:", wraps)

if __name__ == "__main__":
    main()



