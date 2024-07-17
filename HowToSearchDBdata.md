## 如何查詢資料庫中的會員帳號及密碼
1. 進入根目錄並打開終端機。
2. 開始輸入指令🔻
```bash
python manage.py shell
```
```bash
# 查詢全部DB中的資料
from members.models import Member
members = Member.objects.all()
print(f'{"Number":<10} {"Username":<20} {"Password":<20}')  # 打印表頭
for index, member in enumerate(members, start=1):   # 迴圈生成每筆資料
    print(f'{index:<10} {member.username:<20} {member.password:<20}')
    
print(f'------------\n總筆數: {members.count()}')   # 打印總筆數
```
```bash
# 刪除單筆
from members.models import Member 
del = Member.objects.filter(username='xxx').delete()
print('刪除成功')
```
```bash
# 刪除全部
from members.models import Member 
Member.objects.all().delete()
print('刪除成功')
```