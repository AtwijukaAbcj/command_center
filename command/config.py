from datetime import date
from datetime import datetime
from datetime import timedelta
from functools import wraps
from flask import Flask, request, make_response, session
from flask_cors import CORS
from flask_mail import Mail, Message
from flaskext.mysql import MySQL
from flask_toastr import Toastr
from flask_bootstrap import Bootstrap
import string, random, re, socket, hashlib, json, time, pymysql
from tiny import *
import requests, os
path = os.getcwd()
# env = 'demo'
env = 'live'
# set admin email 
admin_email = 'charles.bravo24@gmail.com'
charles = '+256758169834'
#initialize the Airtel Money api set from the account portal 
if env == 'demo':
    RC_SECRET_KEY= demo_token()
else:  
    RC_SECRET_KEY= live_token()

app = Flask(__name__)
app.secret_key = 'a1a4b331-ea92-4446-b877-3a24957bf126'
host = socket.gethostname()

if host == 'DESKTOP-BBRP68I':
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'cmd_center'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['ADMIN_URL'] = 'http://localhost/cmd/'
    app.config['BASE_URL'] = 'http://127.0.0.1:5000/'
    app.config['SITE_URL'] = 'http://localhost/cmd/'
    UPLOAD_FOLDER = os.path.join(path, 'static/uploads')
    IMG_FOLDER = 'static/uploads/'
else:
    app.config['MYSQL_DATABASE_USER'] = 'asabayus_atwijuka'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'BXX(#?;KL@kg'
    app.config['MYSQL_DATABASE_DB'] = 'asabayus_emergedb'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['BASE_URL'] = 'https://emergencyresponse.online/'
    app.config['ADMIN_URL'] = 'https://emergencyresponse.online/admin/index.php'
    app.config['SITE_URL'] = 'https://emergencyresponse.online/'
    UPLOAD_FOLDER = os.path.join(path, 'static/uploads')
    IMG_FOLDER = 'static/uploads/'

# set up mysql connection here 
mysql = MySQL(app)
CORS(app)
Bootstrap(app)
toastr = Toastr(app)
# mysql.init_app(app)
# setup mailer
app.config['MAIL_SERVER']= 'mail.emergencyresponse.online'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'admin@emergencyresponse.online'
app.config['MAIL_PASSWORD'] = 'a]v!gc+bbTqA'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMG_FOLDER'] = IMG_FOLDER
# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_authenticated(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            if token != RC_SECRET_KEY:
                return make_response(json.dumps({'response': 'Unauthorized access', 'code': 401})), 401
            else:
                return f(*args, **kwargs)
        else:
            return make_response(json.dumps({'response': 'Unauthorized access, token missing', 'code': 401})), 401
    return decorated_func

def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if 'email' in session:
            return f(*args, **kwargs)
        else:
            return make_response(json.dumps({'response': 'Unauthorized access, login required', 'code': 404})), 401
    return decorated_func

def hash_password(password):
    result = hashlib.sha1("{}".format(password).encode('utf-8')).hexdigest()
    return result

def email_send(recipient,subject, message):
    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = message
    msg.html = message
    mail.send(msg)
    return True


def get_date():
    now = datetime.now().strftime("%Y-%m-%d")
    return now

# to change on the live server 
def get_time():
    if host == 'CYBERSPACE':
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        xy = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        given_time = datetime.strptime(xy, "%Y-%m-%d %H:%M:%S")
        n = 3 # Add 2 hours to datetime object
        final_time = given_time + timedelta(hours=n)
        now = final_time.strftime("%Y-%m-%d %H:%M:%S")
    return now


def server_ip():
    host_ip = socket.gethostname()
    return host_ip

def get_code():
    code = random.randint(10000, 99999)
    return code

def get_filecode():
    code = random.randint(1000000, 9999999)
    return code

def sanitize_phone(msisdn):
    if '+256' in msisdn:
        new_string = re.sub(r'.', '', msisdn, count = 4)
    else:
        new_string = re.sub(r'.', '', msisdn, count = 1)
    return new_string


def easy_phone(msisdn):
    if '+256' in msisdn:
        new_string = re.sub(r'.', '', msisdn, count = 1)
    else:
        new_string = re.sub(r'.', '', msisdn, count = 1)
    return new_string

def sanitize_sms(msisdn):
    if '+256' in msisdn:
        number = msisdn
    else:
        number = ''.join(('+256', sanitize_phone(msisdn)))
    return number

def clean_app_input(msisdn):
    if '+256' in msisdn:
        number = ''.join(('0', sanitize_phone(msisdn)))
    else:
        number = msisdn
    return number

def country_code(code, phone):
    number = ''.join((code, phone))
    return number

def airtel_trans_id():
    result = random.randint(111111111111, 999999999999)
    return result

def create_wallet():
    result = random.randint(11111111,99999999)
    return result

def generate_user():
    letters = string.digits
    result = ''.join(random.choice(letters) for i in range(10)) 
    return result

def internationalize_number(phone):
    mtn_pattern = '^(0|256|\+256)(77|78|76)([0-9])(\d{6,6})$'
    airtel_pattern = '^(0|256|\+256)(75|70|74)([0-9])(\d{6,6})$'
    if bool(re.match(mtn_pattern, phone)):
        method = 'MTN'
    elif bool(re.match(airtel_pattern, phone)):
        method = 'AIRTEL'
    else:
        method = 'INVALID'
    return method

def get_expiry_time():
    result = int(time.time())
    return result

def check_otp_expiry(otp):
    current = get_expiry_time()
    diff = current - int(otp)
    if diff < 180:
        return True
    else:
        return False 


def converter(frm, to, amount):
    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=b2ed61cf900f7fac3e33".format(frm, to)
    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    rate = round(response.json()["{}_{}".format(frm, to)], 5)
    result = round(float(amount * rate), 2)
    return result

def text_to_log(data):
    with open('log.txt', 'a+') as f:
        f.write("Callback data at {} - ".format(get_time())+str(data))
        f.write("\n")
    f.close()   

def text_to_data(data):
    with open('update.txt', 'a+') as f:
        f.write("Subscriber data at {} - ".format(get_time())+str(data))
        f.write("\n")
    f.close()   

def next_days(n):
    end_date = date.today() + timedelta(days=n)
    return end_date

def time_am_pm():
    t = datetime.today().strftime("%H:%M %p")
    return t

def get_coordinates(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyCqIAwArbvvwzfMQaco1_hxk0005Nzfjno".format(address)
    payload={}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    lat = res['results'][0]['geometry']['location']['lat']
    lng = res['results'][0]['geometry']['location']['lng']
    return "{},{}".format(lat,lng)

# print(get_coordinates('Sillah Tents Limited'))
