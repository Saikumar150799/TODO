from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

apps = Flask(__name__,template_folder='template')
apps.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todos.db'
apps.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(apps)

class Todo(db.Model):
          sno = db.Column(db.Integer,primary_key=True)
          title = db.Column(db.String(200),nullable=True)
          desc = db.Column(db.String(500),nullable=True)
          date_created = db.Column(db.DateTime,default=datetime.utcnow)

          def __repr__(self):
                    return f'{self.sno} {self.title}'

@apps.route('/',methods=['GET','POST'])
def home():
          if request.method=='POST':
                    # print('post')
                    title = request.form['title']
                    desc = request.form['desc']
                    todo = Todo(title=title,desc=desc)
                    db.session.add(todo)
                    db.session.commit()
          allTodo = Todo.query.all()
          # print(allTodo)
          return render_template('base.html',allTodo=allTodo)



@apps.route('/delete/<int:sno>')
def delete(sno):
          todo = Todo.query.filter_by(sno=sno).first()
          db.session.delete(todo)
          db.session.commit()
          return redirect('/') 

@apps.route('/show')
def show():
          allTodo = Todo.query.all()
          print(allTodo)
          return "This is home page"


if __name__ == "__main__":
          apps.run(debug=True)