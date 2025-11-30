from typing import Dict, Any, List
import os

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        # In a real scenario, we would initialize the OpenAI client here
        # self.client = OpenAI(api_key=self.api_key)

    def generate_variable_insights(self, col: str, stats: Dict[str, Any], dtype: str) -> Dict[str, str]:
        """
        Generates Short and Long insights for a specific variable.
        """
        short_insight = ""
        long_insight = ""
        
        if dtype == 'numeric':
            mean = stats.get('mean', 0)
            median = stats.get('50%', 0) # Median
            std = stats.get('std', 0)
            min_val = stats.get('min', 0)
            max_val = stats.get('max', 0)
            count = stats.get('count', 0)
            
            # Short Insight
            if abs(mean - median) < (0.1 * std):
                dist_shape = "normally distributed"
            elif mean > median:
                dist_shape = "positively skewed"
            else:
                dist_shape = "negatively skewed"
                
            short_insight = f"{col} is a {dist_shape} numeric variable with an average of {mean:.2f}."
            
            # Long Insight
            long_insight = (
                f"The variable '{col}' contains {int(count)} observations. "
                f"It ranges from a minimum of {min_val:.2f} to a maximum of {max_val:.2f}, with a standard deviation of {std:.2f}. "
                f"The average value is {mean:.2f}, while the median is {median:.2f}. "
            )
            
            if dist_shape == "normally distributed":
                long_insight += "The close proximity of the mean and median suggests a symmetrical, bell-shaped distribution. "
            elif dist_shape == "positively skewed":
                long_insight += "The mean is higher than the median, indicating a right-skewed distribution with potential high-value outliers. "
            else:
                long_insight += "The mean is lower than the median, indicating a left-skewed distribution. "
                
            cv = (std / mean) * 100 if mean != 0 else 0
            if cv > 50:
                long_insight += f"The data shows high variability (CV: {cv:.1f}%), suggesting significant spread in the values."
            else:
                long_insight += f"The data is relatively consistent (CV: {cv:.1f}%)."

        elif dtype == 'categorical':
            # For categorical, we need frequency data which might not be in 'stats' (describe output)
            # We'll assume 'stats' here is the value_counts dict or similar if passed differently, 
            # but standard 'describe' for object gives count, unique, top, freq.
            
            unique = stats.get('unique', 0)
            top = stats.get('top', 'N/A')
            freq = stats.get('freq', 0)
            count = stats.get('count', 0)
            
            short_insight = f"{col} is a categorical variable with {unique} unique values, dominated by '{top}'."
            
            long_insight = (
                f"The categorical variable '{col}' has {unique} distinct categories across {int(count)} records. "
                f"The most frequent category is '{top}', appearing {int(freq)} times, which accounts for {(freq/count*100):.1f}% of the data. "
            )
            
            if unique == count:
                long_insight += "Every record has a unique value, suggesting this might be an identifier."
            elif unique < 5:
                long_insight += "With fewer than 5 unique values, this variable is suitable for use as a grouping dimension in analysis."
            else:
                long_insight += "The variable shows a diverse range of categories."

        return {
            "short": short_insight,
            "long": long_insight
        }

    def generate_insights(self, data_summary: Dict[str, Any]) -> List[str]:
        """
        Generates insights based on the data summary.
        If an API key is present, it could call an LLM.
        For now, it returns mock insights based on the data.
        """
        insights = []
        
        # Mock logic to generate "smart" sounding insights
        summary = data_summary.get("summary", {})
        
        if not summary:
            return ["No data available to generate insights."]

        # Example: Look for high variance or specific trends in numeric data
        for col, stats in summary.items():
            if stats.get('std', 0) > stats.get('mean', 0):
                insights.append(f"Column '{col}' shows high variability (std dev > mean). Consider investigating outliers.")
            
            if stats.get('min', 0) < 0:
                insights.append(f"Column '{col}' contains negative values. Verify if this is expected.")

        # Generic insights
        insights.append("Data distribution suggests a potential correlation between numeric variables.")
        insights.append("Recommendation: Visualize the distribution of key metrics to identify skewness.")
        
        return insights
