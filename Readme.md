<h1 align="center">
  <img alt="cgapp logo" src="https://lh6.googleusercontent.com/rU8dZ0x67y63AeujFhM79UG_I3ZagEqTmDffagrUVuBI5eXPHtW2Z7zP1KU1MLKtl0wU5eNS_QHU-9v3GUJgxlKYeAR1yKADY8xCj7xMrpL8z9Rr2Zde9_OGsmXTigvBr7DEWggV" width="224px"/><br/>
 Inventory management for Shop (POS)
</h1>
<p align="center"> <b>Python, Django ORM</b> (backend) , <b>database</b> (Postgres)!</p>

## 📖 POS 

It is a Inventory management system for Shop. The inventory management system is useful for tracking huge shipments of stocks, monitoring purchases, order, sell, preparing invoice and production. This project reduces the risk of human error using an automated inventory management system.

🔔 `Note`If you interested to run it from locally with database and .env properly configured
>Example: \
> createvirtualenv env \
> env/Scripts/activate.bat
> pip install -r requirements.txt
> cd pos
> python manage.py migrate
> python manage.py runserver
> 
>> 
 🤾‍♂ `Configure database with the settings:`
DB_HOST=localhost \
DB_PORT=5432 \
DB_USER=postgres \
DB_PASSWORD=12345 \
DB_NAME=posapp_db

🤾‍♂️ `Let's visit localhost:port and expolre my website POS`
# 📋 Project Feature
 - Three types of user - superuser, admin, staff
 - Product Management
 - Monitor and Category Products
 - Manage Product Pricing
 - Sales and Stocks Management
 - Monitor Purchasing Transaction
 - Manage reservations and Orders
 - Revenue and Expenses Management
 - Discount until a threshold price
 - suppliers, employees, and customer management



# 📋 Folder Structure 
```
Pos
├── core
│    ├── migrations
│    ├── test 
│    ├── admin.py
│    ├── apps.py
│    ├── modules.py
├── dashboard
│    ├── migrations 
│    ├── tamplates
│    ├── __init__.py
│    ├── admin.py
│    ├── apps.py
│    ├── modules.py
│    ├── tests.py
│    ├── urls.py
│    ├── views.py
├── investor
│    ├── migrations 
│    ├── tamplates
│    ├── __init__.py
│    ├── admin.py
│    ├── apps.py
│    ├── forms.py
│    ├── manager.py
│    ├── models.py
│    ├── tests.py
│    ├── urls.py
│    ├── views.py            
├── liabilities
│    ├── migrations 
│    ├── tamplates
│    ├── __init__.py
│    ├── admin.py
│    ├── apps.py
│    ├── forms.py
│    ├── manager.py
│    ├── models.py
│    ├── tests.py
│    ├── urls.py
│    ├── views.py
│── media
│    ├── profile_images           -All profile picture of staffs
│── product 
│── scripts
│── settings
│── static
│    ├── common 
│    ├── product
│    ├── site_image
│    ├── user
│── template_tags
│── templates
│    ├── test 
│    ├── admin.py
│    ├── apps.py
│    ├── modules.py
│── user
│    ├── migrations 
│    ├── tamplates
│    ├── __init__.py
│    ├── admin.py
│    ├── apps.py
│    ├── forms.py
│    ├── tests.py
│    ├── urls.py
│    ├── views.py
│── .gitignore
│── manage.py                    
│── requirements.txt             - requirements file for install configuration  
│── myapp_models.png             - Demo picture
```
