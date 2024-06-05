function login_otp() {
    document.getElementById('id01').style.display='none';
    document.getElementById('id03').style.display='none';
    document.getElementById('id04').style.display='none';
    document.getElementById('id02').style.display='block';
}

function login_password() {
    document.getElementById('id02').style.display='none';
    document.getElementById('id03').style.display='none';
    document.getElementById('id04').style.display='none';
    document.getElementById('id01').style.display='block';
}

function forgot_password() {
    document.getElementById('id01').style.display='none';
    document.getElementById('id03').style.display='block';
}

function signup() {
    document.getElementById('id01').style.display='none';
    document.getElementById('id02').style.display='none';
    document.getElementById('id04').style.display='block';
}

function check_status(){
    var otpstatus = JSON.parse(document.getElementById("pythonData").getAttribute("otp_status"))
    var forgotstatus = JSON.parse(document.getElementById("pythonData2").getAttribute("forgot_status"))
    var signupstatus = JSON.parse(document.getElementById("pythonData3").getAttribute("signup_status"))
    var loginstatus = JSON.parse(document.getElementById("pythonData4").getAttribute("login_status"))
    if(otpstatus){
        document.getElementById('id05').style.display='block';
        document.getElementById('id01').style.display='none';
        document.getElementById('id02').style.display='none';
        document.getElementById('id03').style.display='none';
        document.getElementById('id04').style.display='none';
        document.getElementById('id06').style.display='none';
    }
    else if(forgotstatus){
        document.getElementById('id06').style.display='block';
        document.getElementById('id01').style.display='none';
        document.getElementById('id02').style.display='none';
        document.getElementById('id03').style.display='none';
        document.getElementById('id04').style.display='none';
        document.getElementById('id05').style.display='none';
    }
    else if(signupstatus){
        document.getElementById('id04').style.display='block';
        document.getElementById('id01').style.display='none';
        document.getElementById('id02').style.display='none';
        document.getElementById('id03').style.display='none';
        document.getElementById('id05').style.display='none';
        document.getElementById('id06').style.display='none';
    }
    else if(loginstatus){
        document.getElementById('id01').style.display='block';
        document.getElementById('id02').style.display='none';
        document.getElementById('id03').style.display='none';
        document.getElementById('id04').style.display='none';
        document.getElementById('id05').style.display='none';
        document.getElementById('id06').style.display='none';
    }
}

