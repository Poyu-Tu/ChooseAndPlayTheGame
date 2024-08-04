from django.urls import path    # 用於定義 URL 路由
from . import views # 導入了當前應用程式（或模組）中的 views 模組，用於處理請求並返回響應

# urlpatterns：URL 路由列表，包含了所有的路由配置
urlpatterns = [
    path('', views.login, name='home'),  # 根路徑指向登錄頁面
    path('login/', views.login, name='login'),  # 假設你有一個登錄視圖
    path('register/', views.register, name='register'),  # 假設你有一個註冊視圖
    path('game_selection/', views.game_selection, name='game_selection'),
    path('hit_bricks/', views.hit_bricks, name='hit_bricks'),
    path('hungry_snake/', views.hungry_snake, name='hungry_snake'),
    path('api/login/', views.login, name='api_login'),  # 登入 API 的路由
    path('api/register/', views.register, name='api_register'),  # 註冊 API 的路由
]