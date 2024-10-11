
from typing import AnyStr
from gentopia.tools.basetool import *
from .google_search import GoogleSearch

class BMICalculatorArgs(BaseModel):
    height: float = Field(..., description="Height in meters")
    weight: float = Field(..., description="Weight in kilograms")

class BMICalculator(BaseTool):
    """Tool for calculating BMI and providing health insights."""

    name = "bmi_calculator"
    description = ("Calculate Body Mass Index (BMI) based on height and weight "
                   "and provide health insights based on the BMI category.")

    args_schema: Optional[BaseModel] = BMICalculatorArgs

    def _run(self, **kwargs: Dict[str, Any]) -> str:
        # Extracting height and weight from the arguments
        args = kwargs.get('__arg1', '')
        height_str, weight_str = args.split(',')
        height = float(height_str)/100
        weight = float(weight_str)
        
        # Calculate BMI
        bmi = self._calculate_bmi(height, weight)
        
        # Get BMI category, advice, and health implications
        category = self._get_bmi_info(bmi)
        #lifestyle_tips = self._get_lifestyle_tips(category)
        
        # If overweight or obese, search for health and exercise options
        health_exercise_advice = ""
        if category in ["Overweight", "Obese"]:
            exercise_results = self._get_health_exercise_options(category)
            health_exercise_advice = f"\n\nHere are some health and exercise options:\n{exercise_results}"
                    
        health_implication_results = self._get_health_implications(category)
        health_implications = f"\n\nHere are some health and exercise options:\n{health_implication_results}"

        lifestyle_tips_results = self.get_lifestyle_tips(category)
        lifestyle_tips = f"\n\nHere are some health and exercise options:\n{lifestyle_tips_results}"

        






        
        return (f"Your BMI is {bmi:.2f}. You are classified as '{category}'. "
                f" {health_implications} {lifestyle_tips}{health_exercise_advice}")

    def _calculate_bmi(self, height: float, weight: float) -> float:
        return weight / (height ** 2)

    def _get_bmi_info(self, bmi: float) -> tuple:
        if bmi < 18.5:
            return ("Underweight")
        elif 18.5 <= bmi < 24.9:
            return ("Normal weight")
        elif 25 <= bmi < 29.9:
            return ("Overweight")
        else:
            return ("Obese")

    
    
    def get_lifestyle_tips(self, category: str) -> str:
        search_query = f"life style tips for {category.lower()}"
        google_search_tool = GoogleSearch()
        return google_search_tool._run(search_query)

    def _get_health_exercise_options(self, category: str) -> str:
        search_query = f"exercise options for {category.lower()}"
        google_search_tool = GoogleSearch()
        return google_search_tool._run(search_query)
    
    def _get_health_implications(self, category: str) -> str:
        search_query = f"Health implications for {category.lower()}"
        google_search_tool = GoogleSearch()
        return google_search_tool._run(search_query)
    

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    # Example Usage
    user_input = input("Enter your height in meters and weight in kilograms (e.g., '1.8,68'): ")
    
    bmi_calculator = BMICalculator()
    print(bmi_calculator._run(__arg1=user_input))
