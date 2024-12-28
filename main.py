from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from script import run_script

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Allows all origins, you can specify your frontend URL here
    allow_origins=["*"],
    allow_credentials=True,
    # Allows all methods like GET, POST, PUT, DELETE, etc.
    allow_methods=["*"],
    allow_headers=["*"],  # Allows all headers
)

SCRIPT_PATH = "./script.py"  # Replace with your script path

@app.post("/run")
async def run():
    try:
        # Execute the script
        result = run_script()
        # Prepare the response
        response_data = result
    except subprocess.CalledProcessError as e:
        response_data = {
            "status": "error",
            "output": e.stderr
        }
    except Exception as e:
        response_data = {
            "status": "error",
            "output": str(e)
        }

    return JSONResponse(content=response_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)