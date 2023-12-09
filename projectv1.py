import streamlit as st

def grade(marks):
    if marks == 100:
        return 10
    elif marks // 10 > 4:
        return (marks // 10) + 1
    else:
        return 0

def get_subject_data(semester_index, subject_index):
    name = st.text_input(f"Enter the name of subject {subject_index} for Semester {semester_index}: ")
    credits = st.number_input("Enter the credits of the subject: ", min_value=0, step=1, value=1, key=f"credits_{semester_index}_{subject_index}")
    marks_input = st.text_input("Enter marks (comma-separated): ", key=f"marks_{semester_index}_{subject_index}")

    if marks_input and ',' in marks_input:
        um = list(map(int, marks_input.split(",")))
        marks = (um[0] / 2) + (um[1] / 2) + (um[2] / 2) + um[3]
        st.write(f"Marks = {tuple(um)}")
        st.write(f"Calculated Marks: {marks}")
        subject_grade = grade(marks)
        st.write(f"Grade in {name} is {subject_grade}")
        return credits, subject_grade
    else:
        st.warning("Please enter valid marks (comma-separated)")
        return 0, 0

def calculate_sgpa(subjects_data):
    sum_credits = sum(credits for credits, _ in subjects_data)
    
    if sum_credits > 0:
        sgpa = sum(grade * credits for credits, grade in subjects_data) / sum_credits
        return sgpa
    else:
        st.warning("Total credits for the semester should be greater than zero.")
        return 0

def calculate_cgpa(semester_data):
    total_semesters = len(semester_data)
    cumulative_sgpa = sum(semester_sgpa for semester_sgpa, _ in semester_data)
    
    if total_semesters > 0:
        cgpa = cumulative_sgpa / total_semesters
        return cgpa
    else:
        st.warning("Number of semesters should be greater than zero.")
        return 0

def input_semester(semester_index):
    st.subheader(f"Semester {semester_index}:")
    subjects_data = [get_subject_data(semester_index, i) for i in range(1, 7)]
    sgpa_value = calculate_sgpa(subjects_data)
    st.write(f"SGPA = {sgpa_value:.2f}")
    return sgpa_value, subjects_data

def main():
    st.title("PESU GPA Calculator")
    st.write("This is a simple GPA calculator designed for PESU students, by a PESU student.")
    st.write("Note: Enter marks in the following order: ISA1, ISA2, ESA, Project Marks. ISA marks are scaled to 40, Project marks are scaled to 10 and ESA marks are scaled to 100.")
    st.subheader("Number of Semesters")
    n = st.number_input("Enter the number of semesters completed: ", min_value=1, step=1, value=1, key="num_semesters")
    semester_data = [input_semester(i) for i in range(1, int(n) + 1)]
    final_cgpa = calculate_cgpa(semester_data)
    st.write(f"Your CGPA is {final_cgpa:.2f}")

if __name__ == "__main__":
    main()
