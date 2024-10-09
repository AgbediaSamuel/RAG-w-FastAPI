import unittest
from file_parser import FileParser, TextParser, PDFParser

class TestFileParser(unittest.TestCase):

    def test_ocr_parsing(self):
        parser = PDFParser()
        result = parser.parse('obama-ocr.pdf')
        self.assertIn("Barack Obama", result, "OCR parsing failed to find expected text")

    # def test_text_parsing(self):
    #     parser = TextParser()
    #     result = parser.parse('testfile.txt')
    #     self.assertEqual(result, "This is a sample text file.", "Text parsing failed")

    # def test_file_not_found(self):
    #     parser = FileParser('non_existent_file.txt')
    #     result = parser.parse()
    #     self.assertEqual(result, "File does not exist", "File not found handling failed")

    # def test_invalid_file_type(self):
    #     parser = FileParser('invalid_file_type.xyz')
    #     result = parser.parse()
    #     self.assertEqual(result, "Invalid File Type", "Invalid file type handling failed")

if __name__ == '__main__':
    unittest.main()