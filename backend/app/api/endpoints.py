from fastapi import APIRouter, UploadFile, File, HTTPException, Body, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
from typing import Dict, Any, Optional
from backend.app.services.data_processing import DataProcessor
from backend.app.services.ai_service import AIService
from backend.app.services.report_service import ReportService
from backend.app.services.excel_service import ExcelService
from backend.app.services.html_dashboard_service import HtmlDashboardService
from backend.app.services.data_quality_service import DataQualityService
from backend.app.services.statistical_tests import StatisticalTestsService
from backend.app.api import deps
from backend.app.models.user import User
import io
import uuid
import os
import asyncio

router = APIRouter()

# In-memory job store
# Key: job_id, Value: {status: str, progress: int, result: str|None, error: str|None}
jobs: Dict[str, Dict[str, Any]] = {}

def update_progress(job_id: str, progress: int):
    if job_id in jobs:
        jobs[job_id]['progress'] = progress

def generate_report_task(job_id: str, report_format: str, processor: DataProcessor, ai_service: AIService, report_service: ReportService, color_scheme: str = 'kpmg'):
    try:
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['progress'] = 10
        
        stats = processor.get_statistics()
        insights = ai_service.generate_insights(stats)
        
        jobs[job_id]['progress'] = 20
        
        # Define callback
        def progress_callback(p):
            update_progress(job_id, p)

        # Initialize service with color scheme
        report_service = ReportService(color_scheme=color_scheme)

        if report_format == "word":
            buffer = report_service.generate_word_report(processor.df, stats, insights, progress_callback)
            filename = f"report_{job_id}.docx"
        elif report_format == "ppt":
            buffer = report_service.generate_ppt_report(processor.df, stats, insights, progress_callback)
            filename = f"report_{job_id}.pptx"
        elif report_format == "excel":
            excel_service = ExcelService()
            buffer = excel_service.generate_excel_report(processor.df, stats, insights)
            filename = f"report_{job_id}.xlsx"
        elif report_format == "html":
            html_service = HtmlDashboardService()
            buffer = html_service.generate_dashboard(processor.df, stats, insights)
            filename = f"report_{job_id}.html"
        else:
            raise ValueError(f"Unsupported format: {report_format}")
        
        # Save to temp file
        temp_path = os.path.join("temp", filename)
        os.makedirs("temp", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(buffer.getvalue())
            
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['result'] = temp_path
        
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['error'] = str(e)

# ... (keep existing data_store and get_processor) ...
# In-memory storage for simplicity (not production ready)
# Key: session_id (or just 'default' for single user), Value: DataProcessor instance
data_store: Dict[str, DataProcessor] = {}

def get_processor(session_id: str = "default") -> DataProcessor:
    if session_id not in data_store:
        data_store[session_id] = DataProcessor()
    return data_store[session_id]

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    processor = get_processor()
    content = await file.read()
    try:
        preview = processor.load_data(content, file.filename)
        return {"message": "File uploaded successfully", "preview": preview}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/clean")
async def clean_data(action: str = Body(...), params: Dict[str, Any] = Body(default={})):
    processor = get_processor()
    try:
        preview = processor.clean_data(action, params)
        return {"message": "Data cleaned", "preview": preview}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/analyze")
async def analyze_data():
    processor = get_processor()
    try:
        stats = processor.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze/univariate")
async def analyze_univariate(column: str = Body(..., embed=True)):
    processor = get_processor()
    try:
        result = processor.get_univariate_analysis(column)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze/bivariate")
async def analyze_bivariate(col1: str = Body(...), col2: str = Body(...)):
    processor = get_processor()
    try:
        result = processor.get_bivariate_analysis(col1, col2)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyze/multivariate")
async def analyze_multivariate(columns: list[str] = Body(..., embed=True)):
    processor = get_processor()
    try:
        result = processor.get_multivariate_analysis(columns)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/chart-data")
async def chart_data(x_col: str = Body(...), y_col: str = Body(default=None), chart_type: str = Body(default="bar")):
    processor = get_processor()
    try:
        data = processor.get_chart_data(x_col, y_col, chart_type)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/insights")
async def get_insights():
    processor = get_processor()
    ai_service = AIService()
    try:
        stats = processor.get_statistics()
        insights = ai_service.generate_insights(stats)
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/report/start/{report_format}")
async def start_report_generation(
    report_format: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_user)
):
    if not current_user.is_paid:
        raise HTTPException(status_code=403, detail="Payment required to download reports.")
        
    if report_format not in ["word", "ppt", "excel", "html"]:
        raise HTTPException(status_code=400, detail="Invalid format")

    processor = get_processor()
    if processor.df is None:
        raise HTTPException(status_code=400, detail="No data loaded")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "result": None,
        "error": None
    }
    
    ai_service = AIService()
    report_service = ReportService(color_scheme=current_user.preferred_color_scheme or 'kpmg')
    
    background_tasks.add_task(generate_report_task, job_id, report_format, processor, ai_service, report_service, current_user.preferred_color_scheme or 'kpmg')
    
    return {"job_id": job_id}

@router.get("/report/status/{job_id}")
async def get_report_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@router.get("/report/download/{job_id}")
async def download_generated_report(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job = jobs[job_id]
    if job['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Report not ready")
        
    file_path = job['result']
    if not os.path.exists(file_path):
        raise HTTPException(status_code=500, detail="File not found")
        
    filename = os.path.basename(file_path)
    
    # Determine media type based on file extension
    if filename.endswith(".docx"):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif filename.endswith(".pptx"):
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    elif filename.endswith(".xlsx"):
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif filename.endswith(".html"):
        media_type = "text/html"
    else:
        media_type = "application/octet-stream"
    
    return FileResponse(
        file_path, 
        media_type=media_type, 
        filename=filename
    )

@router.get("/analyze/data-quality")
async def analyze_data_quality():
    """Analyze data quality and return issues and recommendations"""
    processor = get_processor()
    if processor.df is None:
        raise HTTPException(status_code=400, detail="No data loaded")
    
    try:
        quality_service = DataQualityService()
        quality_report = quality_service.analyze_quality(processor.df)
        return quality_report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/statistical-test")
async def run_statistical_test(
    test_type: str = Body(...),
    params: Dict[str, Any] = Body(...)
):
    """Run statistical tests (ANOVA, T-test, Chi-Square, Normality)"""
    processor = get_processor()
    if processor.df is None:
        raise HTTPException(status_code=400, detail="No data loaded")
    
    try:
        stats_service = StatisticalTestsService()
        
        if test_type == "anova":
            result = stats_service.run_anova(processor.df, params['categorical_col'], params['numeric_col'])
        elif test_type == "t_test":
            result = stats_service.run_t_test(processor.df, params['group_col'], params['numeric_col'], params.get('test_type', 'independent'))
        elif test_type == "normality":
            result = stats_service.run_normality_test(processor.df, params['column'])
        elif test_type == "chi_square":
            result = stats_service.run_chi_square_test(processor.df, params['col1'], params['col2'])
        else:
            raise HTTPException(status_code=400, detail=f"Unknown test type: {test_type}")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
