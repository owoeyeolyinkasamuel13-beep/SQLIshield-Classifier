# SQL Injection Detection and Classification System Using Convolutional Neural Network

## Overview

This project presents a **Convolutional Neural Network (CNN)-based SQL Injection Detection and Classification System** developed as a final year project.

The system is designed to analyse SQL queries and determine whether they are **normal (benign)** or **malicious (SQL injection)**. The trained CNN model learns patterns from SQL query data and is integrated into a web-based application where users can submit queries for analysis.

The project focuses on using deep learning to improve the detection of SQL injection attacks and provide an additional layer of protection against malicious database queries.

---

## Project Objectives

The main objectives of the project are to:

* Collect legitimate and malicious SQL query data.
* Train a CNN-based model to detect SQL injection attacks.
* Evaluate the performance of the trained model.
* Develop a web-based interface for SQL injection detection.
* Deploy the trained CNN model within the web application.

---

## How the System Works

The system follows a series of steps to analyse submitted SQL queries:

```text
User submits SQL Query
        ↓
Data Pre-processing
        ↓
Tokenization
        ↓
Numerical Encoding
        ↓
Padding
        ↓
CNN Detection Model
        ↓
Classification
   ↙             ↘
Normal          Malicious

```

The query is first cleaned and converted into a numerical representation. The processed query is then passed to the CNN model, which analyses the learned patterns and produces a classification result.

---

## Dataset

The project uses a publicly available SQL query dataset obtained from **Mendeley Data**.

The dataset contains:

* **10,190,450 total SQL queries**
* **7,490,880 benign queries**
* **2,699,570 malicious SQL injection queries**

The dataset contains different SQL injection patterns alongside normal SQL queries.

### Dataset Categories

The project considers SQL injection categories including:

* None-Type
* Error-Based
* Time-Based
* Union-Based
* Boolean-Based
* Meta-Based
* Stacked-Queries-Based

Because the original dataset contained an imbalance between normal and malicious queries, **data balancing** was applied before model training.

---

## Data Pre-processing

Several preprocessing steps were performed before training the CNN model:

### 1. Data Cleaning

Duplicate and unnecessary records were removed to improve the quality of the dataset.

### 2. Data Balancing

The dataset was balanced to reduce the effect of the large difference between benign and malicious query samples.

### 3. Tokenization

SQL queries were converted into tokens so that the model could process individual query components.

### 4. Numerical Encoding

The tokens were converted into numerical representations suitable for machine learning.

### 5. Padding

SQL query sequences were converted to a consistent length before being supplied to the CNN model.

The dataset was divided into:

* **70% Training**
* **15% Validation**
* **15% Testing**

---

## Machine Learning Model

The project uses a **Convolutional Neural Network (CNN)** for SQL injection classification.

The CNN learns patterns within SQL queries that can indicate malicious behaviour. Instead of depending entirely on manually created rules, the model learns relevant patterns from the training data.

The CNN architecture contains components such as:

* Input layer
* Embedding layer
* Convolutional layer
* Pooling layer
* Fully connected layer
* Dropout
* Output layer

The model was trained using supervised learning and the Adam optimizer.

---

## Model Evaluation

The trained model was evaluated using standard classification metrics:

| Metric    |     Result |
| --------- | ---------: |
| Accuracy  | **86.00%** |
| Precision | **86.89%** |
| Recall    | **85.96%** |
| F1-Score  | **85.92%** |

### Accuracy

The model achieved an accuracy of **86%**, meaning that the system correctly classified a large proportion of the evaluated SQL queries.

### Precision

The model achieved a precision of **86.89%**, indicating its ability to correctly identify queries classified as malicious.

### Recall

The recall score was **85.96%**, showing the model's ability to identify malicious SQL injection queries present in the test data.

### F1-Score

The model achieved an F1-score of **85.92%**, providing a balance between precision and recall.

---

## Web Application

The trained model was integrated into a web-based application.

The application provides an interface where a user can:

1. Enter an SQL query.
2. Submit the query for analysis.
3. Send the query to the backend.
4. Process the query using the trained CNN model.
5. Receive the classification result.

The system consists of the following major components:

```text
Web Interface
     ↓
Flask Backend / API
     ↓
Pre-processing
     ↓
CNN Model
     ↓
Classification Result
     ↓
System Log
```

The web interface was developed using **HTML and CSS**, while the backend was implemented using **Python and Flask**.

---

## Technologies Used

### Programming Language

* Python

### Machine Learning & Data Processing

* TensorFlow
* Keras
* NumPy
* Pandas
* Scikit-learn

### Web Development

* HTML
* CSS
* JavaScript
* Flask

### Development Tools

* Visual Studio Code
* Jupyter Notebook
* MySQL / MySQL Workbench
* Git & GitHub

---

## Project Structure

A typical project structure is shown below:

```text
SQL-Injection-Detection/
│
├── app.py
├── model/
│   └── trained_model.h5
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   └── js/
│
├── dataset/
│   └── dataset.csv
│
├── notebooks/
│   └── model_training.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore
```

> File and folder names may differ depending on the final repository structure.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```

The application can then be accessed through the local Flask server.

---

## Example Workflow

A user submits an SQL query through the web interface.

The system processes the query and passes it through the trained CNN model.

The model produces a classification such as:

```text
Query: SELECT * FROM users WHERE username='admin'

Result: NORMAL
```

or:

```text
Query: SELECT * FROM users WHERE username='' OR '1'='1'

Result: SQL INJECTION DETECTED
```

The application can also record detected activity for security monitoring.

---

## Security Purpose

The purpose of this project is to demonstrate how deep learning can be applied to SQL injection detection.

The system is intended as a **research and academic cybersecurity project** and should not be considered a complete replacement for established database security practices such as:

* Parameterized queries
* Prepared statements
* Input validation
* Secure coding practices
* Proper database access controls
* Web application security testing

---

## Project Results

The completed system demonstrates that a CNN model can be used to classify SQL queries based on patterns learned from labelled data.

The final evaluation produced:

**86% Accuracy | 86.89% Precision | 85.96% Recall | 85.92% F1-Score**

The trained model was subsequently integrated into a web-based application for practical testing and interaction.

---

## Future Improvements

Possible improvements to the system include:

* Increasing the diversity of the training dataset.
* Improving detection of previously unseen SQL injection patterns.
* Comparing the CNN model with additional machine learning and deep learning models.
* Improving real-time database integration.
* Adding more detailed attack classification.
* Improving the web application's monitoring and reporting features.
* Deploying the system in a larger production-like environment.

---

## Academic Project

This project was developed as a **Final Year Project in Cyber Security**.

**Project:** SQL Injection Detection and Classification System Using Convolutional Neural Network

**Area:** Cybersecurity / Artificial Intelligence / Machine Learning / Database Security

---

## Disclaimer

This project was developed for **educational, research, and cybersecurity demonstration purposes**.

It should only be tested with authorised systems, applications, datasets, and environments. Do not use the system to perform unauthorised attacks or access systems without permission.

---

## Author

**Olayinka Samuel Owoeye**

Cyber Security

Redeemer's University

---

## License

This project is intended primarily for academic and educational purposes. Please refer to the repository for the applicable license and usage conditions.
