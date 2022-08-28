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
3. After ensuring the requirements installed correctly, run the command `flask db upgrade` to generate the proper database.

### Unix-based systems (Linux, Mac, Cygwin, etc.)
1. Ensure you have Python 3 installed (such as from your OS' package manager).
2. Run `setup.sh`.
3. After ensuring the requirements installed correctly, run the command `flask db upgrade` to generate the proper database.

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


## Graphs Macro
> macro is defined in /app/views/macros/charts.jinja

### Usage

#### 1. Pass the data through to the template from routes.py or anywhere a template is rendered
> Sample data passed into example.html
```python
## Taken from /app/routes.py
data = {
    'domains': (
        'Cardiovascular',
        'Musculoskeletal',
        'Metabolic',
        'Mental Health',
        'Cancer',
        'Kidney',
        'Neurological',
        'Respiratory/Pulmonary',
        'Other'
    ), ## list of available domains
    'charts': [
    {
        'title': 'Core Domains',
        'id': 'test1',
        'yMax': '200', # maximum y value, should be consistent to allow for like to like comparison
        'style': 'core',
        'domains': (1, 1, 1, 0, 0, 0, 0, 0, 0), ## if the index is one, the domain will be shown
        'hours': [
            ('Referrals, Screening or Assessmnts', (32, 8, 12)), ## three tuple as we are showing three domains
            ('Excercise Prescription', (9, 19, 49)),
            ('Excercise Delivery', (10, 2, 24)),
            ('Other', (13, 28, 9)),
        ]
    },
    {
        'title': 'Additional Domains',
        'id': 'test2',
        'yMax': '70',
        'domains': (0, 0, 0, 1, 1, 1, 1, 1, 1),
        'hours': [
            ('Referrals, Screening or Assessmnts', (3, 8, 12, 6, 6, 12)),
            ('Excercise Prescription', (3, 8, 1, 6, 6, 12)),
            ('Excercise Delivery', (5, 3, 1, 6, 6, 12)),
            ('Other', (3, 8, 12, 5, 3, 1)),
        ]
    }]
    }
return render_template('example.html', data=data)
```

#### 2. From the template, import the macro
```jinja
{% import "macros/charts.jinja" as charts %}
```

#### 3. Now within the head block, call the chart_head macro
```jinja
{{ charts.chart_head(data) }}
```

#### 4. Use the chart_div macro to create a div where you wish to inject chart
> Must call once for each dict's id in the data array, this is where it will be created
```jinja
{{ charts.chart_div(id) }}
```
