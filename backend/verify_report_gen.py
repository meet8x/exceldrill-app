import pandas as pd
import numpy as np
from app.services.report_service import ReportService
from app.services.ai_service import AIService
import os

# Mock data
df = pd.DataFrame({
    'A': np.random.rand(100),
    'B': np.random.randint(0, 100, 100),
    'C': np.random.choice(['X', 'Y', 'Z'], 100)
})

stats = {
    'summary': {
        'A': {'mean': 0.5, 'min': 0, 'max': 1},
        'B': {'mean': 50, 'min': 0, 'max': 100}
    }
}

insights = ["Insight 1", "Insight 2"]

report_service = ReportService()

print("Generating Word Report...")
try:
    word_buffer = report_service.generate_word_report(df, stats, insights)
    with open("test_report.docx", "wb") as f:
        f.write(word_buffer.read())
    print("Word Report Generated Successfully.")
except Exception as e:
    print(f"Word Report Failed: {e}")

print("Generating PPT Report...")
try:
    ppt_buffer = report_service.generate_ppt_report(df, stats, insights)
    with open("test_report.pptx", "wb") as f:
        f.write(ppt_buffer.read())
    print("PPT Report Generated Successfully.")
except Exception as e:
    print(f"PPT Report Failed: {e}")
