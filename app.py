from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set secret key for app
app.secret_key = '894ad1df46d08f691c788a0e3a5d1701'

# Set database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Create SQLAlchemy database object
db = SQLAlchemy(app)


# Define User class to store user information
class User(db.Model):
    """
    A class used to represent a user in the database.

    Attributes
    ----------
    id : int
        The unique id of the user.
    username : str
        The username of the user.
    password : str
        The password of the user.
    email : str
        The email address of the user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)


# Define Task class to store created tasks
class Task(db.Model):
    """
    A class used to represent a task in the database.

    Attributes
    ----------
    id : int
        The unique id of the task.
    title : str
        The title of the task.
    description : str
        The description of the task.
    due_date : str
        The due date of the task.
    priority : str
        The priority level of the task (e.g. high, medium, low).
    labels : str
        The labels associated with the task.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.String(80))
    priority = db.Column(db.String(20))
    labels = db.Column(db.String(200))

    def __init__(self, title, description, due_date, priority, labels):
        """
        Initializes a new instance of the Task class.

        Parameters
        ----------
        title : str
            The title of the task.
        description : str
            The description of the task.
        due_date : str
            The due date of the task.
        priority : str
            The priority level of the task (e.g. high, medium, low).
        labels : str
            The labels associated with the task.
        """

        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.labels = labels


@app.route('/')
def index():
    """
    Renders the registration page.
    
    Returns
    -------
    str
        The rendered registration page.
    """
    return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    
    Returns
    -------
    str
        The rendered login page if the registration is successful.
        Otherwise, redirects to the login page with an error message.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('login'))

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists', 'error')
            return redirect(url_for('register'))

        # Create a new user
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    
    Returns
    -------
    str
        The rendered successful page if the login is successful.
        Otherwise, returns an error message.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return render_template('successful.html')
        else:
            flash('Invalid username or password','error')
    return render_template('login.html')


@app.route('/Todo', methods=['GET', 'POST'])
def tasks():
    """
    Handles task creation and retrieval.
    
    Returns
    -------
    str
        The rendered Todo page with all tasks retrieved fromthe database.
    """
    if request.method == 'POST':
        title = request.form['taskTitle']
        description = request.form['taskDescription']
        due_date = request.form['taskDueDate']
        priority = request.form['taskPriority']
        labels = request.form['taskLabels']

        task = Task(title=title, description=description, due_date=due_date, priority=priority, labels=labels)
        db.session.add(task)
        db.session.commit()

    tasks = Task.query.all()
    return render_template('Todo.html', tasks=tasks)


if __name__ == '__main__':
    with app.app_context():
        # Create all database tables before running the app
        db.create_all()

    # Run the app in debug mode on port 8000
    app.run(debug=True, port=8000)
