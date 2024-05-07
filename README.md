Vendor Management System
Vendor Management System (VMS) is a Django-based application is designed to efficiently manage vendor profiles, track purchase orders, and calculate performance metrics for vendors. 
This README will guide you through setting up and testing the system.

Table of Contents
Overview
Features
Setup Instructions
API Endpoints
Token-Based Authentication
Testing
Conclusion
Overview

Features
Vendor Profile Management: Create, retrieve, update, and delete vendor profiles.
Purchase Order Tracking: Create, retrieve, update, and delete purchase orders. Track details such as PO number, order date, items, and quantity.
Vendor Performance Evaluation: Calculate performance metrics for vendors including on-time delivery rate, quality rating average, response time, and fulfillment rate.
Setup Instructions
Follow these steps to set up the Vendor Management System:

Ensure Python and pip are installed.
bash
Copy code
python --version && pip --version
Setup a virtual environment for the project.
bash
Copy code
python -m venv env
Activate the virtual environment.
On Windows:
bash
Copy code
env\Scripts\activate
Clone the repository.
bash
Copy code
git clone https://github.com/tintutom/Vendor_management_system.git
Navigate to the project directory.
bash
Copy code
cd Vendor_management_system
Install dependencies.
bash
Copy code
pip install -r requirements.txt
Apply migrations.
bash
Copy code
python manage.py migrate
Run the development server.
bash
Copy code
python manage.py runserver
Access the API at http://localhost:8000/api/.
API Endpoints
The system exposes the following API endpoints:

Vendor Profile Management: CRUD operations for vendor profiles.
Purchase Order Tracking: CRUD operations for purchase orders.
Vendor Performance Evaluation: Retrieve performance metrics for vendors.
For detailed endpoint documentation, refer to the API Endpoints section in this README.

Token-Based Authentication
To secure the API endpoints, token-based authentication is implemented using Django REST Framework's TokenAuthentication. Follow these steps to set up authentication:

Create an admin user.
bash
Copy code
python manage.py createsuperuser
Generate a token for the user.
Using Django Admin interface: http://localhost:8000/admin/

Conclusion
Vendor Management System provides a robust solution for tracking vendor profiles, purchase orders, and evaluating vendor performance metrics. If you encounter any issues during setup, feel free to reach out for assistance.

Thank you for using the Vendor Management System!
