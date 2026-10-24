import sqlite3
import pandas as pd
import numpy as np

# 1. Pipeline extraction from the active local database
conn = sqlite3.connect('campus_placement.db')

query_students = "SELECT student_id, department, eligible FROM students"
query_placements = "SELECT student_id, package, status FROM placements WHERE status = 'Accepted'"
query_skills = """
    SELECT s.skill_name 
    FROM student_skills ss
    JOIN skills s ON ss.skill_id = s.skill_id
    JOIN placements p ON ss.student_id = p.student_id
    WHERE p.status = 'Accepted'
"""

df_students = pd.read_sql_query(query_students, conn)
df_placements = pd.read_sql_query(query_placements, conn)
df_skills = pd.read_sql_query(query_skills, conn)
conn.close()

# 2. Re-compile calculations
eligible_counts = df_students[df_students['eligible'] == 1].groupby('department').size().to_frame('Eligible Cohort')
placed_counts = df_placements.groupby('student_id').first().reset_index()
placed_counts = placed_counts.merge(df_students, on='student_id').groupby('department').size().to_frame('Placed Cohort')
packages = df_placements.merge(df_students, on='student_id').groupby('department')['package'].agg(
    Mean_Package_LPA=np.mean,
    Median_Package_LPA=np.median
)

# Compile calculations into structured data sheets
report_df = eligible_counts.join(placed_counts).fillna(0)
report_df['Placement Rate (%)'] = round((report_df['Placed Cohort'] / report_df['Eligible Cohort']) * 100, 2)
report_df = report_df.join(packages).round(2).reset_index()

skill_demand_df = df_skills['skill_name'].value_counts().to_frame('Total Placement Offers Secured').reset_index()
skill_demand_df.rename(columns={'index': 'Core Technical Skill'}, inplace=True)

# 3. Export to structured Multi-Sheet Excel Workbook
excel_file = 'Campus_Placement_Analytics_Report.xlsx'

with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    report_df.to_excel(writer, sheet_name='Department Summary', index=False)
    skill_demand_df.to_excel(writer, sheet_name='Skill Matrix Trends', index=False)

print("="*60)
print(f"✨ SUCCESS: Spreadsheet report compiled and saved successfully!")
print(f"📂 Output File Location: '{excel_file}'")
print("="*60)
