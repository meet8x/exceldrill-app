"""Test script to verify HTML dashboard generation works correctly"""
import pandas as pd
import numpy as np
from backend.app.services.html_dashboard_service import HtmlDashboardService

# Create sample data
np.random.seed(42)
df = pd.DataFrame({
    'age': np.random.randint(18, 65, 100),
    'salary': np.random.randint(30000, 120000, 100),
    'experience': np.random.randint(0, 30, 100),
    'department': np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR'], 100),
    'performance': np.random.choice(['Excellent', 'Good', 'Average', 'Poor'], 100)
})

# Mock stats
stats = {
    'summary': {
        'age': {'mean': df['age'].mean(), 'std': df['age'].std(), 'min': df['age'].min(), 'max': df['age'].max()},
        'salary': {'mean': df['salary'].mean(), 'std': df['salary'].std(), 'min': df['salary'].min(), 'max': df['salary'].max()},
        'experience': {'mean': df['experience'].mean(), 'std': df['experience'].std(), 'min': df['experience'].min(), 'max': df['experience'].max()}
    }
}

# Mock insights
insights = [
    "Average age is 41 years with good distribution across age groups",
    "Salary ranges from $30K to $120K with mean around $75K",
    "Strong correlation (0.85) between experience and salary",
    "Engineering department has highest average salary",
    "Performance ratings are fairly distributed across all departments"
]

print("Testing HTML Dashboard Service...")
try:
    service = HtmlDashboardService()
    html_buffer = service.generate_dashboard(df, stats, insights)
    
    # Save to file
    with open('test_dashboard.html', 'wb') as f:
        f.write(html_buffer.getvalue())
    
    print("✓ HTML dashboard generated successfully!")
    print(f"✓ File size: {len(html_buffer.getvalue())} bytes")
    print("✓ Saved to: test_dashboard.html")
    print("\nYou can now open test_dashboard.html in your browser to verify:")
    print("  - Interactive Plotly charts")
    print("  - Responsive layout with sidebar navigation")
    print("  - Data quality table")
    print("  - Correlation heatmap")
    print("  - Export to PDF button")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
