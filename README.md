# email_list_generator_uh
This script takes the classes from UH Manoa's spring 2019 class list and gathers all the course information, including the instructor, instructor's email address, location, and more. It then takes this course information and saves it as a spreadsheet. 

To run the script, simply go onto terminal to location of where script is located and run
```bash
python uh_s19_email_list_generator.py
```
It will then prompt you to enter the department abbreviation. After entering the department, enter the course numbers you are interested in. Hit enter without entering anything to move on.

## Example
```bash
Enter the department abbrviation: (ex: BUS, PHYS)
PHYS


Please wait while the UH class database is being accessed ...


Enter in a course number, to specify multiple course numbers use a '-' to specify the range ex: 100-396

100-120
151

Course CRN numbers found: 
100  :  81307
151  :  81310


Do you want to add more classes from another department? (y/n)
n

Gathering infromation on classes given, please wait ...

Finished. Data saved to output.xlsx

```
