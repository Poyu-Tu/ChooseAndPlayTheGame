# Choose and Play The Game ☺️

這是一款使用 Django 和 Flask 框架開發的街機遊戲應用程式集，包含前後端設計與資料庫串街，以下稱本作品。

## 目錄

- [簡介](#簡介)
- [安裝](#安裝)
- [使用方法](#使用方法)
- [功能](#功能)
- [遊戲列表](#遊戲列表)
- [貢獻](#貢獻)
- [授權](#授權)

## 簡介

本作品整體是透過 Django 框架開發，在前台運用會員註冊及登入的功能，來與後台的 SQL Server 資料庫串接並驗證，以進入使用 Flask 框架所包裝的街機遊戲選擇與遊玩之應用程式集。整體前端設計使用 HTML、CSS、JavaScript 技術，後端開發使用 Python 語言。

## 安裝

以下是安裝步驟：

```bash
# 獲取本作品所有檔案
git clone https://github.com/Poyu-Tu/ChooseAndPlayTheGame.git
```
```bash
# 進入本作品目錄
cd ChooseAndPlayTheGame
```
```bash
# 建立虛擬環境
python3 -m venv env
```
```bash
# 啟動虛擬環境
source env/bin/activate # Mac 作業系統
source env\Scripts\activate # Windows 作業系統
```
```bash
# 安裝依賴
pip install -r requirements.txt
```
```bash
# 遷移資料庫
python manage.py migrate
```
ℹ️ 以下需於終端機的地方開啟三個分頁
```bash
# 啟動包裝 Hit bricks 遊戲的 Flask 開發伺服器
python flask_servers\hit_bricks_server.py
```
```bash
# 啟動包裝 Hungry snake 遊戲的 Flask 開發伺服器
python flask_servers\hungry_snake_server.py
```
```bash
# 啟動開發伺服器 (啟動後，點選這裡的網址)
python manage.py runserver
```

## 使用方法

啟動開發伺服器後，可以在瀏覽器中打開 [http://127.0.0.1:8000](http://127.0.0.1:8000) 查看本作品。

1. 在瀏覽器中輸入上述網址。
2. 你將看到一個簡單介紹的彈出框，點選彈出框外後進入會員登入頁面，在這裡可以使用已註冊的帳號密碼進行登入。
3. 如果你沒有帳號，可以點擊“註冊”按鈕，進入註冊頁面進行註冊。
4. 填寫註冊表單後，提交註冊訊息。
5. 註冊成功後，將自動跳轉回登入頁面，使用新註冊的帳號進行登入。(確認資料庫中的資料可以[點此](HowToSearchDBdata.md))
6. 登入後會進入遊戲列表選擇遊戲，這裡包含遊戲的介紹與操作說明，可以點擊"切換遊戲"來做遊戲的切換，亦或是點選"回登入頁"，來回到會員登入頁面。
7. 點擊遊戲的名稱即會跳轉到該遊戲視窗及操作頁面，即可開始玩遊戲。(建議可開啟聲音來獲得更好的遊戲體驗!)
8. 若遊戲結束，會跳出在該遊戲所獲得的分數；若中離遊戲，將會回到該遊戲未啟動畫面。此時使用者可以選擇回上一頁或是重新開始遊戲。

## 功能

- 會員註冊：用戶可以在註冊頁面創建新帳號。
- 會員登入：已註冊用戶可以使用帳號和密碼登入遊戲列表選擇遊戲。
- 顯示登入的使用者名稱：在選擇遊戲畫面、遊戲操作頁面上方會顯示目前所登入的使用者名稱。
- 選擇遊戲：使用者可以在本頁瀏覽遊戲的說明、切換遊戲或回登入頁面。
- 遊戲視窗及操作頁面：使用者可透過跳出的遊戲視窗遊玩遊戲，遊戲結束後可以選擇是否重新啟動遊戲，或是回到選擇遊戲畫面。

## 遊戲列表

點擊下方遊戲名稱可查看該遊戲詳細資訊，遊戲持續推出更新......

- [打磚塊(Hit bricks)](Hit_bricks.md)：玩家需使用可移動的板塊接住並彈起小球，打擊上方的磚塊。
- [貪食蛇(Hungry snake)](Hungry_snake.md)：玩家需控制蛇吃到食物以增加長度，同時避免撞到牆壁或吃到自己。

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