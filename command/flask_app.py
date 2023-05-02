from config import *
from utils import sms_send
from flask import request, make_response, render_template, redirect, session, url_for, flash
import uuid, json, pymysql
from werkzeug.utils import secure_filename
import logging
logging.basicConfig(filename='logs.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')

# @app.route('/index')
# @app.route('/')
# def index():
#     return redirect(app.config['SITE_URL'], code=302)

@app.route('/admin/')
def load_admin():
    return redirect(app.config['ADMIN_URL'], code=302)

# format currency 
@app.template_filter()
def currency_format(value):
    value = float(value)
    return "{:,.0f}".format(value)


# authentication 
@app.route('/v1/admin-login', methods=['POST','GET'])
@is_authenticated
def admin_login():
    data = request.get_json(force=True)
    email = data['email']
    password = hash_password(data['password'])
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE (email=%s OR contact=%s) AND password=%s LIMIT 1", (email, email, password))
    rows = cursor.fetchone()
    if rows:
        code = get_code()
        id = rows['userID']
        # set these temporary for demo login 
        expires_in = get_expiry_time()
        sqlQuery = "UPDATE admins set otp=%s, expires_in=%s WHERE userID=%s"
        bindData = (code, expires_in, id,)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        # send email or text 
        subject = "Login Verification"
        message = "Hello {}, use this 5-digit verification code {} to access ECCTE.".format(rows['name'], code)
        email_send(rows['email'], subject, message)
        # send sms here 
        # sms_send(message, rows['contact'])
        response = {'message': 'Login accepted, OTP Sent', 'status': 'success', 'userid': id}
    else:
        response = {'message':'Email or password is incorrect', 'status': 'failed'}
    return make_response(json.dumps(response))
 

# route for registering via app
@app.route('/v1/app-register', methods=['POST','GET'])
@is_authenticated
def app_register():
    data = request.get_json(force=True)
    name = data['name']
    phone = data['phone']
    email = data['email']
    password = data['password']
    age = data['age']
    hashed = hash_password(password)
    code = get_code()
    address = data['address']
    expires_in = 0
    image = ''
    pid = generate_user()
    if int(data['age']) > 17:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # check if email is not registered
        cursor.execute("SELECT * FROM patients WHERE email=%s LIMIT 1", (email))
        chk = cursor.fetchone()
        # check if the phone number is not registered 
        cursor.execute("SELECT * FROM patients WHERE phone=%s LIMIT 1", (phone))
        check = cursor.fetchone()
        if not chk and not check:
            sql_query = "INSERT INTO patients(pid, name, email, phone, password, age, address, otp, expires_in, image) " \
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            bind_data = (pid, name, email, phone, hashed, age, address, code, expires_in, image,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql_query, bind_data)
            conn.commit()
            # send an email to the user 
            subject = "ECC User Registration"
            message = "Hello {}, you have successfully registered for ECC with your email {}.".format(name, email)
            email_send(email, subject, message)
            response = {'message': 'User registered successfully', 'status': 'success'}
        elif not check:
            response = {'message':'Email already registered', 'status':'failed'}
        elif not chk:
            response = {'message':'Phone number already registered', 'status':'failed'}
        else:
            response = {'message':'Email and phone already registered', 'status':'failed'}
        return make_response(json.dumps(response))
    else:
        response = {'message':'Please confirm your age, only 18+ are allowed to signup', 'status':'failed'}
        return make_response(json.dumps(response))

