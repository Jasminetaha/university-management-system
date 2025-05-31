import pandas as pd
#This imports the pandas library and ali it pd
#pandas is used to store and manipulate datasets


read_university_list= pd.read_csv('university_list.csv')

def student_add(df,name,course): # function to add a new sudent to course
    new_id= df['StudentId'].max()+1 #creates a new student id by incrementing the maximum existing student id by 1
#checks if the student is already in the specified course
    if (course in df['Course'].values) and (name in df['Name'].values):
        print("Student already in course")
    elif course in df['Course'].unique(): #if yes, add student to data frame
        new_student = pd.DataFrame({'Course':[course],'Name':[name],'StudentId':[new_id]})
        df= pd.concat([df, new_student],ignore_index=True) #combines the two data frames along rows
    else:
        print("Course does not exist")
    return df

def course_remove(df,name,course):
    df = df[(df['Name']!=name) and (df['Course']!=course)] #this filters the pandas DataFrame
    return df

def enter_grades(df,name,course,midterm_grade,final_grade):
    if (course in df['Course'].values) and (name in df['Name'].values):
        df.loc[(df['Course'] ==course) & (df['Name']==name),'Midterm Grade']=midterm_grade
        df.loc[(df['Course']==course) & (df['Name']== name),'Final Grade']=final_grade #updates thhe grades at a location base on the row/ column indexer
    else:
        return ValueError("Student or Course not found")
    return df

def update_grades(df,name,course,midterm_grade=None,final_grade=None):
    #check if the specified course and student exist in the DataFrame
    if (course in df['Course'].values) and (name in df['Name'].values):
        #update the 'Midterm Grade' if the midterm_grade parameter is provided
        if midterm_grade is not None:
            df.loc[(df['Course']==course) & (df['Name']==name),'Midterm Grade']=midterm_grade
            # update the final if the final grade parameter is provide
        if final_grade is not None:
            df.loc[(df['Course']== course) & (df['Name']== name),'Final Grade']=final_grade
    else:
        # if the student or course is not found, return  ValueError
        raise ValueError("Student or Course not found")
    return df
#arguement of the correct datatype but the value of the arguement

# function to calculate total gpa
def calculate_total_gpa(df,student_id):
    student_data = df[df['StudentId'] == student_id]
    if student_data.empty:
        return ValueError("Student not found")

    courses  = student_data['Course']
    total_weighted_gpa= 0.0
    total_credits = 0

    for course in courses:
        midterm_grade  = student_data[student_data['Course'] == course]['Midterm Grade'].values[0]
        final_grade    = student_data[student_data['Course'] == course]['Final Grade'].values[0]

        credits   = 3  # Adjust the credit value according to the course credit system

        final_course_grade = (midterm_grade + final_grade) / 2 * 100

        final_course_gpa = None
        gpa_scale = {
            (100, 93): 4.0,
            (92, 90): 3.7,
            (89, 87): 3.3,
            (86, 83): 3.0,
            (82, 80): 2.7,
            (79, 77): 2.3,
            (76, 73): 2.0,
            (72, 70): 1.7,
            (69, 67): 1.3,
            (66, 65): 1.0,
            (64, 0): 0
        }

        for (upper_bound, lower_bound), gpa in gpa_scale.items():
            if lower_bound <= final_course_grade <= upper_bound:
                final_course_gpa = gpa
                break

        if final_course_gpa is None:
            return ValueError("Invalid final course grade range")

        weighted_gpa  = final_course_gpa * credits
        total_weighted_gpa += weighted_gpa
        total_credits += credits

    return total_weighted_gpa / total_credits

#function to search student
def search_student(df,key,NM='Name'):
    if NM not in ['Name', 'Id']:
        return ValueError("Invalid search criteria. Use 'Name' or 'Id'.")

    if NM == 'Name':
        result = df[df['Name'] == key]
    else:
        result = df[df['Id'] == key]

    if result.empty:
        print(f"No student found with {NM} '{key}'")
    else:
        print(result)

#testing examples
read_university_list = student_add(read_university_list,"Sahar Taha","Calculus")
#print(read_university_list[read_university_list['Name']=='Sahar Taha'])

read_university_list = student_add(read_university_list,"Sahar Taha","Calculus")
read_university_list = student_add(read_university_list,"Sahar Taha","History")
#read_university_list=course_remove(read_university_list,"Sahar Taha","Calculus")

read_university_list = student_add(read_university_list,"Sahar Taha","Calculus")
read_university_list = enter_grades(read_university_list,"Sahar Taha","Calculus",midterm_grade=0.90,final_grade=0.85)
read_university_list = update_grades(read_university_list,"Sahar Taha","Calculus",midterm_grade=0.95)

print(read_university_list[read_university_list['Name']=='Sahar Taha'])
#print(read_university_list.head())
print(calculate_total_gpa(read_university_list,98))
print(read_university_list[read_university_list['StudentId']=='98'])
print(search_student(read_university_list,'Sahar Taha',NM='Name'))
print(f"total gpa is {calculate_total_gpa()}")