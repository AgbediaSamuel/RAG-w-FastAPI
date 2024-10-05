from abc import ABC, abstractmethod
import pytesseract
from PyPDF2 import PdfReader

class BaseParser(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def parse(self, filepath):
        pass


class FileParser(BaseParser):
    def __init__(self):
        super().__init__()

    def parse(self, filepath):
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except Exception as e:
            return {"message": f"Error Occurred: {str(e)}"}


class PDFParser(BaseParser):
    def __init__(self):
        super().__init__()

    def parse(self, filepath):
        try:
            with open(filepath, 'rb') as file:
                reader = PdfReader(file)
                text = ""
                for page in range(len(reader.pages)):
                    text += reader.pages[page].extract_text()
                return text
        except Exception as e:
            return {"message": f"Error Occurred: {str(e)}"}