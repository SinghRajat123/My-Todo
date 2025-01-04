  
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
    
# Create the database tables 
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        
        
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        print(f"Added todo: {title} - {desc}")
        
    search_query = request.args.get('Search') 
    print(f"Search query: {search_query}")
    
    if search_query:
        allTodo = Todo.query.filter( (Todo.title.contains(search_query)) | (Todo.desc.contains(search_query)) ).all() 
        print(f"Search results: {allTodo}")
    else:
        allTodo = Todo.query.all()
        print(f"All todos: {allTodo}")
  
    return render_template('index.html', allTodo=allTodo)


    



@app.route('/update/<int:sno>', methods=['GET', 'POST'])

def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")




if __name__=="__main__":
    app.run(debug=True)