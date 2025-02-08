# Tacnique
Tacnique evaluation assignment

1. Create SQLite database by name 'tacnique.db'
	c:\sqlite\sqlite3 tacnique.db

2. Run sqlite3 on command line and create Employees & Departments tables in tacnique.db
	create table Employees (id INTEGER PRIMARY KEY, name TEXT NOT NULL, department TEXT, salary INTEGER, hire_date);
	create table Departments (id INTEGER PRIMARY KEY, name TEXT NOT NULL, manager TEXT);

3. Insert data in the tables
	insert into Employees values(1, 'Alice','Sales',50000,'2021-01-15');
	insert into Employees values(2, 'Bob','Engineering',70000,'2020-06-10');	
	insert into Employees values(3, 'Charlie','Marketing',60000,'2022-03-20');
	insert into Employees values(4, 'David','Sales',40000,'2021-05-15');
	insert into Employees values(5, 'Edwards','Sales',30000,'2024-01-01');
	insert into Employees values(6, 'Fiona','Marketing',50000,'2022-05-15');

	insert into Departments values(1, 'Sales','Alice');
	insert into Departments values(2, 'Engineering','Bob');
	insert into Departments values(3, 'Marketing','Charlie');

4. Python script chatAssist.py
	Use 'gpt-3.5-turbo' as LLM
	Used gradio to create simple chatbot interface
	Create 'system' role instructing LLM to act as middleperson between user & database and giving details of SQLite tables
	For each user prompt:
		create 'assistant' role instructing LLM to create a SQL query based on user prompt
		Send user prompt to LLM
		Check returned response if it is a valid SQL
		If valid SQL then invoke SQLite and send the query
		If query returned rows then format the rows and print in chatbot
		If no rows or not a valid SQL then inform user as such

