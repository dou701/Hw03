import sqlite3
import csv
import json

db_name = "library.db"  # 資料庫名稱

  # 建立資料庫檔案(輸入資料庫名稱.db, 使用者檔, 圖書檔)
def establish_newsql(user_file, books_file):
    '''
    1.建立資料庫，傳入參數為資料庫名稱。
    2.建立資料表，users儲存帳號密碼，books儲存書的資訊。
    3.讀取csv和json，將資料新增進資料表內。
    '''
    success = True # 儲存是否建立成功，預設為成功，如果發生錯誤會更改為False
    try:
          # 連接資料庫，不存在則會建立一個
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()  # 建立 cursor 物件
          # 建立資料表: 【users】
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users 
                (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL)'''
        )
          # 建立資料表: 【books】
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS books
                (book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publisher TEXT NOT NULL,
                    year INTEGER NOT NULL)'''
        )
          # 開啟 users.csv 檔案將內容資料新增至 users 資料表
        with open(user_file, newline='') as csvfile:
            csv_rows = csv.reader(csvfile)
            next(csv_rows)  # 跳過第一行標題
            for row in csv_rows:  #使用迴圈讀取每一行
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (row[0], row[1]))  # 新增資料至 users 資料表
            conn.commit()  # 儲存變更
        # 開啟 books.json 檔案將內容資料新增至 books 資料表
        with open(books_file,'r', encoding="utf-8") as file:
            json_rows = json.load(file)#讀取資料
            for row in json_rows:
                # 新增資料至 books 資料表
                cursor.execute("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ? ,?)", (row.get("title"), row.get("author"), row.get("publisher"), row.get("year")))
            conn.commit()  # 儲存變更
    except FileNotFoundError:
        print('找不到檔案...')
        success = False  # 變更為False(建立失敗)
    except Exception as e:
        print('開檔發生錯誤...')
        print(e)
        success = False  # 變更為False(建立失敗)
    finally:  # 確保無論是否發生例外都會關閉資料庫連線
        cursor.close()  # 關閉 cursor 物件
        conn.close()  # 關閉資料庫連線
        return success  # 回傳是否建立成功

#帳號密碼登入
def login():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()  # 建立 cursor 物件
    while(True):
        account = input("請輸入帳號：")
        password = input("請輸入密碼：")
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (str(account), str(password)))
        user = cursor.fetchone()  # 讀取資料庫一行
        if user:  #有讀取到資料,而且帳號密碼正確，則關閉連線後回傳true
            cursor.close()  # 關閉 cursor 物件
            conn.close()  # 關閉資料庫連線
            return True

#顯示登入畫面
def show_menu():
    while(True):
        print("\n-------------------")
        print("    資料表 CRUD")
        print("-------------------")
        print("    1. 增加記錄")
        print("    2. 刪除記錄")
        print("    3. 修改記錄")
        print("    4. 查詢記錄")
        print("    5. 資料清單")
        choose = str(input("選擇要執行的功能(Enter離開)："))
        if (len(choose)>0):  # 輸入不是空的
            match choose:
                case '1':
                    insert_data()  # 增加記錄
                case '2':
                    delete_data()  # 刪除記錄
                case '3':
                    update_data()  # 修改記錄
                case '4':
                    select_data()  # 查詢記錄
                case '5':
                    show_all_data()  # 資料清單
                case default:
                    print("=>無效的選擇")
        else:  #Enter結束
            break

  # 功能一 增加記錄
def insert_data():
    try:
        conn = sqlite3.connect(db_name)  # 連線資料庫
        cursor = conn.cursor()  # 建立 cursor 物件

        title = str(input("請輸入要新增的標題：")).strip()  # 去除頭尾空白，也能防止只輸入空格
        author = str(input("請輸入要新增的作者：")).strip()  # 去除頭尾空白，也能防止只輸入空格
        publisher = str(input("請輸入要新增的出版社：")).strip()  # 去除頭尾空白，也能防止只輸入空格
        year = str(input("請輸入要新增的年份：")).strip()  # 去除頭尾空白，也能防止只輸入空格

        if(len(title)>0 and len(author)>0 and len(publisher)>0 and len(year)>0):  # 檢查是否都有輸入
            cursor.execute("SELECT title FROM books WHERE title = '{}'".format(title))
            result_all = cursor.fetchall()  # 讀取所有資料
            if(len(result_all) == 0):  # 查詢資料表中是否有此書名
                cursor.execute("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)", (title, author, publisher, year))
                conn.commit()  # 儲存變更
                print("異動記錄")
                show_all_data()  # 顯示所有資料
            else:
                print("=>書名重複，無法進行新增作業")
        else:
            print("=>給定的條件不足，無法進行新增作業")
    except Exception as e:
        print('發生錯誤...')
        print(e)
    finally:  # 確保無論是否發生例外都會關閉資料庫連線
        cursor.close()  # 關閉 cursor 物件  # 關閉資料庫連線
        conn.close()  # 關閉資料庫連線

  # 功能二 刪除記錄
