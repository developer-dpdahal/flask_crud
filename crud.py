from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'my key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.full_name


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        save_data = User(full_name=full_name, email=email, phone=phone, address=address)
        db.session.add(save_data)
        db.session.commit()
        flash("Data was successfully inserted")
        return redirect(url_for('index'))
    else:
        data = User.query.all()
        return render_template('index.html', user_data=data)


@app.route('/delete/<id>')
def delete(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Data was successfully Deleted")
    return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    if request.method == "POST":
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        criteria = request.form['criteria']
        user = User.query.get(criteria)
        user.full_name = full_name
        user.email = email
        user.phone = phone
        user.address = address
        db.session.commit()
        flash("Successfully updated")
        return redirect(url_for('index'))
    else:
        data = User.query.filter_by(id=id).first()
        return render_template('edit.html', user_data=data)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
