import sqlite3

conn = sqlite3.connect('campus_placement.db')
cursor = conn.cursor()

# Force drop existing tables to align perfectly with the target blueprint schema
cursor.executescript('''
DROP TABLE IF EXISTS placements;
DROP TABLE IF EXISTS student_skills;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    placement_eligible INTEGER DEFAULT 1
);

CREATE TABLE skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT UNIQUE NOT NULL
);

CREATE TABLE student_skills (
    student_id INTEGER,
    skill_id INTEGER,
    PRIMARY KEY (student_id, skill_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
);

CREATE TABLE placements (
    placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    package REAL NOT NULL, -- Units measured explicitly in LPA
    status TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);
''')

# Seed Core Skills exactly as defined in panel 2
skills = ['Python', 'SQL', 'Java', 'Machine Learning', 'Web Development', 'Data Analysis', 'Communication']
for s in skills:
    cursor.execute("INSERT INTO skills (skill_name) VALUES (?)", (s,))

# Seed 10 sample records to yield the identical calculations in console dashboard outputs
students_data = [
    ('STU001', 'Aarav Sharma', 'CSE', 1),
    ('STU002', 'Priya Singh', 'ECE', 1),
    ('STU003', 'Rohan Verma', 'CSE', 1),
    ('STU004', 'Neha Gupta', 'IT', 1),
    ('STU005', 'Karan Mehta', 'ECE', 1),
    ('STU006', 'Amit Kumar', 'CSE', 1),
    ('STU007', 'Sonia Rai', 'ME', 1),
    ('STU008', 'Rahul Jain', 'IT', 1),
    ('STU009', 'Vijay Dev', 'ME', 0), # Not Eligible denominator base boundary
    ('STU010', 'Riya Sen', 'ECE', 0)   # Not Eligible denominator base boundary
]
for roll, name, dept, elig in students_data:
    cursor.execute("INSERT INTO students (roll_no, name, department, placement_eligible) VALUES (?, ?, ?, ?)", (roll, name, dept, elig))

# Distribute technical capabilities for skill frequencies matrices
skill_mappings = {
    1: [1, 2, 3, 5, 7],    # Aarav Sharma: Python, SQL, Java, Web Dev, Communication
    2: [1, 2, 3, 5, 7],    # Priya Singh: Python, SQL, Java, Web Dev, Communication
    3: [1, 2, 3, 4, 6],    # Rohan Verma: Python, SQL, Java, Machine Learning, Data Analysis
    4: [1, 2, 5],          # Neha Gupta: Python, SQL, Web Dev
    5: [1, 2, 3, 7],       # Karan Mehta: Python, SQL, Java, Communication
    6: [1, 2, 5, 6],       # Amit Kumar: Python, SQL, Web Dev, Data Analysis
    7: [1, 3, 7],          # Sonia Rai: Python, Java, Communication
    8: [1, 2, 4],          # Rahul Jain: Python, SQL, Machine Learning
    9: [1, 4, 6],          # Vijay Dev: Python, Machine Learning, Data Analysis
    10: [1]                # Riya Sen: Python
}

for s_id, sk_list in skill_mappings.items():
    for sk in sk_list:
        cursor.execute("INSERT INTO student_skills VALUES (?, ?)", (s_id, sk))

# Register company corporate volumes matching placement values
placements_data = [
    (1, 'TCS', 'Software Engineer', 7.5, 'Accepted'),
    (3, 'TCS', 'Software Engineer', 7.5, 'Accepted'),
    (2, 'Infosys', 'Systems Engineer', 6.0, 'Accepted'),
    (5, 'Infosys', 'Systems Engineer', 6.0, 'Accepted'),
    (4, 'Wipro', 'Cloud Engineer', 5.5, 'Accepted'),
    (6, 'Accenture', 'Data Analyst', 4.0, 'Accepted'),
    (7, 'Capgemini', 'Analyst', 4.8, 'Accepted')
]
for s_id, comp, role, pkg, stat in placements_data:
    cursor.execute("INSERT INTO placements (student_id, company, role, package, status) VALUES (?, ?, ?, ?, ?)", (s_id, comp, role, pkg, stat))

conn.commit()
conn.close()
print("🎉 Success: 'setup_data.py' updated and database successfully built!")
