from flask import Flask, jsonify, make_response, request, abort, url_for
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from datetime import datetime, timedelta
import calendar
import os

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'lana':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


app = Flask(__name__)
CORS(app)
#cors = CORS(app, resources={"/fonis/api/*": {"origins": "*"}})
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Fonisovac(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(120))
    birthday = db.Column(db.DATE)

    def __init__(self, name, surname, birthday):
        self.name = name
        self.surname = surname
        self.birthday = birthday


class FonisovacSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'surname', 'birthday')


fonisovac_schema = FonisovacSchema
fonisovci_schema=FonisovacSchema(many=True)

@app.route('/fonis/api/<int:fonisovac_id>', methods=['GET'])
@auth.login_required
def get_fonisovac(fonisovac_id):
    fonisovac = Fonisovac.query.get(fonisovac_id)
    if fonisovac == not_found:
        abort(404)
    return make_json(fonisovac)


@app.route('/fonis/api/<int:fonisovac_id>', methods=['PUT'])
@auth.login_required
def upbirthday_fonisovac(fonisovac_id):
    fonisovac = Fonisovac.query.get(fonisovac_id)

    if fonisovac == not_found:
        abort(404)
    if not request.json:
        abort(400)

    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    if 'surname' in request.json and type(request.json['surname']) is not str:
        abort(400)
    if 'birthday' in request.json and (
            type(request.json['birthday']) is not str and (type(request.json['birthday']) is not int)):
        abort(400)

    fonisovac.name = request.json['name']
    fonisovac.surname = request.json['surname']
    birthdayPom = str(request.json['birthday'])
    fonisovac.birthday = datetime.strptime(birthdayPom.split('T')[0], '%Y-%m-%d')

    # fonisovac.userID = request.json['userID']
    # mozda je glupo da se ovo menja

    db.session.commit()
    return make_json(fonisovac)


@app.route('/fonis/api/<int:fonisovac_id>', methods=['DELETE'])
@auth.login_required
def delete_fonisovac(fonisovac_id):
    fonisovac = Fonisovac.query.get(fonisovac_id)
    db.session.delete(fonisovac)
    db.session.commit()
    return make_json(fonisovac)
    # popraviti


@app.route('/fonis/api', methods=['GET'])
@auth.login_required
def get_fonisovci():
    all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).all()
    result = fonisovci_schema.dump(all_fonisovci)
    return jsonify({'fonisovci': [make_public_fonisovac(fonisovac) for fonisovac in result.data]})


@app.route('/fonis/api/', methods=['GET'])
@auth.login_required
def get_fonisovci_with_param():
    #n = request.args.get("n")
    d=request.args.get('d')
    #birthday = getTime(request.args.get('d'))
    if d=='this year' or d=='all':
        all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).all()
    elif d=='today':
        string=datetime.today().strftime('%Y-%m-%d')
        string=string[5:]
        all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).filter(Fonisovac.birthday.endswith(string)).all()
    else:
        '''
        if d == 'this week':
            first_day = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7 + 6)
            fstring=first_day.strftime('%Y-%m-%d')
            fstring=fstring[5:]
            last_day=first_day+timedelta(days=6)
            lstring = last_day.strftime('%Y-%m-%d')
            lstring = lstring[5:]
            all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).filter(
                Fonisovac.birthday.has(string)).all()
                '''
        if d == 'this month':
            first_day = datetime.today().replace(day=1)
            string = first_day.strftime('%Y-%m-%d')
            string = string[4:8]
            all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).filter(
                Fonisovac.birthday.contains(string)).all()
        else:
            all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).all()
        #birthdayPom = datetime.today().date() + timedelta(days=1)#...........
        '''
        if birthday == birthdayPom:
                all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).all()
        else:
            
            if (n is None) or n == 'undefined' or n == '' or n == '0':
                all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).filter(
                    and_(Fonisovac.birthday >= birthday, Fonisovac.birthday <= birthday.today()))
            else:
                
            all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).filter(
                and_(Fonisovac.birthday >= birthday, Fonisovac.birthday <= birthday.today())).all()
                '''
        '''
        all_fonisovci = Fonisovac.query.order_by(Fonisovac.birthday.desc()).filter(
            and_(Fonisovac.birthday >= first_day, Fonisovac.birthday <= last_day)).all()
        '''
    result = fonisovci_schema.dump(all_fonisovci)

    return jsonify({'fonisovci': [make_public_fonisovac(fonisovac) for fonisovac in result.data]})


def getTime(argument):
    if argument == 'this week':
        time = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7 - 1)
    elif argument == 'this month':
        time = datetime.today().replace(day=1)
    else:
        time = datetime.today()
    return time.date()


@app.route('/fonis/api', methods=['POST'])
@auth.login_required
def create_fonisovac():
    if not request.json or 'name' not in request.json:
        abort(400)

    # user=request.json['userID']
    name = request.json['name']
    surname = request.json['surname']
    birthdayPom = request.json['birthday']
    birthday = datetime.strptime(birthdayPom, '%Y-%m-%d')

    new_fonisovac = Fonisovac(name, surname, birthday)

    db.session.add(new_fonisovac)
    db.session.commit()

    return make_json(new_fonisovac), 201


@app.errorhandler(404)
@auth.login_required
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_fonisovac(fonisovac):
    new_fonisovac = {}
    for field in fonisovac:
        if field == 'id':
            new_fonisovac['uri'] = url_for('get_fonisovac', fonisovac_id=fonisovac['id'], _external=True)
        else:
            new_fonisovac[field] = fonisovac[field]
    return new_fonisovac


def make_json(fonisovac):
    res = {}
    res['id'] = fonisovac.id
    res['name'] = fonisovac.name
    res['surname'] = fonisovac.surname
    # res['birthday'] = datetime.strftime(fonisovac.birthday, "%d.%m.%Y")
    res['birthday'] = datetime.strftime(fonisovac.birthday, "%Y-%m-%d")
    return jsonify({'fonisovac': make_public_fonisovac(res)})


if __name__ == '__main__':
    app.run(debug=True)

