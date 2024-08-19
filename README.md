# Mobile Reviewer

This is a django backend for my previous idea of using LLM to summarize the youtube video caption. I wanted to keep this as separated bcz I have integrated static files
and this can run with websites rather that CLI. Here is the link to simple CLI (https://github.com/itsashishrath/MobileReviewer)

## Table of Contents
1. [Project Title and Description](#project-title-and-description)
2. [Table of Contents](#table-of-contents)
3. [Installation](#installation)
4. [Usage](#usage)

## Project Title and Description
**Mobile Reviewer**: This project automates the process of gathering and analyzing YouTube reviews for a specific phone model, summarizing the pros and cons based on video captions and generating a professional review using an LLM.

## Installation
Follow these steps to install and run the Mobile Reviewer project on your local machine:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/itsashishrath/ReviewitBackend.git
    cd ReviewitBackend
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up API Keys**:
    - Obtain a YouTube Data API key from [Google Cloud Console](https://console.cloud.google.com/).
    - Obtain an API key for Google Generative AI from [Google AI](https://ai.google.dev/).
    - Set up the environment variables:

        On **Windows**:
        ```cmd
        setx GOOGLEAPIKEY "your_youtube_data_api_key"
        setx GEMINISTUDIOKEY "your_google_ai_api_key"
        ```

        On **macOS/Linux**:
        ```bash
        export GOOGLEAPIKEY='your_youtube_data_api_key'
        export GEMINISTUDIOKEY='your_google_ai_api_key'
        ```

## Usage
1. **Run the Application**:
    ```bash
    python manage.py runserver
    ```

2. **Example Usage**:
    - The application will open at (http://localhost:8000)
    - Enter the name of the mobile in the searchbar
    - It will then fetch captions from the top 5 YouTube videos related to that phone model.
    - Using the LLM, it generates a detailed review with citations to the respective videos.


Feel free to explore and modify the code to suit your needs. Contributions are welcome!