# route for api patient login
@app.route('/v1/app-login', methods=['GET','POST'])
@is_authenticated
def app_login():
    data = request.get_json(force=True)
    email = data['email']
    password = hash_password(data['password'])
    code = get_code()
    if len(email) > 0:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM patients WHERE email=%s AND password=%s LIMIT 1", (email, password))
        rows = cursor.fetchone()
        # check if user is in the system
        if rows:
            code = get_code()
            id = rows['pid']
            expires_in = get_expiry_time()
            # set these temporary for demo login 
            sqlQuery = "UPDATE patients SET otp=%s, expires_in=%s WHERE pid=%s"
            bindData = (code, expires_in, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM patients WHERE pid=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            # send email or text 
            # subject = "Login Verification"
            # message = "Hello {}, use this 5-digit verification code {} to access ECC.".format(rows['name'], code)
            # email_send(rows['email'], subject, message)
            response = {'message': 'Login accepted', 'status': 'success','user_id': id, 'data': ret}
        else:
            response = {'message':'Email or password is incorrect', 'status': 'failed'}
        return make_response(json.dumps(response))
    else:
        phone = data['phone']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # check if login credentials are correct
        cursor.execute("SELECT * FROM patients WHERE phone=%s AND password=%s LIMIT 1", (phone, password))
        rows = cursor.fetchone()
        if rows:
            code = get_code()
            id = rows['pid']
            expires_in = get_expiry_time()
            # set these temporary for demo login 
            sqlQuery = "UPDATE patients SET otp=%s, expires_in=%s WHERE pid=%s"
            bindData = (code, expires_in, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM patients WHERE pid=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            # send email or text 
            # message = "Hello {}, use this 5-digit verification code {} to access ECC.".format(rows['name'], code)
            # sms_send(message, rows['phone'])
            response = {'message': 'Login accepted', 'status': 'success', 'user_id': id, 'data': ret}
        else:
            response = {'message':'Phone number or password is incorrect', 'status':'failed'}
        return make_response(json.dumps(response))

# route for api login
@app.route('/v1/drv-login', methods=['GET','POST'])
@is_authenticated
def driver_login():
    data = request.get_json(force=True)
    email = data['email']
    password = hash_password(data['password'])
    code = get_code()
    if len(email) > 0:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM drivers WHERE email=%s AND password=%s LIMIT 1", (email, password))
        rows = cursor.fetchone()
        # check if user is in the system
        if rows:
            code = get_code()
            id = rows['did']
            expires_in = get_expiry_time()
            # set these temporary for demo login 
            sqlQuery = "UPDATE drivers SET otp=%s, expires_in=%s WHERE did=%s"
            bindData = (code, expires_in, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM drivers WHERE did=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            # send email or text 
            # subject = "Login Verification"
            # message = "Hello {}, use this 5-digit verification code {} to access ECC.".format(rows['name'], code)
            # email_send(rows['email'], subject, message)
            response = {'message': 'Login accepted', 'status': 'success','user_id': id, 'data': ret}
        else:
            response = {'message':'Email or password is incorrect', 'status': 'failed'}
        return make_response(json.dumps(response))
    else:
        phone = data['phone']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # check if login credentials are correct
        cursor.execute("SELECT * FROM drivers WHERE phone=%s AND password=%s LIMIT 1", (phone, password))
        rows = cursor.fetchone()
        if rows:
            code = get_code()
            id = rows['did']
            expires_in = get_expiry_time()
            # set these temporary for demo login 
            sqlQuery = "UPDATE drivers SET otp=%s, expires_in=%s WHERE did=%s"
            bindData = (code, expires_in, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM drivers WHERE did=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            # send email or text 
            # message = "Hello {}, use this 5-digit verification code {} to access ECC.".format(rows['name'], code)
            # sms_send(message, rows['phone'])
            response = {'message': 'Login accepted', 'status': 'success', 'user_id': id, 'data': ret}
        else:
            response = {'message':'Phone number or password is incorrect', 'status':'failed'}
        return make_response(json.dumps(response))

# route for api login
@app.route('/v1/forgot-pwd', methods=['GET','POST'])
@is_authenticated
def forgot_pwd():
    data = request.get_json(force=True)
    email = data['email']
    if len(email) > 0:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM patients WHERE email=%s  LIMIT 1", (email))
        rows = cursor.fetchone()
        # check if user is in the system
        if rows:
            code = get_code()
            id = rows['pid']
            expires_in = get_expiry_time()
            # set these temporary for demo login 
            sqlQuery = "UPDATE patients SET otp=%s, expires_in=%s WHERE pid=%s"
            bindData = (code, expires_in, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM patients WHERE pid=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            # send email or text 
            subject = "Password Reset"
            message = "Hello {}, use this 5-digit verification code {} to reset your password for ECC.".format(rows['name'], code)
            email_send(rows['email'], subject, message)
            response = {'message': 'Password reset accepted, OTP Sent', 'status': 'success', 'user_id': id, 'data': ret}
        else:
            response = {'message':'Email not registered', 'status': 'failed'}
        return make_response(json.dumps(response))
    else:
        phone = data['phone']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # check if login credentials are correct
        cursor.execute("SELECT * FROM patients WHERE phone=%s LIMIT 1", (phone))
        rows = cursor.fetchone()
        if rows:
            code = get_code()
            id = rows['pid']
            expires_in = get_expiry_time()
            # set these temporary for demo login 
            sqlQuery = "UPDATE patients SET otp=%s, expires_in=%s WHERE pid=%s"
            bindData = (code, expires_in, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM patients WHERE pid=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            # send email or text 
            # message = "Hello {}, use this 5-digit verification code {} to reset your password for ECC.".format(rows['name'], code)
            # sms_send(message, rows['phone'])
            response = {'message': 'Password reset accepted, OTP Sent', 'status': 'success', 'user_id': id, 'data': ret}
        else:
            response = {'message':'Phone number not registered', 'status':'failed'}
        return make_response(json.dumps(response))

# route for driver forgot password
@app.route('/v1/drv-forgot', methods=['GET','POST'])
@is_authenticated
def driver_forgot():
    data = request.get_json(force=True)
    email = data['email']
    if len(email) > 0:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM drivers WHERE email=%s  LIMIT 1", (email))
        rows = cursor.fetchone()
        # check if user is in the system
        if rows:
            code = get_code()
            id = rows['did']
            expires_in = get_expiry_time()
            # set these temporary for demo login 
            sqlQuery = "UPDATE drivers SET otp=%s, expires_in=%s WHERE did=%s"
            bindData = (code, expires_in, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM drivers WHERE did=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            # send email or text 
            subject = "Password Reset"
            message = "Hello {}, use this 5-digit verification code {} to reset your password for ECC.".format(rows['full_name'], code)
            email_send(rows['email'], subject, message)
            response = {'message': 'Password reset accepted, OTP Sent', 'status': 'success', 'user_id': id, 'data': ret}
        else:
            response = {'message':'Email not registered', 'status': 'failed'}
        return make_response(json.dumps(response))
    else:
        phone = data['phone']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # check if login credentials are correct
        cursor.execute("SELECT * FROM drivers WHERE phone=%s LIMIT 1", (phone))
        rows = cursor.fetchone()
        if rows:
            code = get_code()
            id = rows['did']
            expires_in = get_expiry_time()
            # set these temporary for demo login 
            sqlQuery = "UPDATE drivers SET otp=%s, expires_in=%s WHERE did=%s"
            bindData = (code, expires_in, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM drivers WHERE did=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            # send email or text 
            # message = "Hello {}, use this 5-digit verification code {} to reset your password for ECC.".format(rows['name'], code)
            # sms_send(message, rows['phone'])
            response = {'message': 'Password reset accepted, OTP Sent', 'status': 'success', 'user_id': id, 'data': ret}
        else:
            response = {'message':'Phone number not registered', 'status':'failed'}
        return make_response(json.dumps(response))

# verify OTP via the phone 
@app.route('/v1/reset-code', methods=['GET', 'POST'])
@is_authenticated
def reset_code():
    try:
        res = request.get_json(force=True)
        otp = res['code']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM patients WHERE otp=%s LIMIT 1", (otp))
        rows = cursor.fetchone()
        if rows:
            if(check_otp_expiry(rows['expires_in'])):
                resp = {"message": "Reset successful, OTP verified", "status": "success","user_id": rows['pid']}
                return make_response(json.dumps(resp))
            else:
                resp = {"message": "Password failed, OTP has expired", "status": "failed"}
                return make_response(json.dumps(resp))
        else:
            resp = {"message": "Password reset failed, OTP is incorrect", "status": "failed"}
            return make_response(json.dumps(resp))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# verify OTP via the driver phone 
@app.route('/v1/drv-set', methods=['POST', 'GET'])
@is_authenticated
def driver_set():
    try:
        res = request.get_json(force=True)
        otp = res['code']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM drivers WHERE otp=%s LIMIT 1", (otp))
        rows = cursor.fetchone()
        if rows:
            if(check_otp_expiry(rows['expires_in'])):
                resp = {"message": "Reset successful, OTP verified", "status": "success","user_id": rows['did']}
                return make_response(json.dumps(resp))
            else:
                resp = {"message": "Password failed, OTP has expired", "status": "failed"}
                return make_response(json.dumps(resp))
        else:
            resp = {"message": "Password reset failed, OTP is incorrect", "status": "failed"}
            return make_response(json.dumps(resp))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# route for api login
@app.route('/v1/reset-pwd', methods=['GET','POST'])
@is_authenticated
def reset_pwd():
    data = request.get_json(force=True)
    user = data['user']
    password = data['password']
    confirm = data['confirm']
    if password == confirm:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM patients WHERE pid=%s  LIMIT 1", (user))
        rows = cursor.fetchone()
        # check if user is in the system
        if rows:
            id = rows['pid']
            pwd = hash_password(password)
            # set these temporary for demo login 
            sqlQuery = "UPDATE patients SET password=%s WHERE pid=%s"
            bindData = (pwd, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM patients WHERE pid=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            response = {'message': 'Password reset successful', 'status': 'success', 'user_id': id, 'data': ret}
        else:
            response = {'message':'Password not reset, user not found', 'status': 'failed'}
        return make_response(json.dumps(response))
    else:
        response = {'message':'Passwords did not match', 'status':'failed'}
        return make_response(json.dumps(response))

# route for setting new passwords for driver
@app.route('/v1/drv-pwd', methods=['GET','POST'])
@is_authenticated
def driver_pwd():
    data = request.get_json(force=True)
    user = data['user']
    password = data['password']
    confirm = data['confirm']
    if password == confirm:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM drivers WHERE did=%s  LIMIT 1", (user))
        rows = cursor.fetchone()
        # check if user is in the system
        if rows:
            id = rows['did']
            pwd = hash_password(password)
            # set these temporary for demo login 
            sqlQuery = "UPDATE drivers SET password=%s WHERE did=%s"
            bindData = (pwd, id,)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            cursor.execute("SELECT * FROM drivers WHERE did=%s LIMIT 1", (id, ))
            ret = cursor.fetchone()
            response = {'message': 'Password reset successful', 'status': 'success', 'user_id': id, 'data': ret}
        else:
            response = {'message':'Password not reset, user not found', 'status': 'failed'}
        return make_response(json.dumps(response))
    else:
        response = {'message':'Passwords did not match', 'status':'failed'}
        return make_response(json.dumps(response))

#adding photo
@app.route('/v1/photo', methods=['POST'])
@is_authenticated
def app_photo():
    if request.method == 'POST':
        user = request.form['user']
        # check if the post request has the file part
        if 'image' not in request.files:
            return make_response(json.dumps({'message': 'No image selected'}))
        file = request.files['image']
        if file.filename == '':
            return make_response(json.dumps({'message': 'No image selected for uploading'}))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.split(".")[-1]
            filename = '{}.{}'.format(get_filecode(), file_ext) 
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM patients WHERE pid=%s LIMIT 1", (user))
            rows = cursor.fetchone()
            if rows:
                id = rows['pid']
                try:
                    if len(rows['image']) > 0:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(rows['image'])))
                except Exception as e:
                    pass
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = app.config['BASE_URL'] + app.config['IMG_FOLDER'] + str(filename)
                # set these temporary for demo login 
                sqlQuery = "UPDATE patients SET image=%s WHERE pid=%s"
                bindData = (image, id,)
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                response = {'message': 'Profile photo updated successfully', 'status': 'success','image': image, 
                'user_id': rows['pid']}
            else:
                response = {'message':'Profile phot not updated, user not found', 'status': 'failed'}
            return make_response(json.dumps(response))
        else:
            return make_response(json.dumps({'message': 'Please upload images of png, jpg, jpeg, gif..'}))

# route for adding an alert via app
@app.route('/v1/app-notify', methods=['POST','GET'])
@is_authenticated
def app_notify():
    data = request.get_json(force=True)
    message = data['message']
    location = data['location']
    user = data['user']
    reply = ''
    driver = ''
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # check if user is registered
        coords = get_coordinates(location)
        cursor.execute("SELECT * FROM patients WHERE pid=%s LIMIT 1", (user,))
        chk = cursor.fetchone()
        if chk:
            stx = 'Pending'
            sql_query = "INSERT INTO notifications(user, location, message, response, date_added, coordinates, driver, status) " \
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            bind_data = (user, location, message, reply, get_time(), coords, driver,stx,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql_query, bind_data)
            conn.commit()
            # send an email to the user 
            # subject = "ECC Notification Alerts"
            # msg = "Hello Admin, an emergency alert has been sent. Please login your dashboard to respond.."
            # email_send(admin_email, subject, msg)
            response = {'message': 'Alert sent successfully', 'status': 'success'}
        else:
            response = {'message': 'Alert not sent, user not found', 'status': 'success'}
        return make_response(json.dumps(response))
    
    except Exception:
        response = {'message':'Internal server error', 'status':'failed'}
        return make_response(json.dumps(response))


# route for loading new requests for the driver 
@app.route('/v1/drv-notify', methods=['GET', 'POST'])
@is_authenticated
def driver_notify():
    try:
        res = request.get_json(force=True)
        user = res['user']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT notifications.user, notifications.location, notifications.message, notifications.coordinates, "\
            "notifications.date_added, patients.name, patients.phone FROM notifications INNER JOIN patients ON " \
            "patients.pid=notifications.user WHERE notifications.response !='' AND status='Pending' AND driver=%s "\
            "order by notifications.nid DESC LIMIT 1", (user,))
        rows = cursor.fetchall()
        if rows:
            resp = {"status": "success","data": rows}
            return make_response(json.dumps(resp))
        else:
            resp = {"status": "failed", "data": [], "message": "No requests sent so far"}
            return make_response(json.dumps(resp))
    except Exception:
       response = {'message':'Internal server error', 'status':'failed'}
       return make_response(json.dumps(response))


# route for loading requests for the patients] 
@app.route('/v1/pt-notify', methods=['GET', 'POST'])
@is_authenticated
def pt_notify():
    try:
        res = request.get_json(force=True)
        user = res['user']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT notifications.user, notifications.location, notifications.message, notifications.coordinates, "\
            "notifications.date_added, patients.name, patients.phone FROM notifications INNER JOIN patients ON " \
            "patients.pid=notifications.user WHERE notifications.response !='' AND status='Pending' AND user=%s "\
            "order by notifications.nid DESC LIMIT 10", (user,))
        rows = cursor.fetchall()
        if rows:
            resp = {"status": "success","data": rows}
            return make_response(json.dumps(resp))
        else:
            resp = {"status": "failed", "data": [], "message": "No requests sent so far"}
            return make_response(json.dumps(resp))
    except Exception:
       response = {'message':'Internal server error', 'status':'failed'}
       return make_response(json.dumps(response))


# handle error
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Page not found: ' + request.url,
    }
    return make_response(json.dumps(message))

# from run import *
if __name__ == "__main__":
	app.run(debug=False)