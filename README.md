# Detecting Fraudulent Job Postings

## Project Background
Fraudulent job postings exploit job seekers by presenting deceptive opportunities, often with malicious intent. With the rise of online job fraud, fake job postings have become a significant issue, leading to financial losses and damaging the reputation of companies. Manual methods for detecting fake job posts are insufficient and inefficient. Automated, scalable solutions are necessary to effectively prevent fraud in the job market. This project aims to develop a machine learning model capable of analyzing job post data to accurately detect fake postings, enhancing the reliability of online recruitment. By leveraging machine learning and extensive exploratory data analysis (EDA), the project aims to identify patterns and anomalies indicative of fraudulent postings. A robust detection system will protect millions of job seekers from scams, promote trust in job platforms, and safeguard companies from reputation risks.

## Project Usefulness
This initiative holds immense value for job seekers and platforms hosting job opportunities:
- **Job Seeker Protection**: Enhances trust in job boards by identifying and eliminating scams.
- **Platform Credibility**: Improves the reputation of job hosting platforms by maintaining genuine job opportunities.
- **Fraud Insights**: Offers data-driven insights into common fraudulent tactics, aiding preventative measures.

## Dataset Infromation
- The project uses a dataset of 18,000 job postings.
- The Employment Scam Aegean Dataset (EMSCAD) is publicly available by the University of the Aegean and includes labeled data, training machine learning models. `http://emscad.samos.aegean.gr/`
- Features like job title, description, location, and company profile are used to classify job postings as real or fake.
- The dataset provides a representative mix of legitimate and fraudulent posts, which is essential for developing an accurate classifier.


## Technical Workflow

