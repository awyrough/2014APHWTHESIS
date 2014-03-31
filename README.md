2014APHWTHESIS
==============

A.P. Hill Wyrough's Thesis Project Source Code: Creating Trip Files for the Entire United States

This README, and Repository '2014APHWTHESIS', is submitted in partial fulfillment of the requirements for the degree of Bachelor 
of Science in Engineering, for the Department of Operations Research and Financial Engineering at Princeton University

June 2014

Advisor: Professor Alain L. Kornhauser *76

I hereby declare that I am the sole author of this thesis. /s/ APHW

I authorize Princeton University to lend this thesis to other institutions or individuals for the purpose of scholarly research. /s/ APHW

I further authorize Princeton University to reproduce this thesis by photocopying or by other means, in total or in part, at the
request of other institutions or individuals for the purpose of scholarly research.

================

README

Requirements: 

Python v3.3
64 Bit Computer (8GB RAM, 2 GHz)
Eclipse IDE
Numpy Library for Python 3.3

Name: NationalTripSynthesizer
Modules:
  - Module1
    - Module1.py
    - Module1runner.py
  - Module2
    - countyAdjacencyReader.py
    - industryReader.py
    - workPlaceHelper.py
    - industryReader.py
    - Data Helpers
      - employeeFileHelper.py
      - zipCodeReader.py
  - Module3
    - countyAdjacencyReader.py
    - schoolCounty.py
    - Module3.py

Analysis:
  - fileRepair.py

Synthesizer Pattern:

Census Data -> module1.py -> module1ouptut
module1output -> module2.py + employment data -> module2output
module2output -> module3.py + enrollment data -> module3output
module3output -> module4.py + tour type data -> module4output
module5output -> module5.py + patronage data -> module5output
module5output -> module6.py + time distributions -> module6output

Data Repository Needed and Structure:

Data Repository:
  MODULE1 Census Data:
    - DemographicQueries
    - GroupQuarterQueries
    - FamilyQueries
    - IncomeQueries
  MODULE2 Employment Data:
    - Employment
      - CountyEmployeeFiles
        - State Folders With EmpPat Files By County
      - Employee Patronage Data
        - Raw State Data
      - ZipCodes
        - Zip Code To County Library
      - SexByIndustryByCounty_MOD.csv
    - WorkFlow
      - J2W.csv
      - allCounties.csv
      - county_adjacency.csv
  MODULE3 School Data:
    - School Database
      - CountyPrivateSchools
        - Private Schools by Type by County (Elem, Mid, High folders)
      - CountyPublicSchools
        - Public Schools by Type by County (Elem, Mid, High Folders)
      - PostSecSchoolsByCounty
      - statenrollmentindegrees.csv
      - statehighelemmidenrollment.csv
      

MODULE1 Documentation:

The goal of Module1.py is to iterate over each Census block and recreate it. Module1.py runs linearly with Census block counts for each state, but within each Census block, it runs linearly with the population contained. 

Run Time: All states can be processed within 6 - 8 hours

MODULE2 Documentation

Run Time: EXTREMELY INTENSIVE

An examination of a run time profiler indicates one thing: the volume of employers in a particular county is the time constraint. No single function call or action within the code takes time. For example, simple lat-lon distance calculations take <0.00001 seconds to complete, but billions are done for a moderate sized state. For every worker, a calculation is done to his or her home to every possible place of work within an industry. New York took one day and 15 hours, Calfornia and Texas took over two days. Most states run from 1 - 10 hours depending on size. States with large concentrations of populations, and/or not a lot of counties take a long time.  
