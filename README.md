# Trainee App

## Introduction
Welcome to Trainee! This is a personal project that I decided to take up to learn about full-stack development and address a specific inconvenience I was having.

## Overview
Trainee is a web app designed to help soccer players find training partners based on specific training focuses of interest. Users are given a Player, inspired from the video game FIFA, where they can track their stats and show off to others. 

## Features
- **Player Profile:** Users can track and share their progress with a virtual Player profile that updates as a user trains more and more.
- **Session Management:** Users can create and join training sessions specifying the date, time, location, and focus of the session.
- **User Authentication:** Secure user authentication system using Flask-Login and bcrypt for password hashing.
- **Join Sessions:** Users can join sessions created by other users and indicate their interest in participating.

## Installation
Clone the repository: 
```
git clone https://github.com/yaitbella/trainee.git
```
Navigate to the project directory: 
```
cd traineewebapp
```
Create a virtual environment: See [Python Docs](https://docs.python.org/3/library/venv.html)
```
python3 -m venv myenv
```
Activate the virtual environment:
- On Windows: 
myenv\Scripts\activate`
- On macOS and Linux: 
`source myenv/bin/activate`
    
Install dependencies: 
```
pip install -r requirements.txt
```
Set up the database: 
```
python3 dbStart.py
```
Run the application: 
```
python3 run.py
```


## Usage
Register an account on the app.
Browse existing training sessions or create your own.
Join sessions that match your interests and availability.
Connect with other players, train together, and improve your game!

## Technologies Used
Python, Flask, SQLAlchemy, Bootstrap

## Contributors
Yussef Ait-Bella - Lead Developer

## Acknowledgements
Special thanks to Corey Schafer and his brilliant videos on youtube. I followed his tutorial (linked below) to help build skeleton of Trainee
https://www.youtube.com/watch?v=MwZwr5Tvyxo
