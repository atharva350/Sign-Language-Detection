import cv2
import pickle
import mediapipe as mp
import numpy as np
import keyboard
import gtts
import os
from playsound import playsound
from flask import *
from flask_mail import *
from random import *
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

app=Flask(__name__)
app.secret_key="login"

#Declaring Global variables
otpno=0 #variable for otp verification
source="" # variable to manage login modal
text=""
save_status=False
noteid=""
tempText=""

#configuring mail server
app.config['MAIL_SERVER']='smtp-mail.outlook.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='atharvaphadke1231@outlook.com'
app.config['MAIL_PASSWORD']='12345_Abcde'
app.config['MAIL_USE_SSL']=False
mail = Mail(app)

#configuring database
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='signlanguage'
mysql=MySQL(app)


#***CODE FOR IMAGE RECONITION AND ADD TEXT IN VARIABLE***

def gen_frames():
    global text,tempText
    model_dict = pickle.load(open('./model.p', 'rb'))
    model = model_dict['model']

    camera = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(0)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.5)

    labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D',4: 'E',5: 'F',6: 'G',7: 'H',8: 'I',9: 'J',10: 'K',11: 'L',12: 'M',13: 'N',14: 'O',15: 'P',16: 'Q',17: 'R',18: 'S',19: 'T',20: 'U',21: 'V',22: 'W',23: 'X',24: 'Y',25: 'Z',26: 'SPACE',27: 'DELETE'}
    while True:

        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()

        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,  # image to draw
                        hand_landmarks,  # model output
                        mp_hands.HAND_CONNECTIONS,  # hand connections
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10

                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                prediction = model.predict([np.asarray(data_aux)])

                predicted_character = labels_dict[int(prediction[0])]

                if keyboard.is_pressed('s'):
                    if predicted_character == "SPACE":
                        text += "  "
                        tempText = predicted_character
                    elif predicted_character == "DELETE":
                        text = text[:-1]
                        tempText = predicted_character
                    else:
                        text += predicted_character
                        tempText = predicted_character
                    print(text)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                            cv2.LINE_AA)
        except: continue

        cv2.waitKey(1)
        ret, buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# views and functions for home page and navigation bar
@app.route('/')
def index():
    status=False
    errormsg=" "
    forgot_status=False
    signup_status=False
    login_status=False
    return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)

@app.route('/neweditor')
def neweditor():
    global save_status,text
    text=""
    if not session.get("email"):
        # if not there in the session then redirect to the login page
        status=False
        login_status=True
        forgot_status=False
        signup_status=False
        return render_template("index.html",status=status,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status) 
    save_status=False
    cur = mysql.connection.cursor()
    cur.execute("SELECT fname FROM users WHERE email = %s", (session['email'],))
    fname_tuple = cur.fetchone()
    fname = fname_tuple[0]
    save_status=False
    return render_template('editor.html',text=text,fname=fname)

@app.route('/saved_notes')
def saved_notes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT userid FROM users WHERE email = %s",(session['email'],))
    userid_tuple = cur.fetchone()
    userid = userid_tuple[0]
    cur.execute("Select * FROM notes WHERE userid = %s",(userid,)) 
    rows = cur.fetchall()
    print(rows)
    cur = mysql.connection.cursor()
    cur.execute("SELECT fname FROM users WHERE email = %s", (session['email'],))
    fname_tuple = cur.fetchone()
    fname = fname_tuple[0]
    return render_template('saved_notes.html',data=rows,fname=fname) 

@app.route('/help')
def help():
    cur = mysql.connection.cursor()
    cur.execute("SELECT fname FROM users WHERE email = %s", (session['email'],))
    fname_tuple = cur.fetchone()
    fname = fname_tuple[0]
    return render_template('help.html',fname=fname) 

@app.route('/logout')
def logout():
    session.pop('email',None)
    status=False
    forgot_status=False
    signup_status=False
    login_status=False
    errormsg=""
    return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)

