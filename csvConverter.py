import csv,datetime
from datetime import datetime, timedelta


def getListOfID(filename):
    ID = []
    with open(filename, "r", encoding="latin1") as file:
        reader = csv.reader(file) #makes csvreader of file
        for row in reader:
            if not row[0] == "JOB_ID":
                ID += [row[0]]
    return ID


def getExpiredID(old_list, new_list):
    expiredID = []
    print(old_list)
    print("*"*10)
    print(new_list)
    for ID in old_list:
        if ID not in new_list:
            print(str(ID) + " exists in old, but not in new")
            expiredID += [ID]
    print("*"*10)
    print(expiredID)
    return expiredID


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

    now = datetime.now()
    curDate = now.strftime("%m/%d/%Y")

    howToApply = "This is a CWU On-Campus job. All application for these types of positions must be processed through the CWU HR website. You may apply by using thedirect jobpost link below or by using the general HR link below and searching for this post by title in their system.\n\nJob Posting Direct Link: " + row[6] + "\n\n\tGeneral HR Website: https://careers.cwu.edu"

    typeOfJob = "Student Employment On-Campus Jobs"
    if "work study" in row[1].lower() or "work study" in row[5].lower():
        typeOfJob = "Work Study"

    new_row = ["CWU On-Campus Employment", "Career Services Representative", location, "WA", "Other (enter below)", "Yes", curDate, howToApply, typeOfJob, "Yes"]
    row += new_row
    return row


def deleteExpired(filename):
    # section to delete all old expired jobs from outdated.csv
    deleted_count = 0

    oldfile = open(filename, "r", encoding="latin1")
    oldgoodfile = open("new_" + filename, "w", newline='', encoding='latin1')

    oldfile_reader = csv.reader(oldfile)
    oldgoodfile_writer = csv.writer(oldgoodfile)
    for row in oldfile_reader:
        if not row[3] == " CLOSE_DATE":
            try:
                year = int(row[3].split("/")[2])
                if year < 2000:
                    year += 2000
                oldfile_closedate = datetime(year, int(row[3].split("/")[0]), int(row[3].split("/")[1]))
                present = datetime.now()
                
                if oldfile_closedate > present:
                    oldgoodfile_writer.writerow(row)
                else:
                    deleted_count += 1
            except IndexError:
                print(row[3])

    print("Found: " + str(deleted_count) + " already expired jobs in " + filename)                
    oldgoodfile.close()


def generateExpiredIDList():
    # section to generate expired ID list
    oldgood_id_list = getListOfID("new_outdated.csv")
    new_id_list = getListOfID("new_CS_LOAD.csv")
    expiredID = getExpiredID(oldgood_id_list, new_id_list)
    return expiredID


def makeExpired(oldID, newID):
    duplicate_count = 0
    # section to modify expired dates in new_outdated.csv and append them to goodfile
    goodfile = open("Updated_Job_List.csv", "a", newline='', encoding='latin1')
    goodfile_writer = csv.writer(goodfile)
    
    oldgoodfile = open("new_outdated.csv", "r", encoding='latin1')
    oldgood_reader = csv.reader(oldgoodfile)
    
    for row in oldgood_reader:
        ID = row[0]
        if ID in oldID:
            modtime = datetime.date(datetime.now() - timedelta(days=1))
            row[3] = str(modtime.month) + "/" + str(modtime.day) + "/" + str(modtime.year)

        if not ID in newID:
            goodfile_writer.writerow(row)
        else:
            duplicate_count += 1
            #print("Duplicate, wrote new")
    print(duplicate_count)
            
    goodfile.close()


def writeCurrent():
    currentID = []
    currentfile = open("new_CS_LOAD.csv", "r", encoding='latin1')
    goodfile = open("Updated_Job_List.csv", "w", newline='', encoding='latin1')

    currentfile_reader = csv.reader(currentfile)
    goodfile_writer = csv.writer(goodfile)
    header = ["JOB_ID", "TITLE", "OPEN_DATE", "CLOSE_DATE", "POST_SEQ", "DESCRIPTION", "URL", "Employer", "Contact", "City", "State", "Resume Submission Method", "Approved", "Posted in WCN", "How to Apply", "Position Type",	"On Campus"]
    goodfile_writer.writerow(header)

    for row in currentfile_reader:
        new_row = modRow(row)
        currentID += [row[0]]
        goodfile_writer.writerow(new_row)

    currentfile.close()
    goodfile.close()

    return currentID
    

def main():
    """old_id_list = getListOfID("outdated.csv")
    new_id_list = getListOfID("CS_LOAD.csv")
    expiredID = getExpiredID(old_id_list, new_id_list)
    print("====="*5)
    
    firstRow = True
    with open("CS_LOAD.csv", newline='', encoding='latin1') as infile: #opens file
        with open("Converted_File.csv", 'w', newline='', encoding='latin1') as outfile: #creates output file
            inReader = csv.reader(infile) #makes csvreader of file
            outWriter = csv.writer(outfile) #makes writer of outfile
            for row in inReader: #every single row in FakeData1.csv
                if row[0] in expiredID:
                    print(str(row[0]) + " is expired")
                    
                if firstRow:
                    new_row = writeFirstRow(row)
                    firstRow = False
                else:
                    new_row = modRow(row)
                outWriter.writerow(new_row) #writing to outfile"""

    deleteExpired("CS_LOAD.csv")
    currentID = writeCurrent()

    deleteExpired("outdated.csv")

    expiredID = generateExpiredIDList()

    makeExpired(expiredID, currentID)


    #oldgoodfile = open("new_outdated.csv", "r", encoding='latin1')
    #oldgoodfile_reader = csv.reader(oldgoodfile)

    #for row in oldgoodfile_reader:
        


if __name__ == "__main__":
    main()
