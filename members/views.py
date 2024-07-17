from django.shortcuts import render, redirect # render 函式用於渲染模板，渲染模板是將動態生成的內容（如從數據庫中查詢得到的資料）通過渲染模板的過程嵌入到這些模板中，最終生成完整的 HTML 頁面
from django.http import JsonResponse    # 返回 JSON 格式的響應
from .models import Member  # 導入了 Member 模型，用於操作會員數據
from django.views.decorators.csrf import csrf_exempt    # 為了免於CSRF驗證
from django.contrib.auth.decorators import login_required  # 用於檢查用戶是否已登入
import json # 用於處理 JSON 數據
import subprocess
import os

# 這是一個裝飾器，用於豁免特定視圖的跨站請求偽造（CSRF）保護。Django 默認啟用 CSRF 保護來防止惡意站點發送跨站請求。
# 這裡 @csrf_exempt 裝飾器被用於 register 視圖函數上，表示對這個視圖的請求不進行 CSRF 驗證。
@csrf_exempt
def register(request):
    # 檢查請求的 HTTP 方法是否為 POST
    # 在 Web 應用中，POST 方法通常用於提交表單數據。對於註冊功能，我們期望從用戶處接收到 POST 請求，包含他們希望使用的用戶名和密碼。
    if request.method == 'POST':
        # 解析 JSON 數據
        # request.body : 請求的原始正文
        # json.loads() 函數將這個 JSON 字符串轉換為 Python 字典。然後，從這個字典中提取 username 和 password
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        # 試圖從 Member 模型中查找一個已經使用該 username 的實例
        # 查詢成功，表示用戶名已被使用，則返回一個 JSON 響應，通知用戶該用戶名不可用。
        try:
            Member.objects.get(username=username)
            return JsonResponse({'status': 'error', 'message': '該用戶名已被使用！'})
        except Member.DoesNotExist: #如果沒有找到，則捕獲 Member.DoesNotExist 異常，繼續執行後面的註冊邏輯
            # 如果用戶名未被占用，則創建一個新的 Member 實例，將解析得到的 username 和 password 賦值給它
            # 調用 .save() 方法將其保存到數據庫中。然後，返回一個 JSON 響應，告知用戶註冊成功。
            member = Member(username=username, password=password)
            member.save()
            return JsonResponse({'status': 'success', 'message': '註冊成功！'})
    # 如果不是POST請求，將向用戶返回註冊表單的 HTML 頁面
    return render(request, 'register.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 解析JSON數據
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            # 查詢資料庫中是否存在該用戶名的會員
            member = Member.objects.get(username=username)
            # 如果存在，進行密碼驗證，返回一個成功的 JSON 響應，表示登入成功，並包含一個歡迎訊息和一個重定向 URL
            if member.password == password:
                welcome_message = f'歡迎，{username} 先生/女士'
                request.session['username'] = username  # 將用戶名存入 session
                return JsonResponse({'success': True, 'message': '登入成功！', 'welcome_message': welcome_message, 'redirect': '/game_selection/'})
            # 如果密碼不匹配，我們返回一個失敗的 JSON 響應，表示帳號或密碼錯誤
            else:
                return JsonResponse({'success': False, 'message': '帳號或密碼錯誤！'})
        except Member.DoesNotExist:
            # 如果不存在該用戶名的會員，返回錯誤訊息
            return JsonResponse({'success': False, 'message': '帳號尚未註冊！'})
    return render(request, 'member-login-register.html')

@login_required
def game_selection(request):
    username = request.session.get('username', 'Guest')  # 從 session 中獲取用戶名
    return render(request, 'game_selection.html', {'username': username})

def hit_bricks(request):
    flask_server_path = os.path.join(os.path.dirname(__file__), '../flask_servers/hit_bricks_server.py')
    subprocess.Popen(['python', flask_server_path])
    username = request.session.get('username', 'Guest')  # 從 session 中獲取用戶名
    return render(request, 'hit_bricks.html', {'username': username})

def hungry_snake(request):
    flask_server_path = os.path.join(os.path.dirname(__file__), '../flask_servers/hungry_snake_server.py')
    subprocess.Popen(['python', flask_server_path])
    username = request.session.get('username', 'Guest')  # 從 session 中獲取用戶名
    return render(request, 'hungry_snake.html', {'username': username})