#routes and functions for editor

@app.route('/update_data')
def update_data():
    global text
    data = text
    return jsonify({'data':data})

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reset')
def reset():
    global text
    text=""
    return ''

@app.route('/save')
def save():
    global text, save_status
    cur = mysql.connection.cursor()
    cur.execute("SELECT userid FROM users WHERE email = %s",(session['email'],))
    userid_tuple = cur.fetchone()
    userid = userid_tuple[0]
    if(save_status==False):
        cur.execute("INSERT INTO notes (userid, create_date, modify_date, text) VALUES (%s, now(), now(), %s)",(userid,text,)) 
        mysql.connection.commit()
        cur.close()
        save_status=True
        return ''
    elif(save_status==True):
        cur.execute("UPDATE notes SET text = %s, modify_date=now() Where noteid = %s ",(text,noteid,)) 
        mysql.connection.commit()
        cur.close()
        return ''

@app.route('/playsound_route')
def playsound_route():
    global text  
    try: 
        sound = gtts.gTTS(text, lang="en")
        sound.save("speech.mp3")
        playsound("speech.mp3") 
        os.remove("speech.mp3")
    finally:
        return ''
    
#routes and functions for saved_notes
    
@app.route('/delete',methods=['POST'])
def delete():
    noteid=request.form['noteid']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notes Where noteid = %s ",(noteid,)) 
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('saved_notes'))

@app.route('/edit',methods=['POST'])
def edit():
    global text, save_status, noteid
    textdata=request.form['datatext']
    noteid=request.form['noteid']
    text = textdata
    save_status=True
    cur = mysql.connection.cursor()
    cur.execute("SELECT fname FROM users WHERE email = %s", (session['email'],))
    fname_tuple = cur.fetchone()
    fname = fname_tuple[0]
    return render_template('editor.html',text=text,fname=fname)

#routes and functions for all modals of login and signup

def change_otp():
    return randint(000000,999999)

@app.route('/verify',methods=["POST"])
def verify():
    global otpno
    otpno=change_otp()
    email = request.form['email']
    msg = Message('One Time Password',sender='atharvaphadke1231@outlook.com',recipients=[email])
    msg.body="Welcome to sign language detection.\nOTP for verification is : " +str(otpno) + "\nDo not share this OTP with anyone.\nThank You."
    mail.send(msg)
    status=True
    errormsg=""
    forgot_status=False
    signup_status=False
    return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status)

@app.route('/validate',methods=["POST"])
def validate():
    global otpno, source, fname, lname, email, password

    status = False
    forgot_status = False
    errormsg = ""
    signup_status=False
    login_status=False
    userotp = request.form['otp']

    if source == "login":
        if otpno == int(userotp):
            session['email']=email
            cur = mysql.connection.cursor()
            cur.execute("SELECT fname FROM users WHERE email = %s", (email,))
            fname_tuple = cur.fetchone()
            fname = fname_tuple[0]
            return render_template('editor.html',fname=fname)
        else:
            errormsg = "OTP entered was incorrect"
            login_status=True

    elif source == "signup":
        if otpno == int(userotp):
            errormsg = "Account Created Successfully. Login Now"
            status = False
            login_status=True
            encpass = sha256_crypt.encrypt(password)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (fname, lname, email, password) VALUES (%s, %s, %s, %s)",
                        (fname, lname, email, encpass))
            mysql.connection.commit()
            cur.close()
        else:
            errormsg = "OTP entered was incorrect"
            signup_status=True

    elif source == "forgot":
        if otpno == int(userotp):
            status = False
            forgot_status = True
        else:
            errormsg = "OTP entered was incorrect"

    return render_template("index.html", status=status, errormsg=errormsg, forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)

    
