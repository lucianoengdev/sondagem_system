# Geotechnical Borehole Manager (Sondagem System)

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Status](https://img.shields.io/badge/status-In%20Development-orange.svg)
![Python](https://img.shields.io/badge/python-3.x-yellow.svg)

## 📌 What is it?
This project is a specialized web application designed for Transport Engineering, specifically focusing on soil geotechnics for road infrastructure. It automates the processing of geotechnical borehole logs (furos de sondagem), which are typically received as scattered PDF files.

The system acts as a centralized platform to import, clean, and analyze soil sample data, replacing the error-prone and time-consuming process of manual data entry into spreadsheets.

## ⚙️ What it does
* **Batch PDF Import:** Accepts folders containing multiple PDF borehole reports and automatically identifies relevant files.
* **Intelligent Extraction:** Uses a custom parsing engine to read complex, non-standardized tables from PDFs, handling merged headers, footers, and "ghost lines" (formatting inconsistencies).
* **Visual Consolidation:** Renders extracted data in a structured, Excel-like web interface that mimics the original engineering report format.
* **Advanced Filtering (Data Cleaning):** Allows engineers to apply boolean logic filters. These filters utilize a robust tag system to manage inclusion/exclusion criteria dynamically.
* **Session Persistence:** Keeps data and filters active while navigating between different modules of the application.

## 🛠️ Technologies Used
* **Backend:** Python 3, Flask (Web Framework).
* **Data Processing:** PDFPlumber (PDF extraction), Pandas (Data manipulation), RegEx.
* **Frontend:** HTML5, CSS3 (Bootstrap 5), JavaScript (Vanilla for Modal/API interactions).
* **Architecture:** Modular MVC-style structure (Routes, Utils packages).

## 🎯 Project Ambition
The goal is to build a comprehensive Geotechnical Decision Support System. We aim to evolve this tool from a simple data extractor into a full analytical suite that can:
1.  Perform automatic statistical analysis of the subgrade.
2.  Generate linear stratigraphy graphs.
3.  Calculate soil substitution requirements automatically.
4.  Export consolidated reports for final engineering designs.

## 📍 Current Stage
**Version 1.1.0 (Stable Alpha)**
* ✅ **Core Engine:** PDF extraction logic is polished and handles edge cases (empty lines, multi-page tables).
* ✅ **Data Cleaning:** The "Filter/Exclude" module is fully functional, allowing granular control over which samples enter the analysis phase.
* ✅ **UI/UX:** Navigation between "Upload", "Print View", and "Analysis View" is implemented with data persistence.

## 🚧 Known Issues & Future Improvements
Currently, the extraction and filtering are working correctly. The immediate focus is on implementing the analytical modules.

**Features to be implemented (Buttons currently unconfigured):**
* [ ] **Generate Statistical Analysis:** Calculate Mean, Median, Standard Deviation, and Percentiles for selected soil properties.
* [ ] **Generate Linear Graph:** Visual representation of the boreholes along the road axis.
* [ ] **Generate Summary:** Create a consolidated executive summary table.
* [ ] **Generate Substitution:** Algorithm to calculate volume/depth of soil replacement needed based on engineering criteria.
* [ ] **Generate Moisture Interval:** Analysis of natural moisture vs. optimum moisture.

---
*Developed by a Transport Engineer(Luciano Faria) for Transport Engineers.*