![Picture3](https://github.com/user-attachments/assets/2f08a503-86cf-4131-bfa7-750a0ead6e0a)

### 1. Data Preprocessing
- **Libraries Used**: The project employs libraries such as `pandas`, `numpy`, `statsmodels`, `seaborn`, `matplotlib`, and `sklearn` for data processing and visualization.
- **Handling Missing Values**:
  - Addressed missing data with statistical techniques like Z-tests to ensure significant and reliable imputations.
- **Text Cleaning**:
  - Removed HTML tags using `BeautifulSoup`.
  - Cleaned URLs, special characters, and numerical values using regular expressions.
  - Converted text to lowercase for case normalization.
  - Tokenized and lemmatized text using `nltk`'s `WordNetLemmatizer`.
  - Removed stop words for improved feature extraction.

### 2. Exploratory Data Analysis (EDA)
- **Visualization**:
  - Utilized `matplotlib` and `seaborn` for plotting trends and distributions in the dataset.
  - Comparision of 'Unknown' rates in real vs fake job postings.
  - Map visualization inidicating no of real and fake job postings wrt. countries in the dataset (`https://my-map-folium.tiiny.site/`).
  - Generated word clouds to identify common keywords in fraudulent job postings.
- **Feature Insights**:
  - Analyzed the distribution of features like department, employment type, and required education.
  - Z-tests were performed to verify differences in missing value rates between real and fake job postings.

### 3. Sampling and Class Imbalance
- **Over-Sampling & Under-Sampling**:
  - Implemented **SMOTE** (Synthetic Minority Over-sampling Technique) for generating synthetic samples.
  - Combined with **Tomek Links** to remove borderline samples, balancing the dataset more effectively.

### Machine Learning

#### 1. Feature Engineering
- **Imputation**: Missing values were replaced with empty strings to ensure compatibility with text-based features.
- **TF-IDF Vectorization**:
  - Applied `TfidfVectorizer` to convert textual data into numerical features, capturing term importance.

#### 2. Class Balancing
- The dataset is highly imbalanced, with 97.8% non-fraudulent (0) and only 2.2% fraudulent (1) instances. 
- Utilized a combination of **SMOTE (Synthetic Minority Over-sampling Technique)** and **Tomek Links** to handle class imbalance:
  - SMOTE was used to create synthetic samples for the minority class.
  - Tomek Links removed overlapping samples, improving separation between classes.

#### 3. Models
- **Algorithms Tested**:
  - Logistic Regression
  - Random Forest
  - K-Nearest Neighbors (KNN)
  - Naive Bayes
  - Multi-layer Perceptron (MLP)
- **Pipeline**:
  - Built end-to-end pipelines using `sklearn.pipeline.Pipeline` and `imblearn.pipeline.Pipeline`.
  - Steps included imputation, scaling, and modeling for streamlined experimentation.

#### 4. Evaluation Metrics
- Focused on:
  - **Precision**: To minimize false positives (incorrectly classifying real jobs as fraudulent).
  - **Recall**: To ensure fraudulent job postings are accurately detected.
  - **F1-Score**: For a balanced assessment of precision and recall.
  - **ROC-AUC, PR-AUC and Learning curve**: To evaluate the model's performance across various thresholds.
 
#### 5. Model Analysis
- **Top Performers**: Logistic Regression, Random Forest, and Naive Bayes consistently achieved high accuracy (~98-99%), with balanced precision, recall, and F1-scores. These models are robust, generalize well, and exhibit minimal bias and variance.
- **Other Models**:
  - **MLP**: Near-perfect performance but computationally intensive, suitable for complex, non-linear data.
  - **k-NN**: Lower accuracy (86%), prone to overfitting and sensitive to noise, requiring preprocessing.
- **Conclusion**: Logistic Regression, Random Forest, and Naive Bayes are the most reliable and efficient for this dataset, balancing simplicity, accuracy, and generalization.
 
#### 6. Key Observations
- Despite rigorous tuning, synthetic data created by SMOTE cannot fully replace the diversity of real-world data.
- The best-performing combination was **SMOTE + Tomek Links** with Random Forest, achieving balanced precision and recall.

### Deployment

#### Backend Deployment
- **Flask Server**:
  - Hosted POST APIs for evaluating machine learning models with trained `.pickle` files.  
  - Predictive APIs handle requests and return predictions from Logistic Regression, Random Forest, and Naive Bayes models.  
  - Includes endpoints for serving static files (`index.html`) and retrieving preprocessed job features.
- **Steps to Set Up the Flask Server**:
  - Create and activate a Python environment:
    ```bash
    conda env create -f environment.yml
    conda activate naren_flask
    ```
    - The `environment.yml` file includes a `name` field, you can update it to customize the environment name.

  - Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

  - Configure AWS DynamoDB:
    - Set up your AWS credential file:
      - **Linux/Mac**: `~/.aws/credentials`
      - **Windows**: `%USERPROFILE%\.aws\credentials`
    - Update the DynamoDB table name in `flask_server.py` if necessary (default: `JobPostings`).

  - Run the Flask server:
    ```bash
    python flask_server.py
    ```
    - The server will be available at `http://127.0.0.1:5000` by default.

#### Frontend Deployment
- **Express Server**:
  - Hosted public files (e.g., `index.html`) and GET APIs using JSON.  
  - Optimized for handling high memory usage with the following command:
    ```bash
    node --max-old-space-size=4096 server.js
    ```

#### Data Preparation
- Ensure the following files are available in the `Machine_Learning/Models` directory:
  - **Trained Models**:
    - `logistic_regression_model.pkl`
    - `Naive_Bayes_model.pkl`
    - `Random_Forest_model.pkl`
  - **Preprocessed Data**:
    - `X_preprocessed.npy`

#### API Endpoints
- Flask server provides the following endpoints:
  - `/`: Serves the `index.html` file.
  - `/predict`: Accepts JSON input and returns predictions from multiple ML models.
  - `/features/<index>`: Fetches preprocessed feature data for a job posting based on its index.
  - `/api/jobs`: Fetches filtered job postings based on criteria like employment type, experience level, and education.
  - `/api/jobs/all`: Fetches all job postings from the DynamoDB table.
 
### Future Implications
- Being able to deal with class imbalance in a very effective way
- Experiment with more different kinds of classifier and nlp techniques to extract features, and building API's to extract features instead of mapping to able to deal with such kind of problem
- Creating pagination to retrieve particular sets of data from DynamoDB to make it user-friendly
- Creating user friendly features such as login, saving job profiles,etc similar other job portals.
- Create a flow to keep updating new genuine job postings to keep the users safe.

### Conclusion
This project addresses the critical issue of detecting fraudulent job postings, providing immense real-life value by protecting job seekers and enhancing the credibility of job platforms. One of the major challenges faced was the class imbalance in the dataset, which significantly impacted model performance. Despite employing various sampling techniques, SMOTE combined with Tomek Links emerged as the most effective method for balancing the dataset, both theoretically and practically. This approach improved separation between classes while retaining meaningful patterns, ensuring reliable predictions.

However, it is important to acknowledge that no synthetic data can fully replicate the diversity and complexity of real-world data. While SMOTE + Tomek Links enhanced model performance, the availability of authentic, balanced datasets remains crucial for training machine learning models to their full potential. This reinforces the need for better data collection practices, as real-world data would greatly improve classification accuracy and robustness in detecting fraudulent job postings.