@app.route('/signup',methods=["POST","GET"])
def signup():
    global fname,lname,email,password,encpass
    fname=request.form['fname']
    lname=request.form['lname']
    email=request.form['email']
    password=request.form['password']
    con_password=request.form['con_password']
    if(password != con_password):
        errormsg = "Password and Confirm password didn't matched. Try Again"
        status=False
        forgot_status=False
        signup_status=True
        login_status=False
        return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)

    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user:
            errormsg = "Email Already exsist"
            signup_status=True
            login_status=False
            forgot_status=False
            status=False
            return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)
        
        global otpno
        global source
        source = "signup"
        otpno=change_otp()
        email = request.form['email']
        msg = Message('One Time Password',sender='atharvaphadke1231@outlook.com',recipients=[email])
        msg.body="Welcome to sign language detection.\nOTP for verification is : " +str(otpno) + "\nDo not share this OTP with anyone.\nThank You."
        mail.send(msg)
        status=True
        forgot_status=False
        signup_status=False
        login_status=False
        return render_template("index.html",status=status,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)

@app.route('/loginpass',methods=["POST","GET"])
def loginpass():
    status=False
    forgot_status=False
    signup_status=False
    login_status=False
    email=request.form['email']
    password=request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    useremail = cur.fetchone()
    if useremail:
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
        userpass_tuple = cur.fetchone()
        userpass = userpass_tuple[0]
        if(sha256_crypt.verify(password,userpass)):
            login_status = False
            session['email']=email
            cur.execute("SELECT fname FROM users WHERE email = %s", (email,))
            fname_tuple = cur.fetchone()
            fname = fname_tuple[0]
            return render_template('editor.html',fname=fname)
        else:
            errormsg="Password Incorrect"
            login_status = True
            return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)
    else:
        errormsg="User Not Found"
        login_status= True
        return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status) 

    
@app.route('/loginotp',methods=["POST"])
def loginotp():
    global email
    email=request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    if user:
        global otpno
        global source
        source = "login"
        otpno=change_otp()
        msg = Message('One Time Password',sender='atharvaphadke1231@outlook.com',recipients=[email])
        msg.body="Welcome to sign language detection.\nOTP for verification is : " +str(otpno) + "\nDo not share this OTP with anyone.\nThank You."
        mail.send(msg)
        status=True
        forgot_status=False
        signup_status=False
        login_status=False
        return render_template("index.html",status=status,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)
    else:
        status=False
        errormsg="User Not Found"
        forgot_status=False
        signup_status=False
        login_status=False
        return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)
    
@app.route('/forgotpass',methods=['POST',"GET"])
def forgotpass():
    global emailid,email
    email=request.form['email']
    emailid=email
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    if user:
        global otpno
        global source
        source = "forgot"
        otpno=change_otp()
        msg = Message('One Time Password',sender='atharvaphadke1231@outlook.com',recipients=[email])
        msg.body="Welcome to sign language detection.\nOTP for verification is : " +str(otpno) + "\nDo not share this OTP with anyone.\nThank You."
        mail.send(msg)
        status=True
        forgot_status=False
        signup_status=False
        login_status=False
        return render_template("index.html",status=status,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)
    else:
        status=False
        forgot_status=False
        signup_status=False
        errormsg="User Not Found"
        login_status=False
        return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)
    
@app.route('/changepass',methods=['POST'])
def changepass():
    global emailid
    password=request.form['password']
    con_password=request.form['con_password']    
    if(password != con_password):
        errormsg = "Password and Confirm password didn't matched. Try Again"
        status=False
        forgot_status=True
        signup_status=False
        return render_template("index.html",status=status,errormsg=errormsg,forgot_status=forgot_status,signup_status=signup_status)

    else:
        status=False
        errormsg ="Password change successful. Login Now" 
        forgot_status=False
        signup_status=False
        login_status=True
        encpass=sha256_crypt.encrypt(password)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password = %s WHERE email = %s", (encpass,emailid))
        mysql.connection.commit()
        cur.close()
        return render_template("index.html",status=status,forgot_status=forgot_status,signup_status=signup_status,login_status=login_status)       


if __name__=="__main__":
    app.run(debug = True)
