document.addEventListener("DOMContentLoaded", function() { 
    var csrftoken = getCookie('csrftoken');  // 取得 CSRF token 的函數

    document.getElementById("register-form").addEventListener("submit", function(event){
        
        event.preventDefault();

        var username = document.getElementById("register-username").value;
        var password1 = document.getElementById("register-password1").value;
        var password2 = document.getElementById("register-password2").value;

        if(password1 != password2){
            alert("兩次輸入的密碼不相符，請再次確認!");
            document.getElementById("register-password1").value = "";
            document.getElementById("register-password2").value = "";
            return;
        }
        else{
            fetch("/api/register/", {
                method : "POST",
                headers : {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body : JSON.stringify({ username : username, password : password1 })
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === "success") {
                    alert(data.message);
                    resetRegisterForm();
                    window.location.href = "/login/";    //註冊成功將導回登入畫面
                } 
                else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                resetRegisterForm();
            });
        }
    });

    /*
        以下是方法
    */
    // 獲取 CSRF 令牌的函數
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function resetRegisterForm(){
        document.getElementById("register-username").value = "";
        document.getElementById("register-password1").value = "";
        document.getElementById("register-password2").value = "";
    }
})