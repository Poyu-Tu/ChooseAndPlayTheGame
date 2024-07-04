# 在Django上實現會員註冊登入系統(The implementation of member registration and login on Django)

這是一個使用 Django 框架開發的會員註冊與登入的作品，包含前端設計與資料庫，以下稱本作品。

## 目錄

- [簡介](#簡介)
- [安裝](#安裝)
- [使用方法](#使用方法)
- [功能](#功能)
- [貢獻](#貢獻)
- [授權](#授權)

## 簡介

本作品是一個用於展示會員註冊與登入功能的 Django 專案，包含前端設計(HTML、CSS、JavaScript)和資料庫(SQLite)配置。

## 安裝

以下是安裝步驟：

```bash
# 獲取本作品所有檔案👇
git clone https://github.com/Poyu-Tu/The-implementation-of-member-registration-and-login-on-Django.git
```
```bash
# 進入本作品目錄👇
cd django_member_register_login
```
```bash
# 建立虛擬環境👇
python3 -m venv env
```
```bash
# 啟動虛擬環境👇
source env/bin/activate # 對於 Windows 系統，請使用 `env\Scripts\activate`
```
```bash
# 安裝依賴👇
pip install -r requirements.txt
```
```bash
# 遷移資料庫👇
python manage.py migrate
```
```bash
# 啟動開發伺服器👇
python manage.py runserver
```

## 使用方法

啟動開發伺服器後，可以在瀏覽器中打開 [http://127.0.0.1:8000](http://127.0.0.1:8000) 查看專案。

1. 在瀏覽器中輸入上述網址。
2. 你將看到會員登入頁面，可以使用已註冊的帳號密碼進行登入。
3. 如果你沒有帳號，可以點擊“註冊”按鈕，進入註冊頁面進行註冊。
4. 填寫註冊表單後，提交註冊訊息。
5. 註冊成功後，將自動跳轉回登入頁面，使用新註冊的帳號進行登入。
6. 這裡登入後，預設會進入YouTube的首頁。

## 功能

- 會員註冊：用戶可以在註冊頁面創建新帳號。
- 會員登入：已註冊用戶可以使用帳號和密碼登入系統。
- 會員資料管理：登入後可以查看和管理個人資料，詳細使用方式請參考[此處](CreateDjangoSuperuser)。

## 貢獻

歡迎任何形式的貢獻！如果你想要貢獻，請遵循以下步驟：

1. **Fork 本儲存庫**：點擊 GitHub 頁面右上角的 "Fork" 按鈕。
2. **創建分支**：在你的儲存庫中創建一個新分支來開發你的變更。
```bash
git checkout -b feature-branch
```
3. **提交更改**：將你的變更提交到該分支。
```bash
git commit -m "Add some feature"
```
4. **推送到 GitHub**：將你的分支推送到 GitHub。
```bash
git push origin feature-branch
```
5. **開 Pull Request**：在 GitHub 上開一個 Pull Request，描述你的變更，等待維護者的審核與合併。

## 授權

此專案採用 MIT 授權條款。詳情請參閱 [LICENSE 文件](LICENSE)。