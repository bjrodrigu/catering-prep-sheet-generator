import os
import io
from google.cloud import vision
from PIL import Image
import fitz
from dotenv import load_dotenv

load_dotenv()

class ReceiptScanner:
    def __init__(self):
        self.receipts_data = []

    def pdfprocess(self, chosenPDF):
        try:
            client = vision.ImageAnnotatorClient()
            doc = fitz.open(chosenPDF)
            print("Number of pages: ", doc.page_count)
            text = ""
            for page_number in range(doc.page_count):
                page = doc.load_page(page_number)
                page_text = page.get_text("text")  # Try plain text extraction first

                if not page_text:
                    # If no text found, try extracting images and use OCR
                    print(f"Attempting OCR on page {page_number + 1}")
                    image_list = page.get_images(full=True)
                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image = Image.open(io.BytesIO(image_bytes))

                        # Convert PIL image to bytes for Google Vision API
                        image_byte_arr = io.BytesIO()
                        image.save(image_byte_arr, format='PNG')
                        content = image_byte_arr.getvalue()

                        image = vision.Image(content=content)
                        response = client.text_detection(image=image)
                        ocr_text = response.full_text_annotation.text
                        page_text += ocr_text

                if page_text:
                    text += page_text
                else:
                    print(f"No text found on page {page_number + 1}")

            # Create output file name
            base_name = os.path.splitext(chosenPDF)[0]
            outputFile = f"{base_name}_processed.txt"
            self.receipts_data.append(outputFile)

            # Save the OCR output to the file
            with open(outputFile, "w") as file:
                file.write(text)
            print(f"OCR output saved to {outputFile}")

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def imageprocess(self, chosenImage):
        try:
            client = vision.ImageAnnotatorClient()

            # Read the image file
            with io.open(chosenImage, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            text = response.full_text_annotation.text

            # Create output file name
            base_name = os.path.splitext(chosenImage)[0]
            outputFile = f"{base_name}_processed.txt"
            self.receipts_data.append(outputFile)

            # Save the OCR output to the file
            with open(outputFile, "w") as file:
                file.write(text)
            print(f"OCR output saved to {outputFile}")

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def main(self):
        while True:
            imageInput = input("Name of image file (or 'q' to quit): ")
            if imageInput == 'q':
                break
            if imageInput.endswith(".pdf"):
                print("PDF file detected")
                self.pdfprocess(imageInput)
            else:
                self.imageprocess(imageInput)

if __name__ == "__main__":
    scanner = ReceiptScanner()
    scanner.main()
