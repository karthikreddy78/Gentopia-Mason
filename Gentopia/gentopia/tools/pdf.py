from typing import AnyStr
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *


class PDFReadArgs(BaseModel):
    file_path: str = Field(..., description="Path to the PDF file")


class PDFReader(BaseTool):
    """Tool that reads and summarizes first few lines of text from a PDF file.I have used the same template as google_search"""

    name = "pdf_reader"
    description = ("A tool for reading PDF files and retrieving summarized text from them."
                   "Input should be the local file path to the PDF.")

    args_schema: Optional[Type[BaseModel]] = PDFReadArgs

    def _run(self, file_path: AnyStr) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        #I have chosen to print the first 10 lines of a pdf file
        sentences = text.split('.')
        summary = '. '.join(sentences[:10]) + '.'
        return summary

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = PDFReader()._run("kmusku.pdf")
    print(ans)
