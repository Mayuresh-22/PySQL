import sys
from tabulate import tabulate
from authorize import Authorization as auth


class PySQL():

    def __init__(self):
        obj = auth()
        mes = obj.login()

        if mes is None or mes is False:
            sys.exit(f"{' ':<2}Login failed...")
        else:
            print(f"\n{' ':<2}Successfully Logged In...\n")
            self.queries()


# --- take initial queries as an input
    def queries(self):
        ddl = ["create database", "open database"]
        while True:
            try:
                query = input(f"{' ':<2}> ").strip()
                query_lis = query.split()
                if f"{query_lis[0]} {query_lis[1]}" in ddl:
                    self.operate(query)
                else:
                    self.parse(query)
            except KeyboardInterrupt:
                print("\n")
                break


# --- Performs starting operations on DDL commands
    def operate(self, query):

        # checks starting query
        cmd_lis = query.split()
        try:
            if len(cmd_lis) != 3:
                raise ValueError(f"{' ':<2}: Invalid Command")

            # open database
            '''
            This commands opens existing database.
            After opening the database
            further operations can be performed on it.

            Note: To perform operations on database
            it is necessary to open the database first it first.
            Syntax:
                > OPEN DATABASE {database_name}
            '''
            if cmd_lis[0].lower() == "open" and cmd_lis[1].lower() == "database":
                dbname = cmd_lis[2]
                with open(f"./database/{dbname}.json", "r") as f:
                    db_data = f.read()
                print(f"{' ':<2}Success: Database Opened")
                self.sub_operate(eval(db_data), dbname)

            # create database
            '''
            This command creates a new database.
            Syntax:
                > CREATE DATABASE {database_name}
            '''
            if cmd_lis[0].lower() == "create" and cmd_lis[1].lower() == "database":
                db_data = {}
                dbname = cmd_lis[2]
                with open(f"./database/{dbname}.json", "w") as f:
                    f.write(str(db_data))
                print(f"{' ':<2}Success: Database Created")
                self.sub_operate(db_data, dbname)

        except ValueError as e:
            print(e)
        except FileNotFoundError:
            print(f"{' ':<2}Database with name '{dbname}' doesn't exist")


# --- Performs starting operations on DML commands
    def sub_operate(self, db_data=None, dbname=None):
        while True:
            try:
                query = input(f"{' ':<2}>> ").strip()
                query_lis = query.split()
                if query_lis[0].lower() == "close" and query_lis[1].lower() == "database":
                    print(f"{' ':<2}Success: Database Closed")
                    break
                else:
                    self.parse(query, db_data, dbname)
            except KeyboardInterrupt:
                print("\n")
                break


    # --- Parsing the query
    def parse(self, query, db_data=None, dbname=None):
        try:
            cmd_lis = query.split()
            if cmd_lis[0].lower() == "create":
                self.create_cmd(cmd_lis, db_data, dbname)
            if cmd_lis[0].lower() == "insert":
                self.insert_cmd(cmd_lis, db_data, dbname)
            if cmd_lis[0].lower() == "view":
                self.view_cmd(cmd_lis, db_data, dbname)
        except KeyboardInterrupt:
            print("\n")


    # --- datbase operation commands
    def create_cmd(self, cmd_lis, db_data, db_name):
        cmd = ["table"]
        ''' --- Create Table:
        if its a create table command
        '''
        if cmd_lis[1].lower() in cmd:
            self.table(cmd_lis, db_data, db_name)


    def insert_cmd(self, cmd_lis, db_data, db_name):
        cmd = ["into"]
        if cmd_lis[1].lower() in cmd:
            self.insert(cmd_lis, db_data, db_name)

    def view_cmd(self, cmd_lis, db_data, db_name):
        cmd = ["from"]
        if cmd_lis[2].lower() in cmd:
            self.view(cmd_lis, db_data, db_name)

    # --- methods to perform DML commands ---

    # # Create Table
    def table(self, cmd_lis, db_data, dbname):
        # --- Create Table
        '''
        This query is used to create the table in the databases with the column
        names specified in the query
        '''
        try:
            # empty table
            tbname = cmd_lis[2].strip()
            db_data[tbname] = {}

            # table columns
            colname = cmd_lis[3].replace("(", "").replace(")", "")
            colname = tuple(map(str, colname.split(',')))

            for _ in colname:
                db_data[tbname][_] = []

            # cleaning before wrting it to file
            data = repr(db_data).replace("'", '"')
            with open(f"./database/{dbname}.json", "w") as f:
                f.write(data)
        except IndexError:
            print(f"{' ':<2}: Invalid Command")


    # # Insert in Table
    def insert(self, cmd_lis, db_data, dbname):
        # --- Insert data in table/columns
        '''
        This Insert query is used to insert new records to the database tables
        It inserts values to the columns specified in the query, in case column
        name is not specified "null" value is inserted in that particular column 
        syntax:
            > INSERT INTO {table_name} ({columns}) ({values})
        '''
        try:
            # table
            tbname = cmd_lis[2]
            # gathering table column names in tuple
            colname = cmd_lis[3].replace("(", "").replace(")", "")
            colname = tuple(map(str, colname.split(',')))

            # gathering values in tuple
            values = cmd_lis[4].replace("(", "").replace(")", "")
            values = tuple(map(str, values.split(',')))

            # inserting values in table
            i = 0
            col = list(db_data[tbname].keys())
            for _ in col:
                if _ in colname:
                    db_data[tbname][_].append(values[i].replace('"', ''))
                    i += 1
                else:
                    db_data[tbname][_].append("null".replace('"', ''))

            # cleaning before wrting it to file
            data = repr(db_data).replace("'", '"')
            with open(f"./database/{dbname}.json", "w") as f:
                f.write(data)

        except IndexError:
            print(f"{' ':<2}: Invalid Command")
        except KeyError:
            print(f"{' ':<2}: Column not found")

    # # View table
    def view(self, cmd_lis, db_data, dbname):
        # -- View entire table records
        '''
        View query is used to view the contents of the databases.

        syntax:
            > VIEW ({columns}) FROM {tablename}
        '''
        try:
            # table
            tbname = cmd_lis[3]
            # raise error if table not found
            if tbname not in db_data:
                raise KeyError

            # columns
            colname = cmd_lis[1].replace("(", "").replace(")", "")
            colname = tuple(map(str, colname.split(',')))
            if colname[0] == "*":
                colname = db_data[tbname].keys()

            viewtemp = {_: db_data[tbname][_] for _ in colname}
            print(f"\n{' ':<2}TABLE: {tbname}")
            print(tabulate(viewtemp, headers="keys", tablefmt="grid"), "\n")

        except IndexError:
            print(f"{' ':<2}: Invalid Command")

        except KeyError:
            print(f"{' ':<2}: No {tbname} table found")
