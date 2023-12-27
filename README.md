# Pizza-Ordering-Website-with-Djnago\
This project aims to provide a user-friendly platform for ordering pizzas online. Users can customize their pizza orders by choosing from a variety of toppings, crust types, and sizes. The website also includes features for user authentication,  and an admin panel for managing orders and menu items.

Create Virtual Environment:
python -m venv venv

Activate Virtual Environment:
venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate

Install Dependencies:
pip install -r requirements.txt

Run Migrations:
python manage.py migrate

Create Superuser (Admin):
python manage.py createsuperuser

Run the Development Server:
python manage.py runserver

Access the Website:
Open your web browser and go to http://localhost:8000/

Access the Admin Panel:
Visit http://localhost:8000/admin/ and log in with the superuser credentials.
