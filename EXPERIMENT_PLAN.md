# Experimental Plan

## Research question
How do adverse visual conditions affect UAV detection performance, uncertainty reliability, and explanation stability, and does condition augmentation help?

## Dataset
Start with the official VisDrone-DET release: https://github.com/VisDrone/VisDrone-Dataset. Record the release, split files, date, terms, and any filtering. Do not use hidden test labels.

## Experiment matrix
1. Train a clean baseline.
2. Evaluate the baseline on fixed clean validation data.
3. Evaluate the same checkpoint on documented fog, rain, low-light, blur and noise conditions at predefined severities.
4. Train a condition-augmented variant using training data only.
5. Evaluate both models on identical clean and corrupted validation inputs.
6. Add calibration/error-ranking metrics only after documenting matching rules for detections, false positives and missed objects.
7. Add an explanation method such as D-RISE and define a quantitative stability measure.

## Metrics
Report mAP@0.5, mAP@0.5:0.95, precision, recall, per-class/per-condition results, runtime/hardware, and documented calibration, error-ranking and explanation-stability metrics.

## Reproducibility
Record model/weights hash, software versions, dataset split, seeds, image size, epochs, batch size, optimizer, learning rate, augmentations, confidence threshold, NMS settings, evaluation implementation, hardware and runtime. Published literature scores must remain attributed to their original methods and datasets.
