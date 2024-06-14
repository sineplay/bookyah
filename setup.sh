# BOOKYAH - Asset Reservation Application
# Copyright (C) 2024 Sineplay Studio, LLC
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The LICENSE file describes the conditions under which this software
# may be distributed.

#!/bin/bash

# Check if Python is installed and available
if ! command -v python &> /dev/null
then
    echo "Python is not installed or not found in PATH. Please install Python and try again."
    exit 1
fi

# Navigate to the correct directory (if necessary)
# Uncomment the next line if the script is not run from inside the project directory
# cd path/to/bookyah

echo "Creating virtual environment..."
python -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

if [ -f "mycal/.env.example" ]; then
    echo "Renaming .env.example to .env..."
    mv mycal/.env.example mycal/.env

    echo "Generating a Django secret key..."
    # This command uses Python to generate a secret key and replace the placeholder in the .env file
    SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    sed -i "s/YOUR_RANDOMLY_GENERATED_KEY_SEE_README/$SECRET_KEY/" mycal/.env
else
    echo ".env.example does not exist. Skipping rename and key generation."
fi

echo "Running migrations..."
cd mycal
python manage.py makemigrations authentication booking
python manage.py migrate

echo "Creating superuser..."
# Interactive superuser creation
read -p "Enter superuser email: " email
read -p "Enter superuser first name: " first_name
read -p "Enter superuser last name: " last_name

# Password verification loop
while true; do
    read -s -p "Enter superuser password: " password
    echo
    read -s -p "Confirm superuser password: " password2
    echo
    if [ "$password" = "$password2" ]; then
        break
    else
        echo "Passwords do not match, please try again."
    fi
done

# Using Django shell to create superuser
echo "from django.db.models.signals import post_save;
from django.contrib.auth import get_user_model;
from authentication.signals import send_welcome_email;
User = get_user_model();

post_save.disconnect(send_welcome_email, sender=User);

User.objects.create_superuser(email='$email', password='$password', first_name='$first_name', last_name='$last_name', is_staff=True, email_verified=True);

post_save.connect(send_welcome_email, sender=User);" | python manage.py shell

echo "Setup complete! Activate the virtual environment (source venv/bin/activate), change your directory to the mycal folder (cd mycal), and run the server with: python manage.py runserver"
