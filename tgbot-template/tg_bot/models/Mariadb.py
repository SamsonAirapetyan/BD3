import mariadb


class Database:
    def __init__(self):
        self.cur: mariadb.Cursor

    async def create(self):
        try:
            conn = mariadb.connect(
                user="root",
                password="1234",  #смена пароля
                host="localhost",
                port=3306,
                database="repair_work"  #смена названия БД
            )
            self.cur = conn.cursor()
            conn.autocommit = True
            print("sucsses!")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

    def add_device(self, Id: int, Name: str, Type: str, Date: str):
        sql = "INSERT INTO device VALUES (?, ?, ? ,?);"   #замена таблицы
        print(sql)
        self.cur.execute(sql, (Id, Name, Type, Date))

    def add_worker(self, Id: int, Surname: str, Name: str, Patronymic: str, Category: int, Date: str):
        sql = "INSERT INTO worker VALUES (?, ?, ? ,?, ?, ?);"  #замена таблицы
        print(sql)
        self.cur.execute(sql, (Id, Surname, Name, Patronymic, Category, Date))

    def add_Work_Repair(self, Id: int, Id_master: int, Name: str, Date: str, Type: str, Cost: int, Cod: int):  #замена входных данных
        sql = "INSERT INTO work_repair VALUES (?, ?, ? ,?, ? , ? , ?);"  #замена таблицы
        print(sql)
        self.cur.execute(sql, (Id, Id_master, Name, Date, Type, Cost, Cod))

    def count_of_device(self):
        sql = "SELECT count(Code_device) FROM device"  #
        self.cur.execute(sql)
        answer = self.cur.fetchone()
        return answer

    def sum_cost(self):
        sql = "SELECT SUM(Cost_repair) as sum FROM work_repair"
        self.cur.execute(sql)
        answer = self.cur.fetchone()
        return answer

    def select_device(self, Id: int):
        sql = "SELECT * FROM device WHERE Code_device = ?"
        self.cur.execute(sql, Id)
        return self.cur.fetchall()