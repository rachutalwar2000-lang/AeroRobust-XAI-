import io, os, time
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
load_dotenv(Path(__file__).resolve().parents[1] / '.env')
app=FastAPI(title='UAV Object Detection API',description='Research starter API; demo mode is explicit until weights are configured.',version='1.0.0')
origins=[x.strip() for x in os.getenv('CORS_ORIGINS','http://localhost:5173,http://127.0.0.1:5173').split(',') if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=False,allow_methods=['GET','POST','OPTIONS'],allow_headers=['*'])
MODEL_PATH=os.getenv('MODEL_PATH','').strip(); CONF=float(os.getenv('CONFIDENCE_THRESHOLD','0.25')); MAX_MB=int(os.getenv('IMAGE_MAX_MB','10')); _model:Any=None

def get_model():
 global _model
 if not MODEL_PATH: return None
 path=Path(MODEL_PATH)
 if not path.is_absolute(): path=Path(__file__).resolve().parents[1]/path
 if not path.exists(): raise HTTPException(status_code=503,detail=f'Configured model file does not exist: {path}')
 if _model is None:
  try: from ultralytics import YOLO; _model=YOLO(str(path))
  except ImportError: raise HTTPException(status_code=503,detail='Install Ultralytics: pip install ultralytics')
  except Exception as exc: raise HTTPException(status_code=503,detail=f'Could not load model: {exc}')
 return _model
@app.get('/')
def root(): return {'name':'UAV Object Detection API','docs':'/docs','health':'/health'}
@app.get('/health')
def health(): return {'status':'ok','mode':'yolo' if MODEL_PATH else 'demo','model_configured':bool(MODEL_PATH),'model_loaded':_model is not None,'note':'Demo mode does not generate detections.' if not MODEL_PATH else 'Model loads on first prediction.'}
@app.post('/predict')
async def predict(file:UploadFile=File(...)):
 if not file.content_type or not file.content_type.startswith('image/'): raise HTTPException(status_code=415,detail='Please upload an image file.')
 data=await file.read()
 if not data: raise HTTPException(status_code=400,detail='Uploaded file is empty.')
 if len(data)>MAX_MB*1024*1024: raise HTTPException(status_code=413,detail=f'Image exceeds {MAX_MB} MB limit.')
 try: image=Image.open(io.BytesIO(data)).convert('RGB')
 except (UnidentifiedImageError,OSError): raise HTTPException(status_code=400,detail='File could not be decoded as an image.')
 if not MODEL_PATH: return {'mode':'demo','message':'Image received. Configure MODEL_PATH with trained YOLO weights for real inference.','filename':file.filename or 'uploaded-image','image_width':image.width,'image_height':image.height,'detections':[],'inference_ms':None}
 model=get_model(); start=time.perf_counter()
 try:
  results=model.predict(source=image,conf=CONF,verbose=False); elapsed=(time.perf_counter()-start)*1000; detections=[]
  if results:
   result=results[0]; names=result.names
   if result.boxes is not None:
    for box in result.boxes:
     coords=[float(v) for v in box.xyxy[0].tolist()]; cls_id=int(box.cls[0].item()); confidence=float(box.conf[0].item())
     detections.append({'class_name':str(names.get(cls_id,cls_id) if isinstance(names,dict) else cls_id),'confidence':confidence,'box':coords})
  return {'mode':'yolo','message':'Inference completed. Confidence scores are not automatically calibrated probabilities.','filename':file.filename or 'uploaded-image','image_width':image.width,'image_height':image.height,'detections':detections,'inference_ms':elapsed}
 except HTTPException: raise
 except Exception as exc: raise HTTPException(status_code=500,detail=f'Inference failed: {exc}')
