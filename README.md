# AI Career Path Predictor

A Django web application that predicts career paths based on skill assessment, provides learning roadmaps, skill gap analysis, career demand insights, and includes features like a career chatbot, resume analyzer, and personality test.

## Getting Started

1. Create a Python virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

- Windows (PowerShell): `& .venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Train the prediction model (required anytime the dataset changes):

```bash
python manage.py train_model
```

6. Run the server:

```bash
python manage.py runserver
```

## Notes

- Update `ml_training/dataset.csv` and retrain with `python manage.py train_model` to refresh predictions.
- Resume analyzer supports `.txt`, `.pdf`, and `.docx` resume uploads.
