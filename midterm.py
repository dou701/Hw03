import os
import pack.modu as lib

db_name = "library.db"  # 資料庫名稱
lib.db_name = db_name # 將套件中儲存的資料庫預設名稱變更
users_file = "users.csv"  # 使用者檔
book_file = "books.json"  # 圖書檔
db_exist = os.path.exists(db_name)  # 存儲資料庫是否存在(True=存在,False=不存在)

  # 檢查資料庫檔 library.db 是否存在
if not db_exist:  # 資料庫不存在
    db_exist = lib.establish_newsql(users_file, book_file)  # 建立新資料庫(成功後db_exist變更為True)

if db_exist:  # 確認資料庫是否存在或是否建立成功
  lib.login()  # 登入帳號密碼
  lib.show_menu()  # 顯示清單