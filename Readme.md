Code Scorer is a Python-based tool that analyzes and scores Python code snippets using machine learning. It extracts syntactic and structural features from code and predicts a score out of 100 based on training data.

🔍 How It Works
Feature Extraction (feature_extractor.py)

Uses lexical analysis (PLY) and abstract syntax trees (AST) to extract:

Token count

Keyword/operator usage

Number of variables

Loops, branches, function calls

Nesting depth and recursion

Estimated time and space complexity

Model Training (model.py)

Trains a linear regression model on code_samples.csv

Evaluates model using MAE and R² score

Prediction Interface (main.py)

Accepts Python code input from the user

Outputs a predicted score between 0 and 100