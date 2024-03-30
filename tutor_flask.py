from flask import Flask, render_template, request, redirect                                                           # Importing all Flask's modules
from flask_mysqldb import MySQL                                                                                       # Importing Flask MySQL
from werkzeug.utils import secure_filename                                                                            
import os

app = Flask(__name__)                                                                                                 # Creating Flask instance with __name__ constructor

app.secret_key = 'your_secret_key'                                                                                    # Creating secret key   

app.config['MYSQL_HOST'] = 'localhost'                                                                                # Creating MySQL Configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'python_db'

mysql = MySQL(app)

UPLOAD_FOLDER = 'uploads'                                                                                             # Folder to store uploaded files
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}                                                                           # Allowed file extensions


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')                                                                                                       # Home page HTML Rendering
def index():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])                                                                      # Registration HTML page rendering by POST and GET Request
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        college = request.form['college']
        department = request.form['department']
        graduate_year = request.form['graduate_year']
        college_CGPA = request.form['college_CGPA']
        tenth_percentage = request.form['tenth_percentage']
        twelfth_percentage = request.form['twelfth_percentage']
        current_location = request.form['current_location']
        programming_languages = request.form['programming_languages']
        expected_salary = request.form['expected_salary']
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur = mysql.connection.cursor()                                                                           # Store data in MySQL
            cur.execute(
                "INSERT INTO candidates (name, email, college, department, graduate_year, college_CGPA, tenth_percentage, twelfth_percentage, current_location, programming_languages, expected_salary, upload_file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (name, email, college, department, graduate_year, college_CGPA, tenth_percentage, twelfth_percentage,
                 current_location, programming_languages, expected_salary, filename))
            mysql.connection.commit()
            cur.close()

            return redirect('/thankyou')
        else:
            return redirect(request.url)
    return render_template('register.html')


@app.route('/thankyou')                                                                                               # Rendering Thank you HTML Page
def thankyou():
    return render_template('thankyou.html')


if __name__ == '__main__':
    app.run(debug=True)
