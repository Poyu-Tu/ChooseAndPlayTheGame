// 等待整個HTML文件（DOM）完全加載並準備就緒後，再執行內部的JavaScript程式碼。
// $(document).ready 是jQuery提供的一個方法，確保網頁內容在完全加載後再執行我們的程式碼。
$(document).ready(function() {
    // 使用Bootstrap的模態框（modal）方法，將ID為welcomeModal的模態框顯示出來。
    // $('#welcomeModal') 是一個jQuery選擇器，用來選擇ID為welcomeModal的元素。
    // .modal('show') 則是Bootstrap模態框的方法，用來顯示該模態框。
    $('#welcomeModal').modal('show');

    // 為整個文檔（document）綁定一個點擊事件。當用戶在網頁的任意位置點擊時，這個事件處理器將會被觸發。
    // function(event) 是事件處理函數，event 參數包含了關於點擊事件的所有訊息。
    $(document).click(function(event) {
        // 檢查點擊事件的目標（即用戶點擊的元素）是否沒有在模態框內。
        // $(event.target) 選擇被點擊的元素。
        // .closest('.modal-content') 方法從點擊的元素開始向上查找，直到找到包含該元素的 .modal-content
        // .length 用來檢查是否找到這樣的元素。如果長度為0，則說明點擊不在模態框內。
        if (!$(event.target).closest('.modal-content').length) {
            // .modal('show') 則是Bootstrap模態框的方法，用來隱藏該模態框。
            $('#welcomeModal').modal('hide');
        }
    });
    
    // 獲取 CSRF token，getCookie 函數從瀏覽器的 cookie 中獲取 CSRF 令牌
    var csrftoken = getCookie('csrftoken');

    //getElementById("login-form") : 使用getElementById方法獲取id為login-form的元素
    //addEventListener("submit", function(event) : 添加表單提交事件的監聽器，提交時執行指定函數
    document.getElementById("login-form").addEventListener("submit", function(event){
        
        event.preventDefault(); //阻止表單默認提交行為，防止瀏覽器重新加載頁面，使JS可以處理表單提交，以便自定義驗證邏輯

        var username = document.getElementById("login-username").value; //獲取用戶輸入的帳號
        var password = document.getElementById("login-password").value; //獲取用戶輸入的密碼
        
        //fetch 是 JavaScript 提供的一個 API，用於發送網路請求。這裡我們發送了一個 POST 請求到 /login/ 路由
        fetch("/login/", {
            method : "POST",

            headers : {
                "Content-Type" : "application/json",    // 告訴Server請求主體是 JSON 格式的資料
                "X-CSRFToken": csrftoken // 取得 CSRF 令牌並添加到請求頭中，以防止 CSRF 攻擊
            },

            // 將用戶輸入的帳密使用JSON格式準備，以便發送給後端進行驗證
            body : JSON.stringify({
                username : username,
                password : password
            })
        })

        //Promise 的一個方法，用於處理當前 Promise 對象執行成功後的操作。使用 then 方法來處理從後端 API 返回的回應。
        .then(response => response.json())  // 使用箭頭函數將回應解析為 JSON 格式，然後進行後續處理
        .then(data => { // 接收從前一個 .then() 方法返回的 JSON 格式的回應作為參數，這個回應是從後端 API 返回的
            if(data.success){    // 檢查回應的狀態碼，如果回應中的 success 屬性為 true，則顯示登入成功的訊息，並根據回應中的 redirect 屬性重新導向用戶
                alert(data.message);
                alert(data.welcome_message);
                resetLoginForm();
                if (data.redirect) {
                    window.location.href = data.redirect;  // 重新定向到指定的 URL
                }
            }
            else{   // 如果回應中的 success 屬性為 false，則顯示相應的錯誤訊息。
                alert(data.message);
                resetLoginForm();
            }
        })

        // Promise 物件的另一個方法，用於捕獲當前 Promise 物件執行失敗時的錯誤。
        .catch(error => {   //是一個箭頭函數，這個函數接收一個參數 error，代表 Promise 物件執行時發生的錯誤。
            console.error("Error:", error);   //顯示錯誤訊息給用戶。這樣可以讓用戶知道發生了什麼錯誤，並且進行相應的處理。
            resetLoginForm();
        })
    });

    /*
        註冊按鈕監聽器
    */
    document.getElementById("go-to-register").addEventListener("click", function() {
        window.location.href = "/register/";
    });


    /*
        以下是方法
    */
    // 獲取 CSRF 令牌的函數
    function getCookie(name) {
        var cookieValue = null; // 聲明了一個名為 cookieValue 的變數，並初始化為 null
        if (document.cookie && document.cookie !== '') {    // 檢查瀏覽器的 cookie 是否存在且不為空。如果存在且不為空，進入 if 
            var cookies = document.cookie.split(';');   // 將瀏覽器的 cookie 字符串以分號（;）分割成一個包含多個 cookie 的數組 cookies
            for (var i = 0; i < cookies.length; i++) {  // 找與指定名稱匹配的 cookie
                var cookie = cookies[i].trim(); // 對每個 cookie 字符串進行去除空白字符，.trim():用於從字符串的開頭和末尾刪除空白字符，返回刪除空白字符後的新字符串
                // 如果找到匹配的 cookie 名稱，則解析 cookie 字符串，取出名稱之後的值，並對其進行 URI 解碼，然後賦值給 cookieValue
                if (cookie.substring(0, name.length + 1) === (name + '=')) {    // 檢查某個 cookie 字符串是否以特定名稱開頭的，如果是的話，表示找到了對應的 cookie
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 用於重置登入表單中的用戶名和密碼輸入框
    function resetLoginForm() {
        document.getElementById("login-username").value = "";
        document.getElementById("login-password").value = "";
    }
})