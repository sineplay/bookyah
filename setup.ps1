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

# PowerShell Script for BOOKYAH - Asset Reservation Application Setup

# Check if Python is installed and available
$pythonCommands = @("python3", "python", "py") # List of possible Python command names
$requiredVersion = "3.8"
$pythonCommand = $null # Initialize the variable to store the command
$pythonVersion = $null

foreach ($cmd in $pythonCommands) {
    # Check each command to see if it executes correctly
    try {
        $versionOutput = & $cmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        if ($versionOutput) {
            Write-Host "Found Python command $cmd with version $versionOutput"
            if ([version]$versionOutput -ge [version]$requiredVersion) {
                $pythonCommand = $cmd
                $pythonVersion = $versionOutput
                break
            } else {
                Write-Host "$cmd version $versionOutput is less than required $requiredVersion."
            }
        }
    } catch {
        Write-Host "$cmd cannot execute properly."
    }
}

if (-not $pythonCommand) {
    Write-Error "Python is not installed or not found in PATH. Please install Python and try again."
    exit
}

# Check for Python version 3.8 or newer
$version = & $pythonCommand -c 'import sys; print(sys.version_info.major, sys.version_info.minor)'
$versionArray = $version -split " "
if ([int]$versionArray[0] -lt 3 -or ([int]$versionArray[0] -eq 3 -and [int]$versionArray[1] -lt 8)) {
    Write-Error "Detected Python version $($versionArray[0]).$($versionArray[1]), but Python 3.8 or newer is required."
    exit
}

Write-Host "Using Python command: $pythonCommand with version $($versionArray[0]).$($versionArray[1])"

Write-Host "Creating virtual environment..."
& $pythonCommand -m venv venv

Write-Host "Activating virtual environment..."
. ".\venv\Scripts\Activate.ps1"

Write-Host "Installing requirements..."
pip install -r requirements.txt

if (Test-Path "mycal/.env.example") {
    Write-Host "Renaming .env.example to .env..."
    Rename-Item "mycal/.env.example" "mycal/.env"

    Write-Host "Generating a Django secret key..."
    $secretKey = & $pythonCommand -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    $content = Get-Content "mycal/.env" -Raw
    $content = $content -replace 'YOUR_RANDOMLY_GENERATED_KEY_SEE_README', $secretKey
    Set-Content "mycal/.env" -Value $content
} else {
    Write-Host ".env.example does not exist. Skipping rename and key generation."
}

Write-Host "Running migrations..."
Set-Location mycal
& $pythonCommand manage.py makemigrations authentication booking
& $pythonCommand manage.py migrate

Write-Host "Creating superuser..."
$email = Read-Host "Enter superuser email"
$firstName = Read-Host "Enter superuser first name"
$lastName = Read-Host "Enter superuser last name"

$correct = $false
do {
    $password = Read-Host "Enter superuser password" -AsSecureString
    $confirmPassword = Read-Host "Confirm superuser password" -AsSecureString
    $correct = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)) -eq [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($confirmPassword))
    if (-not $correct) {
        Write-Host "Passwords do not match, please try again."
    }
} while (-not $correct)

$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

# Using Django shell to create superuser
& $pythonCommand manage.py shell -Command "
from django.db.models.signals import post_save;
from django.contrib.auth import get_user_model;
from authentication.signals import send_welcome_email;
User = get_user_model();
post_save.disconnect(send_welcome_email, sender=User);
User.objects.create_superuser(email='$email', password='$plainPassword', first_name='$firstName', last_name='$lastName', is_staff=True, email_verified=True);
post_save.connect(send_welcome_email, sender=User);
"

Write-Host "Setup complete! Activate the virtual environment (.\venv\Scripts\Activate.ps1), change your directory to the mycal folder (Set-Location mycal), and run the server with: $pythonCommand manage.py runserver"
