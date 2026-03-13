"""
Start the Adaptive Quiz API server
This is just a launcher
"""

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print(f"Project root added to path: {project_root}")
print(f"Launching your FastAPI app from: app/main.py")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("API Docs: http://localhost:8000/docs")
    print("Alternative: http://localhost:8000/redoc")
    print("="*50 + "\n")
    
    uvicorn.run(
        "app.main:app",  
        host="0.0.0.0",
        port=8000,
        reload=True
    )