# CITS3200_6

We are requiring a software program that will transcribe our student logbooks, to be completed in Qualtrics, to readable reports for each student, showing where they are placed, which activity and how many hours they completed with each Host and then their final reports to be placed into our Sonia Placement Software.

I have an example, from our 4th year placements, similar to what I would require. The database needs to be robust and user friendly so if our Hosts change or hours of particular student skills change, we can easily adapt the database to continue to work. The data also needs to be secure.

Thank you for your consideration.

Client
Contact: Jo Huggins
Phone: 6488 2901
Email: jo.huggins@uwa.edu.au
Preferred contact: Phone,Email
Location: Human Sciences

IP Exploitation Model
The IP exploitation model requested by the Client is: Creative Commons (open source) https://creativecommons.org.au/

## How to install
First, clone the repository into your folder of choice.

### Windows
1. Ensure you have Python installed.
2. Run `setup.bat`.

### Unix-based systems (Linux, Mac, Cygwin, etc.)
1. Ensure you have Python 3 installed (such as from your OS' package manager).
2. Run `setup.sh`.

## How to launch

### From command line

1. Ensure you are in the .venv virtual environment. If not, re-enter by running the `setup` script again.
2. Run `flask run`.
3. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser of choice.

### From VSCode

1. Install the [VSCode Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) if you haven't already.
2. Go to the `Run and Debug` pane (Ctrl+Shift+D).
3. Click `Add Configuration`.
4. Select `Python` as the category.
5. Select `Flask` as the debug category.
6. Now either click the `Python: Flask` button or press `F5` on your keyboard.
7. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser of choice.
