# Muhtasib Watch - Email Security Analyzer

Muhtasib Watch is a comprehensive email security analyzer that detects phishing attempts, analyzes DKIM/SPF headers, and scans attachments for potential malware. It is designed to help users and administrators secure their email communications.

## Table of Contents
- [Project Features](#project-features)
- [Installation](#installation)
- [How to Run the Application](#how-to-run-the-application)
- [Technologies Used](#technologies-used)

## Project Features
1. **Phishing Email Detection**:
   - Analyzes email text to detect phishing attempts using a pre-trained machine learning model.
   
2. **DKIM and SPF Header Analysis**:
   - Validates email headers to ensure sender authenticity.

3. **Attachment Scanning**:
   - Scans local files, downloadable links, Gmail attachments, and Outlook attachments using ClamAV for malware detection.

4. **URL Redirection Checker**:
   - Inspects URLs for multiple redirects and checks against VirusTotal's database for potential threats.

---

## Installation

### **Step 1: Download the Installer**
- Install **MuhtasibWatchInstaller.exe** located in the `Output` directory of this repository.

### **Step 2: Install ClamAV (If Required)**
- If you plan to use the Gmail attachment scanning feature, **you must install ClamAV** from the official website:  
  [https://www.clamav.net/](https://www.clamav.net/)

---

## How to Run the Application

1. **Launch the Application**:
   - After installation, run `Muhtasib Watch` from the desktop or Start Menu.

2. **Using the Features**:
   - **Phishing Analysis**: Paste the email text and click "Analyze Email."
   - **DKIM/SPF Analysis**: Paste email headers and click "Check DKIM/SPF."
   - **Attachment Scanning**: 
     - Paste a downloadable link or email attachment URL and click "Scan Attachments."
   - **URL Checking**: Paste a URL and click "Check URL."

---

## Technologies Used
- **Python**: Backend development.
- **PyQt5**: GUI framework.
- **Scikit-learn**: Machine learning model for phishing detection.
- **ClamAV**: Malware detection engine.
- **VirusTotal API**: URL reputation checking.
- **Inno Setup**: Installer creation.

---

Let me know if you need further modifications!
