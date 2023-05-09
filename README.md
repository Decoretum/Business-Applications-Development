# Business-Applications-Development
This is a repository for the files in fulfillment of the <b> MSYS 42 </b> project.<br><br>
The real-world client of this project is China Global Steel Corporation. <br><br>
To obtain the settings.py and Django Secret Key, message [Gael Estrera](https://github.com/Decoretum).<br><br><br>

<h1> Systems Design and Development </h1> <br>
The Software System was designed by Chan Hyun, Gael Estrera, Jem Flores, Faustin Pua, and Alexis Miner. <br><br>

This Software System was developed by [Gael Estrera](https://github.com/Decoretum).

<br><br>
<h1> Tech Stack used </h1>

<b> Django </b> <br>
This framework utilizes Python and is used for both front-end and back-end. For this project, it is heavily used for back-end computing especially in session data, Model data analysis, and model instance creations. <br>

<b> Javascript </b> <br>
Plain Javascript will be used for client-side rendering of dynamic HTML changes such as dropdown quantity and total cost. This will also be used for User Interface and User experience. <br>

<b> SQL </b> <br>
SQL is used for creating and managing queries for functional back-end algorithms.

<br>

<h1> Supported Platforms and Browsers </h1>
The application can be used in Windows 10+ and MacOS 10.14.16 (Mojave) <br>
Google Chrome and Safari <br>

<h1> Database Architecture </h1>
https://app.diagrams.net/#G1PZlwUNpmm8cHGGkcCigoE5KhDCgxFYLc

<br><br>
<h1> Install MySQL </h1>
Install MySQL for MacOS: <br>
https://dev.mysql.com/doc/mysql-macos-excerpt/5.7/en/macos-installation.html <br><br>

Install MySQL for Windows: <br>
https://dev.mysql.com/downloads/installer/ <br><br>

Afterwards, setup a <b> permanent </b> environment path for MySQL.

<br><br>
<h1> Install Python </h1> 
Install Python 3.9.5 in Windows or Mac. <br><br>
Install Python for MacOS: <br>
https://www.dataquest.io/blog/installing-python-on-mac/ <br><br>

Install Python for Windows: <br>
https://www.tomshardware.com/how-to/install-python-on-windows-10-and-11 <br><br>

<h1> Activate Python Virtual Environment   </h1> <br>
The purpose of a Python virtual environment is to create an isolated virtual space where you could freely <br>
install packages and depencies for a <b> certain </b> project without worrying if these packages and depencies will <br>
conflict with your global packages! <br><br>

Open up the directory of the project, but be sure you're outside of the "SalesApp" directory. Once you're in this directory, type: <br><br>
For MacOS:
```bash
source Steel/bin/activate
``` 

The Python Virtual Environment for MacOS will then be activated! You can now run the server.
<br><br>

For Windows:
```bash
python3 -m venv Steel
```

<br><br>

<h1> Running the Server </h1>
Enter the directory of the virtual environment folder that you've created. <br>
Activate the Python virtual environment: <br><br>
For MacOS devices: 
<br>

```bash
source bin/activate 
``` 
<br>

For Windows devices greater than 7 and 8:
<br>

```bash
Scripts/activate
``` 
<br>


After activation, move out of the virtual environment directory, and run the commond below to install packages dedicated to your virtual environment: <br>
```bash
pip install -r requirements.txt 
```
Once Django is installed in the machine, go within the "SalesApp" directory and type: <br>
python manage.py runserver OR python3 manage.py runserver <br>




