
from typing import AnyStr
from gentopia.tools.basetool import *

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

        bmi = self._calculate_bmi(height, weight)
        
        category, advice, health_implications = self._get_bmi_info(bmi)
        lifestyle_tips = self._get_lifestyle_tips(category)
        
        return (f"Your BMI is {bmi:.2f}. You are classified as '{category}'. "
                f"{advice} {health_implications} {lifestyle_tips}")

    def _calculate_bmi(self, height: float, weight: float) -> float:
        return weight / (height ** 2)

    def _get_bmi_info(self, bmi: float) -> tuple:
        if bmi < 18.5:
            return ("Underweight", "Consider gaining weight to reach a healthier BMI.", 
                    "Health Implications: Being underweight can lead to nutritional deficiencies, weakened immune system, and potential fertility issues.")
        elif 18.5 <= bmi < 24.9:
            return ("Normal weight", "Great job! Maintain your current lifestyle.", 
                    "Health Implications: Generally, a normal weight reduces the risk of chronic diseases and promotes overall well-being.")
        elif 25 <= bmi < 29.9:
            return ("Overweight", "Consider adopting a healthier diet and exercise routine.", 
                    "Health Implications: Overweight individuals are at an increased risk for heart disease, type 2 diabetes, and hypertension.")
        else:
            return ("Obese", "It's advisable to consult a healthcare provider for personalized advice.", 
                    "Health Implications: Obesity can lead to serious health issues, including cardiovascular disease, certain cancers, and joint problems.")

    def _get_lifestyle_tips(self, category: str) -> str:
        if category == "Overweight":
            return ("**Lifestyle Tips for Overweight Individuals:**\n"
                    "- Incorporate more physical activity into your daily routine. Aim for at least 150 minutes of moderate aerobic activity each week.\n"
                    "- Focus on a balanced diet rich in fruits, vegetables, whole grains, and lean proteins.\n"
                    "- Limit the intake of processed foods, sugars, and unhealthy fats.\n"
                    "- Stay hydrated by drinking plenty of water throughout the day.\n"
                    "- Consider keeping a food diary to track your eating habits.\n"
                    "- Set realistic weight loss goals, aiming for 1-2 pounds per week.\n")
        elif category == "Obese":
            return ("**Lifestyle Tips for Obese Individuals:**\n"
                    "- Consult a healthcare provider or nutritionist for personalized advice and support.\n"
                    "- Incorporate regular exercise into your routine, starting slowly and gradually increasing intensity.\n"
                    "- Focus on portion control and mindful eating practices.\n"
                    "- Engage in activities that you enjoy to make exercise more enjoyable.\n"
                    "- Consider joining a support group for motivation and accountability.\n")
        else:
            return ""

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    # Example Usage
    user_input = input("Enter your height in meters and weight in kilograms (e.g., '1.8,68'): ")
    
    bmi_calculator = BMICalculator()
    print(bmi_calculator._run(__arg1=user_input))
