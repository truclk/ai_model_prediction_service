# AI Model Prediction Service

A comprehensive benchmarking framework for evaluating AI predictive models across diverse datasets.

## Features

- User-friendly interface for dataset upload and model selection
- Automated training and evaluation process
- Comprehensive performance metrics (accuracy, precision, recall, F1-score, ROC curves)
- Support for multiple AI models including KNN, LGBM, Logistic Regression, and Naive Bayes

## Prerequisites

- Python 3.12+
- pip
- Redis server

## Installation

1. Install system dependencies:

```bash
sudo apt install python3-pip python3.12-venv redis-server
```

2. Clone the repository:

```bash
git clone https://github.com/truclk/ai_model_prediction_service.git
cd ai_model_prediction_service
```

3. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Configuration

1. Prepare the database:
```bash
make migrate
```

2. Edit the c.IdentityProvider.token in jupyter_notebook_config.py for security reasons.

## Running the Server

Run the following commands in three separate terminal windows:

```bash
make run_notebook
make run_server
make run_celery
```

## Initial Setup

1. Create a superuser:

```bash
python manage.py createsuperuser
```

2. Access the admin panel at http://localhost:8000/admin and create a new user.

3. Manually create clients, users, and client users in the admin page.


## Usage

1. Upload datasets through the user interface.
2. Configure and run AI models for benchmarking.
3. View and compare results across different models and datasets.


## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

##License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

Dr. Quan Thanh Tho for supervision and guidance
FPT University for providing resources and support











