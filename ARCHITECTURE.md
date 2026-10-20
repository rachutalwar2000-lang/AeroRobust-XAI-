# Architecture

```text
Browser -> React + Vite dashboard -> POST /predict -> FastAPI
                                                |-> image validation
                                                |-> demo response if no weights
                                                `-> optional Ultralytics YOLO inference

Research pipeline (planned): VisDrone -> baseline -> controlled corruptions
 -> condition-augmented training -> per-condition evaluation
 -> calibration/error ranking -> explanation stability
```

The starter does not yet implement the complete training pipeline, corruption benchmark, calibration study, or D-RISE explanation engine. Those must be implemented and evaluated separately.
