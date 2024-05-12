import sqlite3, datetime


def connect_db():
    return sqlite3.connect("abc.db")


class Models:
    @staticmethod
    def register_customer(connection, name, age, gender, city, email, password, balance,account_type, username):
        current_year = datetime.datetime.now().year
        cur = connection.cursor()
        with connection:
            cur.execute("INSERT INTO customers "
                        "(name, age, gender, city, email,"
                        " password, balance,account_type, username) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (name, age, gender, city, email, password, balance,account_type, username))
            last_id = cur.lastrowid
            acc_num = f"{current_year}{last_id:05d}"  # Example: 202300001
            cur.execute("UPDATE customers SET acc_num = ? WHERE rowid = ?", (acc_num, last_id))
            return acc_num
    
    @staticmethod
    def delete_customer(connection, acc_num):
        cur = connection.cursor()
        with connection:
            cur.execute("delete from customers where acc_num = (?) ", (acc_num,))
            affected_rows = cur.rowcount
            if affected_rows:
                return cur.execute("select acc_num from customers"
                                   " order by acc_num desc limit 1").fetchone()
            else:
                return None
            
    @staticmethod
    def view_all_customers(connection):
        cur = connection.cursor()
        with connection:
            table = cur.execute("select * from customers").fetchall()
            print(table)
            return table


            
    @staticmethod
    def view_one_customers(connection, acc_num):
        cur = connection.cursor()
        with connection:
            cur.execute("select * from customers where acc_num = (?)",(acc_num,))
            

def main():
    connection = connect_db()
    try:
        cur = connection.cursor()
        cur.execute("create table if not exists customers ("
                    "s_no integer primary key AUTOINCREMENT,acc_num integer,"
                    "name text, age integer, gender text, city text, email text,"
                    "password text, balance integer,account_type text, username text)")

        # Example usage:
        # acc_num = Models.register_customer(connection, "omkar", 22, \
        # "Male", "Pune", "ok@gmail.com", "sdkgf&*R^4", 50000, "savings", "omkar123")
        # print(f"New account number: {acc_num}")
        # print(Models.delete_customer(connection, 5))
        #
        # acc_num = Models.register_customer(connection, "Raj", 22, \
        # "Male", "PCMC", "r@gmail.com", "sdkgf&*R^4", 500000, "savings", "raj")
        # print(f"New account number: {acc_num}")
        #
        # acc_num = Models.register_customer(connection, "hitesh", 22, \
        # "Male", "PCMC", "h@gmail.com", "sdkgf&*R^4", 500000, "savings", "hitman")
        # print(f"New account number: {acc_num}")
        #
        # acc_num = Models.register_customer(connection, "Prateek", 22, \
        # "Male", "PCMC", "p@gmail.com", "sdkgf&*R^4", 500000, "savings", "Prat")
        # print(f"New account number: {acc_num}")

        # print(Models.delete_customer(connection,202400002))


    finally:
        connection.close()


if __name__ == "__main__":
    main()