def delete_data():
    try:
        show_all_data()  # 顯示所有資料
        conn = sqlite3.connect(db_name)  # 連線資料庫
        cursor = conn.cursor()  # 建立 cursor 物件

        title = str(input("請問要刪除哪一本書？：")).strip()  # 去除頭尾空白，也能防止只輸入空格
        if(len(title)>0):  # 檢查是否有輸入
            cursor.execute("SELECT title FROM books WHERE title = '{}'".format(title))
            result_all = cursor.fetchall()  # 讀取所有資料
            if(len(result_all) > 0):  # 查詢資料表中是否有此書名
                cursor.execute('DELETE FROM books WHERE title = ?', (title,))
                conn.commit()  # 儲存變更
                print("異動記錄")
                show_all_data()  # 顯示所有資料
            else:
                print("=>無此書名，無法進行刪除作業")
        else:
            print("=>給定的條件不足，無法進行刪除作業")
    except Exception as e:
        print('發生錯誤...')
        print(e)
    finally:  # 確保無論是否發生例外都會關閉資料庫連線
        cursor.close()  # 關閉 cursor 物件  # 關閉資料庫連線
        conn.close()  # 關閉資料庫連線

  # 功能三 修改記錄
def update_data():
    try:
        show_all_data()  # 顯示所有資料
        conn = sqlite3.connect(db_name)  # 連線資料庫
        cursor = conn.cursor()  # 建立 cursor 物件

        title = str(input("請問要修改哪一本書的標題？：")).strip()  # 去除頭尾空白，也能防止只輸入空格
        new_title = str(input("請輸入要更改的標題：")).strip()  # 去除頭尾空白，也能防止只輸入空格
        author = str(input("請輸入要更改的作者：")).strip()  # 去除頭尾空白，也能防止只輸入空格
        publisher = str(input("請輸入要更改的出版社：")).strip()  # 去除頭尾空白，也能防止只輸入空格
        year = str(input("請輸入要更改的年份：")).strip()  # 去除頭尾空白，也能防止只輸入空格

        if(len(title)>0 and len(new_title)>0 and len(author)>0 and len(publisher)>0 and len(year)>0):  # 檢查是否有輸入
            cursor.execute("SELECT title FROM books WHERE title = '{}'".format(title))
            result_all = cursor.fetchall()  # 讀取所有資料
            if(len(result_all) > 0):  # 查詢資料表中是否有此書名
                cursor.execute('UPDATE books SET title=?, author=?, publisher=?, year=? WHERE title=?', (new_title, author, publisher, year, title))
                conn.commit()  # 儲存變更
                print("異動記錄")
                show_all_data()  # 顯示所有資料
            else:
                print("=>無此書名，無法進行修改作業")
        else:
            print("=>=>給定的條件不足，無法進行修改作業")
        
    except Exception as e:
        print('發生錯誤...')
        print(e)
    finally:  # 確保無論是否發生例外都會關閉資料庫連線
        cursor.close()  # 關閉 cursor 物件  # 關閉資料庫連線
        conn.close()  # 關閉資料庫連線

  # 功能四 查詢記錄
def select_data():
    try:
        conn = sqlite3.connect(db_name)  # 連線資料庫
        cursor = conn.cursor()  # 建立 cursor 物件

        input_text = str(input("請輸入想查詢的關鍵字：")).strip()  # 去除頭尾空白
        cursor.execute("SELECT title, author, publisher, year FROM books WHERE title LIKE '%{}%' OR author LIKE '%{}%'".format(input_text, input_text))  #執行SQL語法查詢

        result_all = cursor.fetchall()  # 讀取所有資料
        if(len(result_all)>0):  #是否有資料
            print("|　　　　書名　　　　|　　　　作者　　　　|　　　出版社　　　　| 年份 |")
            for row in result_all:
                print(f"|{row[0]:{chr(12288)}<10}|{row[1]:{chr(12288)}<10}|{row[2]:{chr(12288)}<10}|{row[3]:{chr(12288)}<6}|")
        else:
            print("查無資料")
    except Exception as e:
        print('發生錯誤...')
        print(e)
    finally:  # 確保無論是否發生例外都會關閉資料庫連線
        cursor.close()  # 關閉 cursor 物件
        conn.close()  # 關閉資料庫連線

  # 功能五 資料清單
def show_all_data():
    try:
        conn = sqlite3.connect(db_name)  # 連線資料庫
        cursor = conn.cursor()  # 建立 cursor 物件
        cursor.execute("SELECT title, author, publisher, year FROM books")  #執行SQL語法查詢

        result_all = cursor.fetchall()  # 讀取所有資料
        if(len(result_all)>0):  #是否有資料
            print("|　　　　書名　　　　|　　　　作者　　　　|　　　出版社　　　　| 年份 |")
            for row in result_all:
                print(f"|{row[0]:{chr(12288)}<10}|{row[1]:{chr(12288)}<10}|{row[2]:{chr(12288)}<10}|{row[3]:<6}|")
        else:
            print("查無資料")
    except Exception as e:
        print('發生錯誤...')
        print(e)
    finally:  # 確保無論是否發生例外都會關閉資料庫連線
        cursor.close()  # 關閉 cursor 物件
        conn.close()  # 關閉資料庫連線
