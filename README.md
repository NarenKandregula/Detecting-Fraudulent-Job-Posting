# Detecting Fraudulent Job Postings

## Project Background
Fraudulent job postings exploit job seekers by presenting deceptive opportunities, often with malicious intent. This project addresses the critical need for robust detection methods to classify job postings as real or fake. By leveraging machine learning and extensive exploratory data analysis (EDA), the project aims to identify patterns and anomalies indicative of fraudulent postings.

## Project Usefulness
This initiative holds immense value for job seekers and platforms hosting job opportunities:
- **Job Seeker Protection**: Enhances trust in job boards by identifying and eliminating scams.
- **Platform Credibility**: Improves the reputation of job hosting platforms by maintaining genuine job opportunities.
- **Fraud Insights**: Offers data-driven insights into common fraudulent tactics, aiding preventative measures.

## Technical Workflow

### 1. Data Preprocessing
- Addressed missing values using **Z-tests** to ensure statistically significant handling.
- Compared 'unknown' rates between real and fake postings to identify fraud-specific patterns.

### 2. Exploratory Data Analysis (EDA)
- **Descriptive Statistics**: Revealed trends and anomalies in data distributions.
- **Feature Distribution Analysis**: Highlighted tendencies like fraudulent postings often requiring less experience and simpler qualifications.
- **Class Imbalance**: A significant disparity exists between real and fake postings, underscoring the need for careful sampling techniques.

### 3. Modeling Approach
- Initial testing with algorithms like Logistic Regression and Decision Trees.
- Evaluated models using **precision**, **recall**, and **F1 scores** to ensure effective fraud detection.

### 4. Handling Class Imbalance
- Extensive trials on sampling methods led to adopting **SMOTE + TEMOK**, which provided the best results theoretically and practically.
- However, synthetic data has inherent limitations, and real-world data remains irreplaceable for creating robust models.

## Deployment Details

### Flask Server
Hosts POST APIs for evaluation using the trained `.pickle` file.

#### Setup:
```bash
conda activate naren_flask
pip install -r requirements.txt
python flask_server.py
