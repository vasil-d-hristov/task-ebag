# eBag - Technical Task

### Description: "a backend API for a system to manage a category tree"

---

### How to Use:

#### Note: below are cited Windows 10 Command Prompt commands for your convenience

1. Clone the repository files in the desired local folder
2. Within the repo folder create virtual environment
    * **virtualenv venv**
3. Activate the virtual environment
    * **.\venv\Scripts\activate**
4. Install the necessary project's dependencies
    * **pip install -r requirements.txt**
5. Change the current folder to ".\ebag"
    * **cd ebag**
6. Apply migrations ( create database )
    * **py manage.py migrate**
7. Create Root Category ( first record )
    * **py manage.py reset_db**
8. Run the Django development server
    * **py manage.py runserver**
9. Browse to http://127.0.0.1:8000/

#### Note: "reset_db" accepts two optional parameters

reset_db [ -c --categories < int > [ -s --similarities < int > ] ]

* categories - the count of the categories to be created in addition to the Root Category
* similarities - the number of attempts to create unique similarities

For example: **py manage.py reset_db -c 10** or **py manage.py reset_db -c 10 -s 10**

#### Note: to run the implemented Tests use the following command

* **py manage.py test**

#### Note: Test Images for upload are provided in ".\ebag\categories\tests\files"

---

### Credits:

* **CSS** thanks to w3schools.com
* Test **Images** thanks to pixabay.com
* **Graph(s)** thanks to geeksforgeeks.org
