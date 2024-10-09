from abc import ABC, abstractmethod
from PyPDF2 import PdfReader
import pytesseract
import fitz
from PIL import Image
import os
import io

class BaseParser(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def parse(self, filepath):
        pass


class TextParser(BaseParser):
    def __init__(self):
        super().__init__()

    def parse(self, filepath):
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except Exception as e:
            return f"Error Occurred: {str(e)}"


class PDFParser(BaseParser):
    def __init__(self):
        super().__init__()

    def parse(self, filepath):
        try:
            with open(filepath, 'rb') as file:
                reader = PdfReader(file)
                # include check for encrypted files
                text: str = ""
                for page in range(len(reader.pages)):
                    page_content = reader.pages[page].extract_text()
                    if not page_content:
                        page_content: str = self.ocr(filepath, page)
                    text += page_content
                return text
        except Exception as e:
            return {"message": f"Error Occurred: {str(e)}"}
    

    def ocr(self, filepath, page) -> str:
        try:
            document = fitz.open(filepath)
            page = document.load_page(page)
            temp = page.get_pixmap()
            image = Image.open(io.BytesIO(temp.tobytes("png")))
            text: str = pytesseract.image_to_string(image)
            document.close() #might be unnecessary
            return text
        except Exception as e:
            return f"Error Occurred: {str(e)}"
        

# creating registry for parsers
class register_parser:
    parsers = {}

    @classmethod
    def register(cls, extension, parser):
        cls.parsers[extension] = parser

register_parser.register("txt", TextParser)
register_parser.register("pdf", PDFParser)


# creating a method to return the correct parser and parse the file
class FileParser:
    def __init__(self, filepath):
        self.filepath = filepath

        def parse(self):
            try:
                if not os.path.exists(self.filepath):
                    return "File does not exist"
                extension = os.path.splitext(self.filepath)[1]
                if extension in register_parser.parsers:
                    return "Invalid File Type"
                return register_parser.parsers[extension].parse(self.filepath)
            except Exception as e:
                return f"Error Occurred: {str(e)}"