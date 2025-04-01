import openpyxl
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import PieChart, Reference

wb = Workbook()
ws_tasks = wb.active
ws_tasks.title = "Tasks"

headers = ["Task", "Subtasks", "Timeline", "Status", "Notes"]
ws_tasks.append(headers)

tasks_data = [
    ["Cloud Stacks", "2 initial stacks; 1 monthly ongoing", "Initial, Monthly", "", ""],
    ["Google Stacks", "4 per month", "Monthly", "", ""],
    ["CTR - Branded Keywords", "Set up tracking for 10 keywords", "Months 1-3", "", "Record monthly CTR data"],
    ["CTR - Low-Competition Keywords", "Identify & track 10 keywords", "Monthly", "", ""],
    ["CTR - High-Volume Keywords", "Month 1: 3 keywords; add 5 monthly up to 30", "Month 1 onward", "", ""],
    ["Backlink Building", "Research, outreach, follow-up", "Ongoing", "", ""],
    ["Enhanced Schema", "Audit, plan, implement, test", "One-Time Project", "", ""]
]
for row in tasks_data:
    ws_tasks.append(row)

ws_lists = wb.create_sheet(title="Lists")
ws_lists["A1"] = "Not Started"
ws_lists["A2"] = "In Progress"
ws_lists["A3"] = "Completed"

dv = DataValidation(type="list", formula1="=Lists!$A$1:$A$3", allow_blank=True)
dv.error = 'Please select a valid status'
dv.errorTitle = 'Invalid Status'
ws_tasks.add_data_validation(dv)
dv.add("D2:D8")

ws_summary = wb.create_sheet(title="Summary")
ws_summary["A1"] = "Metric"
ws_summary["B1"] = "Value"
ws_summary["A2"] = "Total Tasks"
ws_summary["B2"] = "=COUNTA(Tasks!A2:A8)"
ws_summary["A3"] = "Completed Tasks"
ws_summary["B3"] = '=COUNTIF(Tasks!D2:D8, "Completed")'
ws_summary["A4"] = "Overall Completion (%)"
ws_summary["B4"] = '=IF(B2=0, 0, B3/B2)'
ws_summary["B4"].number_format = "0.00%"

ws_summary["A6"] = "Category"
ws_summary["B6"] = "Count"
ws_summary["A7"] = "Completed"
ws_summary["B7"] = '=COUNTIF(Tasks!D2:D8, "Completed")'
ws_summary["A8"] = "Not Completed"
ws_summary["B8"] = '=COUNTA(Tasks!D2:D8)-COUNTIF(Tasks!D2:D8, "Completed")'

pie = PieChart()
data = Reference(ws_summary, min_col=2, min_row=7, max_row=8)
labels = Reference(ws_summary, min_col=1, min_row=7, max_row=8)
pie.add_data(data, titles_from_data=False)
pie.set_categories(labels)
pie.title = "Project Completion Breakdown"
ws_summary.add_chart(pie, "D6")

output_filename = "ProjectTracker.xlsx"
wb.save(output_filename)
print(f"Excel workbook '{output_filename}' created successfully!")
