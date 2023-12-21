from flask import Flask, Response, render_template, request, redirect, flash
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
from dateutil.parser import parse

# Flask application instance
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '0987654321'

# Global variable to store DataFrame
uploaded_df = None

# CSV upload and Validation Function
def validate_csv(file_content):
    try:
        # Read CSV file using pandas
        df = pd.read_csv(StringIO(file_content))
        
        # Check if required columns are present
        required_columns = ['Employee ID', 'Billable Rate(per hour)', 'Project', 'Date', 'Start Time', 'End Time']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            return False, f"Missing columns: {', '.join(missing_columns)}"

        # Validate data types for numeric columns
        numeric_columns = ['Billable Rate(per hour)', 'Hours']
        for col in numeric_columns:
            if col in df.columns:
                try:
                    # Attempt to convert the column to numeric
                    df[col] = pd.to_numeric(df[col], errors='raise')
                except pd.errors.OutOfBoundsDatetime:
                    return False, f"Invalid value in column '{col}': Out of bounds datetime"
                except pd.errors.OverflowError:
                    return False, f"Invalid value in column '{col}': Overflow error"
                except pd.errors.PandasError as e:
                    return False, f"Invalid value in column '{col}': {str(e)}"
        

        # Store the DataFrame in the global variable
        global uploaded_df
        uploaded_df = df

        return True, None

    except pd.errors.ParserError as e:
        return False, f"Invalid CSV format: {str(e)}"

# Routing for uploading timesheet
@app.route('/', methods=['GET', 'POST'])
def upload_timesheet():
    global uploaded_df

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            file_content = file.read().decode('utf-8')

            # Validate the CSV file
            is_valid, error_message = validate_csv(file_content)

            if is_valid:
                flash('File uploaded successfully!', 'success')
            else:
                flash(error_message, 'error')

    return render_template('index.html')

# Invoice generation function
def generate_invoices():
    global uploaded_df

    if uploaded_df is None:
        return []  # No CSV uploaded yet

    invoices = []
    grouped_projects = uploaded_df.groupby('Project')

    previous_project = None
    for project_name, project_df in grouped_projects:
        total_cost = 0

        for index, row in project_df.iterrows():
            hours_worked = int((parse(row['End Time']) - parse(row['Start Time'])).total_seconds() / 3600)
            cost = int(row['Billable Rate(per hour)'] * hours_worked)  
            total_cost += cost

            # Create invoice dictionary
            invoice = {
                'Project Name': project_name,
                'Employee ID': row['Employee ID'],
                'Number of Hours': hours_worked,
                'Unit Price': row['Billable Rate(per hour)'],
                'Cost': cost,
            }

            if project_name != previous_project:
                # If a new project, append a new invoice
                invoices.append(invoice)
            else:
                # If the same project, update the last invoice's cost and total
                invoices[-1]['Cost'] += cost
                invoices[-1]['Total Invoice Amount'] = total_cost

        previous_project = project_name

    return invoices

# Routing for generating invoices
@app.route('/generate_invoices')
def generate_invoices_route():
    invoices = generate_invoices()
    return render_template('invoices.html', invoices=invoices)  # Pass invoices as a template argument


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
