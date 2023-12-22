Law Firm Invoice Generator

The task is to develop a web application for a leading law firm in Ghana to streamline their revenue collection process. The firm operates on a billable rate system where lawyers submit their timesheets, and invoices are generated based on the total hours worked.
Problem Statement

Lawyers submit their timetables in CSV format with the following structure:

csv

Employee ID, Billable Rate(per hour), Project, Date, Start Time, End Time
1, 300, Google, 2019-07-01, 09:00, 17:00
2, 100, Facebook, 2019-07-01, 11:00, 16:00

The goal is to design a web application that takes this timesheet as input and automatically generates invoices for each company.
Solution
Features

    Accepts timesheets in CSV format.
    Calculates the total number of hours, unit price, and cost for each employee.
    Provides a summary of the total cost for each company.
    Generates invoices for each company.

Usage

    Upload the timesheet in CSV format.
    The application will process the data and generate invoices.
    Invoices will be displayed with details such as Employee ID, Number of Hours, Unit Price, and Cost.
    The total invoice amount for each company is calculated and presented.

Technologies Used

    Python
    Flask (Web Framework)
    Pandas (Data Manipulation)
    HTML/CSS (Frontend)

How to Run

    Clone this repository.
    Install the required dependencies (pip install -r requirements.txt).
    Run the Flask application (python app.py).
    Access the web application in your browser (http://localhost:5000).
