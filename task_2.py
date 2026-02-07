import csv
import statistics
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# -----------------------------
# Step 1: Read Data from File
# -----------------------------
names = []
scores = []

with open("data.csv", "r") as file:
    reader = csv.DictReader(file)

    # Clean headers: strip spaces + lowercase
    reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]

    for row in reader:
        row = {k.strip().lower(): v for k, v in row.items()}
        names.append(row["name"])
        scores.append(int(row["score"]))


# -----------------------------
# Step 2: Analyze Data
# -----------------------------
total_students = len(scores)
average_score = statistics.mean(scores)
highest_score = max(scores)
lowest_score = min(scores)

# -----------------------------
# Step 3: Create PDF Report
# -----------------------------
pdf = SimpleDocTemplate(
    "Automated_Report.pdf",
    pagesize=A4
)

styles = getSampleStyleSheet()
content = []

# Title
content.append(Paragraph("<b>AUTOMATED REPORT GENERATION</b>", styles["Title"]))
content.append(Paragraph("Student Performance Analysis", styles["Heading2"]))

# Summary Section
summary_text = f"""
Total Students: {total_students}<br/>
Average Score: {average_score:.2f}<br/>
Highest Score: {highest_score}<br/>
Lowest Score: {lowest_score}
"""
content.append(Paragraph("<b>Summary</b>", styles["Heading3"]))
content.append(Paragraph(summary_text, styles["Normal"]))

# -----------------------------
# Table Data
# -----------------------------
table_data = [["Name", "Score"]]

for i in range(total_students):
    table_data.append([names[i], scores[i]])

table = Table(table_data)

table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
]))

content.append(Paragraph("<b>Detailed Scores</b>", styles["Heading3"]))
content.append(table)

# Build PDF
pdf.build(content)

print("PDF Report Generated Successfully!")
