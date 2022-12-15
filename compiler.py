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

# --- take queries
    def queries(self):

        while True:
            try:
                query = input(f"{' ':<2}> ").strip()
                self.operate(query)
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
            This commands opens previously created database.
            After opening the database
            further operations can be performed on it.
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
    def sub_operate(self, db_data, dbname):
        while True:
            try:
                query = input(f"{' ':<2}>> ").strip()
                cmd_lis = query.split()
                if cmd_lis[0].lower() == "create" and cmd_lis[1].lower() == "table":
                    self.table(cmd_lis, db_data, dbname)
                if cmd_lis[0].lower() == "insert" and cmd_lis[1].lower() == "into":
                    self.insert(cmd_lis, db_data, dbname)
                if cmd_lis[0].lower() == "view" and cmd_lis[1].lower() == "table":
                    self.view(cmd_lis, db_data, dbname)
            except KeyboardInterrupt:
                print("\n")
                break

    # --- methods to perform DML commands ---
    # # Create Table

    def table(self, cmd_lis, db_data, dbname):
        # --- Create Table
        try:
            # empty table
            tbname = cmd_lis[2].strip()
            db_data[tbname] = {}

            # table columns
            colname = cmd_lis[3].replace("(", "").strip()
            colname = colname.replace(")", "")
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
        syntax:
            > INSERT INTO {table_name} ({columns}) ({values})
        '''
        try:
            # table
            tbname = cmd_lis[2]
            # table columns
            colname = cmd_lis[3].replace("(", "")
            colname = colname.replace(")", "")
            colname = tuple(map(str, colname.split(',')))
            # values
            values = cmd_lis[4].replace("(", "")
            values = values.replace(")", "")
            values = tuple(map(str, values.split(',')))
            for i, _ in enumerate(colname):
                db_data[tbname][_].append(values[i].replace('"', ''))
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
        # -- View entire table upto 20 records
        try:
            # table
            tbname = cmd_lis[2]
            if tbname not in db_data:
                raise KeyError
            print(f"\n{' ':<2}TABLE: {tbname}")
            print(tabulate(db_data[tbname], headers="keys", tablefmt="grid"), "\n")

        except IndexError:
            print(f"{' ':<2}: Invalid Command")

        except KeyError:
            print(f"{' ':<2}: No {tbname} table found")
