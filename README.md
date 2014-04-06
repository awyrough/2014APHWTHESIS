2014APHWTHESIS
==============

A.P. Hill Wyrough's Thesis Project Source Code: Creating Trip Files for the Entire United States

This README, and Repository '2014APHWTHESIS', is submitted in partial fulfillment of the requirements for the degree of Bachelor of Science in Engineering, for the Department of Operations Research and Financial Engineering at Princeton University

June 2014

Advisor: Professor Alain L. Kornhauser *76

I hereby declare that I am the sole author of this thesis. /s/ APHW

I authorize Princeton University to lend this thesis to other institutions or individuals for the purpose of scholarly research. /s/ APHW

I further authorize Princeton University to reproduce this thesis by photocopying or by other means, in total or in part, at the request of other institutions or individuals for the purpose of scholarly research.


Project Description: 

Globally, every day, nearly one billion personal automobiles and other motorized vehicles travel millions of miles of roadway. The world's consumers have spent trillions of dollars on these vehicles, which rely in most respects on automotive systems and designs developed 50-75 years ago. The indirect costs of traffic congestion, pollution and accidents add tens of billions of additional expense to the bill for personal transportation freedom. As with many other industries, technologies are emerging to revolutionize old models and potentially deliver greater individual and collective good at lower cost. These novel technological systems focus on implementing autonomously driven vehicles to serve personal transportation demand by replacing the personal automobile with fleets of self-driving cars. One of the more vexing challenges of self-driving cars is not the technological element, but the determination of the potential personal demand and patterns of use.
    
To that end, modeling existing travel behavior is fundamental in creating and analyzing such systems. This thesis develops an existing disaggregate travel demand model, constrained for use within the state of New Jersey, into a nation-wide daily transportation demand model. Data drawn from the U.S. 2010 Census, as well as other sources, are used to simulate a population with specific personal attributes and the range of trips each person will take throughout a day. With precise spatial and temporal attributes that mimic actual personal travel behavior, these trips comprise a data set ready for use in the analysis of the efficacy of novel transportation systems. Upon knowing where everyone wants to go, from where, and when, one can begin to dream up systems to serve this demand using autonomously vehicles. Particularly, this data set is designed for use in gaining insight on a national system of autonomous taxis that could (a) match the comfort and convenience of personal cars, (b) exceed the accessibility of mass transit, and (c) deliver wide-ranging benefits such as alleviated congestion, reduced pollution, and increased vehicle safety.

What It Does:

It accepts an incredible amount of data to simulate the 300 million residents of the United States and the approximately 1.1 Billion personal, casual (non-commercial) trips they take on an average work day. It builds a synthetic population that matches the real population and sends each worker to a specific place of work, each student to a specific school, and everyone on all the errands and trips throughout a typical day. 

For the written Thesis report documenting and analyzing this project inquire at alexander.hill.wyrough@gmail.com or with Princeton University, if it is for academic purposes. 
For data requests inquire at alexander.hill.wyrough@gmail.com or awyrough@princeton.edu

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
