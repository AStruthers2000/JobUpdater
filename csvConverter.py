import csv,datetime

def writeFirstRow(row):
    row = row
    new_row = ["Employer", "Contact", "City", "State", "Resume Submission Method", "Approved", "Posted in WCN", "How to apply", "Position Type", "On Campus"]
    row += new_row
    return row 

def modRow(row):
    row = row

    if "how to apply" in row[5].lower():
        row[5] = row[5].split("How To Apply")
        #print(row[5])
        row[5] = row[5][0]
        if row[5] == " ":
            row[5] = "To view the details of this job posting, please see the original posting on the HR website at the link provided."
    row[5] += "\n\nHow To Apply:\n\tClick the grey Apply button at the top of the page and follow the links in the popup tab.\n\t\tPlease note, if the grey box is not clickable, you may need to upload a resume into the system first."
    
    location = ""
    locations = ["Lynnwood", "des Moines", "Wenatche", "Pierce", "Yakima", "moses lake"]
    for loc in locations:
        if loc.lower() in row[1].lower():
            if not location == "":
                location += ","
            location += loc
    if location == "":
        location = "Ellensburg"

    now = datetime.datetime.now()
    curDate = now.strftime("%m/%d/%Y")

    howToApply = "This is a CWU On-Campus job. All application for these types of positions must be processed through the CWU HR website. You may apply by using thedirect jobpost link below or by using the general HR link below and searching for this post by title in their system.\n\nJob Posting Direct Link: " + row[6] + "\n\n\tGeneral HR Website: https://careers.cwu.edu"

    typeOfJob = "Student Employment On-Campus Jobs"
    if "work study" in row[1].lower() or "work study" in row[5].lower():
        typeOfJob = "Work Study"

    new_row = ["CWU On-Campus Employment", "Career Services Representative", location, "WA", "Other (enter below)", "Yes", curDate, howToApply, typeOfJob, "Yes"]
    row += new_row
    return row

firstRow = True
with open("CS_LOAD.csv", newline='') as infile: #opens file
    with open("Converted_File.csv", 'w', newline='') as outfile: #creates output file 
        inReader = csv.reader(infile) #makes csvreader of file
        outWriter = csv.writer(outfile) #makes writer of outfile
        for row in inReader: #every single row in FakeData1.csv
            if firstRow:
                new_row = writeFirstRow(row)
                firstRow = False
            else:
                new_row = modRow(row)
            outWriter.writerow(new_row) #writing to outfile
