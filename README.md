# Muhtasib Watch - Email Security Analyzer

Muhtasib Watch is a comprehensive email security analyzer application that can detect phishing attempts, analyze DKIM/SPF headers, and scan attachments for potential malware. This tool is designed to help users and administrators ensure the security and integrity of their email communications.

## Table of Contents
- [Project Features](#project-features)
- [Installation](#installation)
- [Dataset Preparation](#dataset-preparation)
- [Training the Model](#training-the-model)
- [Usage](#usage)
- [How to Run the Application](#how-to-run-the-application)
- [Directory Structure](#directory-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Project Features
1. **Phishing Email Detection**:
   - Analyzes email text to detect if it is a phishing attempt using a pre-trained machine learning model.
2. **DKIM and SPF Header Analysis**:
   - Validates the integrity of email headers to ensure the sender's authenticity.
3. **Attachment Scanning**:
   - Downloads and scans email attachments using ClamAV to detect malware.
4. **URL Redirection Checker**:
   - Inspects URLs for multiple redirects and checks against VirusTotal's database for potential threats.

## Installation
Follow these steps to set up the application on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Hamzah2002/Muhtasib-Watch.git
   cd Muhtasib-Watch
