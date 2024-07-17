from flask import Flask, render_template, send_from_directory
import subprocess

app = Flask(__name__, template_folder='../templates')  # 指定模板目錄

@app.route('/start_game')
def start_game():
    subprocess.Popen(['python', 'static/members/Hit_Bricks_app/hitbricks.py'])
    return "Game started!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
