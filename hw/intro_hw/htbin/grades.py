#!/usr/bin/env python

def getGrades():
    grades = []
    with open("grades.txt", "r") as grade_file:
        grades = grade_file.readlines()
    response = "<h1>Grades<h1>"
    for line in grades:
        line = line.strip()
        if line.startswith("#"):
            response += "<h2>" + line[1:].strip() + "</h2>"
        elif line != "":
            response += line + "<br>"
    return response

print "Content-type: text/html"
print
print getGrades()

