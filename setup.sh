#!/bin/bash

# Navigate to the correct directory (if necessary)
# Uncomment the next line if the script is not run from inside the project directory
# cd path/to/bookyah

echo "Renaming .env.example to .env..."
mv mycal/.env.example mycal/.env

echo "Creating virtual environment..."
python -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Generating a Django secret key..."
# This command uses Python to generate a secret key and replace the placeholder in the .env file
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
sed -i "s/YOUR_RANDOMLY_GENERATED_KEY_SEE_README/$SECRET_KEY/" mycal/.env

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
echo "from django.contrib.auth import get_user_model; User = get_user_model();
User.objects.create_superuser(username='$email', email='$email', password='$password', first_name='$first_name', last_name='$last_name')" | python manage.py shell

echo "Setup complete! Change your directory to the mycal folder (cd mycal) and run the server with: python manage.py runserver"
