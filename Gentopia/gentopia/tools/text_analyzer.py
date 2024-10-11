from typing import AnyStr

from gentopia.tools.basetool import *
import os

class TextFileAnalyzeArgs(BaseModel):
    file_path: str = Field(..., description="Path to the text file")

class TextFileAnalyzer(BaseTool):
    """Tool that analyzes a text file and retrieves basic statistics."""

    name = "text_file_analyzer"
    description = ("A tool for analyzing text files. It provides the number of lines, words, "
                   "and characters in the text file.")

    args_schema: Optional[Type[BaseModel]] = TextFileAnalyzeArgs

    def _run(self, file_path: AnyStr) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        num_lines = text.count('\n') + 1
        num_words = len(text.split())
        num_characters = len(text)

        summary = (f"Analysis of {os.path.basename(file_path)}:\n"
                   f"Lines: {num_lines}\n"
                   f"Words: {num_words}\n"
                   f"Characters: {num_characters}\n")

        return summary

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    
    file_path = input("Enter the path to the text file: ")
    analyzer = TextFileAnalyzer()
    result = analyzer._run(file_path)
    print(result)
