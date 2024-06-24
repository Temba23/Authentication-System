This project is for the authentication of the users. Simple JWT is applied to provide the security.

Packages Used:
- djangorestframework-simplejwt for the JWT Authentication
- django-all-auth for the Google OAuth 


Features:
- Google Authentication
- JWT Authentication
- Email for the OTP Pins
- Email messages to the user
- 2FA Authentication
- Alternative account recovery with Security Questions


To Install The Authentication System in your project : 

1. Clone the repository:
   - git clone https://github.com/Temba23/Authentication-System.git
2. Create env and install packages:
   - pip install -r requirements.txt
3. Create .env file and configure environment variables:
    CLIENT_ID=''
    CLIENT_SECRET=''
    SECRET_KEY=''
    EMAIL=''
    PASSWORD=''
4. Make migrations:
   - python manage.py makemigrations
   - python manage.py migrate
5. Run application:
   - python manage.py runserver

API Documentation View: 
   ![image](https://github.com/Temba23/Authentication-System/assets/126068369/0d3f1f34-4041-43d6-829e-86d7859ce16f)

Author : Temba Sherpa
