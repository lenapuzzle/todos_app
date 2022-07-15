
from flask import Flask, render_template, request, redirect, session #Import Flask to allow us to create our app
app = Flask(__name__) # Create a new instance of the Flask class called "app"
app.secret_key = 'Keep it secret' # there is no secret on github

# @app.route('/')
# @app.route('/login')
# def hello_world():
#   return "Hello Python July 2022 class"

# @app.route('/python')
# def display_python_message():
#   return "Hello, this is different route /python."

# @app.route('/hello/<first_name>/<last_name>')
# def greet_person(first_name, last_name):
#   print(f'Hey there {first_name} {last_name}')
#   return f'Howdy, {first_name} {last_name}'

# @app.route('/info/<name>/<int:age>')
# def display_info(name, age):
#   print(type(name), type(age))
#   print(age + 5)
#   return f'Name: {name} Age: {age}'


list_of_users =  [
  {
  "first_name" : "Alex",
  "last_name" : "Miller",
  "id" : 1
  },
  {
  "first_name" : "Martha",
  "last_name" : "Speaks",
  "id" : 2
  },
  {
  "first_name" : "Roger",
  "last_name" : "Anderson",
  "id" : 3
  }
]

list_of_todos = [
  {
  "id" : 1,
  "description" : "Learn Python",
  "status" : "complete",
  "user_id" : 1
  },
  {
  "id" : 2,
  "description" : "Learn OOP",
  "status" : "complete",
  "user_id" : 1
  },
  {
  "id" : 3,
  "description" : "Learn Flask",
  "status" : "in_progress",
  "user_id" : 2
  },
  {
  "id" : 4,
  "description" : "Learn POST",
  "status" : "in_progress",
  "user_id" : 3
  }
]


@app.route('/todos')
def get_todos():
  if "logged_user" not in session:
    return redirect('/user/login')
  logged_uid = int(session['logged_user'])
  user = list_of_users[logged_uid-1] #simulating getting the user from the db

  # print(type(logged_uid))
  return render_template('todos.html', todos = list_of_todos, user = user)


@app.route('/todo/form')
def display_todo_form():
  if "logged_user" not in session:
    return redirect('/user/login')
  logged_uid = int(session['logged_user'])
  user = list_of_users[logged_uid-1] #simulating getting the user from the db
  next_todo_id = len(list_of_todos) + 1
  return render_template('todo_form.html', users = list_of_users, user = user, id = next_todo_id)


@app.route('/todo/new', methods = ['POST'])
def create_todo():
  # print(request.form)
  # if "logged_user" not in session:
  #   return redirect('/user/login')
  if session['logged_user'] != request.form['hidden']:
      return "HEY, THAT'S NOT YOU!"
  if int(request.form['id']) != len(list_of_todos)+1:
      return "INVALID ID FOR NEXT TODO"
  new_todo = {
    'id' : int(request.form['id']),
    'description' : request.form['description'],
    'status' : request.form['status'],
    'user_id' : int(request.form['hidden'])
  }
  list_of_todos.append(new_todo)
  return redirect('/todos')


@app.route('/user/process_login', methods = ['POST'])
def process_login():
  session['logged_user'] = request.form['user_id']
  return redirect('/todos')


@app.route('/user/login')
def user_login():
  return render_template('user_login.html', users = list_of_users)


@app.route('/user/logout')
def user_logout():
    # deleted_user = session.pop('logged_user') # pop will return the value as well
    # or
    # session.clear() # it clears everything in session!
    # or
    del session['logged_user'] # similar to session.pop() but does not return any value
    return redirect('/user/login')



"""
Convention syntax rules/recommendations

Method: GET
Getting all of a particular type
Url: '/todos'
Function: get_all_todos()
          get_todos()

Method: GET
Getting one of a particular
Url: '/todo/<int:id>'
Function: get_todo_by_id(id)

Method: GET
Displaying a form for a type
Url: '/todo/form'
Function: display_todo_form()

Method: POST
Creating a new type
Url: '/todo/new'
Function: create_todo()
"""


if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)  # Run the app in defug mode. And you can update the PORT here as: app.run(debug=True, PORT=5001) **instead of default 5000**