import streamlit as st
import pandas as pd

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
    if semester_index >= 3:
        num_subjects = 5 
    else:
        num_subjects = 6
    subjects_data = [get_subject_data(semester_index, i) for i in range(1, num_subjects + 1)]
    sgpa_value = calculate_sgpa(subjects_data)
    st.write(f"SGPA = {sgpa_value:.2f}")
    return sgpa_value, subjects_data

def calculate_required_sgpa(current_cgpa, target_cgpa, completed_semesters):
    if completed_semesters == 0:
        return target_cgpa
    else:
        required_sgpa = (target_cgpa * (completed_semesters + 1) - current_cgpa * completed_semesters) / 1
        return required_sgpa

def main():
    st.title("GPA Calculator")
    st.write("This is a simple GPA calculator for PES University students.")
    st.write("Besides the fact that we are students of PES University, we have no other sort of formal affiliation with the management of the university. Thus, the calculation methods used in this might not reflect PESU's actual calculation methods. This is just a fun CS semester 1 mini project :D")
    # Input for the semesters
    n = st.number_input("Enter the number of semesters completed: ", min_value=1, step=1, value=1, key="num_semesters")
    semester_data = [input_semester(i) for i in range(1, int(n) + 1)]
    final_cgpa = calculate_cgpa(semester_data)
    st.success(f"Your CGPA is {final_cgpa:.2f}")

    # Visualization
    df_sgpa = pd.DataFrame({
        'Semester': list(range(1, int(n) + 1)),
        'SGPA': [sgpa for sgpa, _ in semester_data]
    })

    df_cgpa = pd.DataFrame({
        'Semester': list(range(1, int(n) + 1)),
        'CGPA': [calculate_cgpa(semester_data[:i + 1]) for i in range(int(n))]
    })

    # Line chart for SGPA
    st.subheader("SGPA Over Semesters")
    st.line_chart(df_sgpa.set_index('Semester'))

    # Line chart for CGPA
    st.subheader("CGPA Over Semesters")
    st.line_chart(df_cgpa.set_index('Semester'))

    # Section for calculating required SGPA for the next semester
    st.header("Target CGPA Calculator")
    completed_semesters = st.number_input("Number of semesters completed: ", min_value=0, step=1, value=1, key="completed_semesters")
    current_cgpa = st.number_input("Current CGPA: ", min_value=0.0, value=final_cgpa, key="current_cgpa")
    target_cgpa = st.number_input("Target CGPA for the next semester: ", min_value=0.0, key="target_cgpa")

    if st.button("Calculate Required SGPA"):
        required_sgpa = calculate_required_sgpa(current_cgpa, target_cgpa, completed_semesters)
        if required_sgpa > 10:
            st.warning("Oops! You need a very high SGPA to achieve your target CGPA.")
        else:
            st.success(f"You need an SGPA of {required_sgpa:.2f} in the next semester to achieve your target CGPA.")

if __name__ == "__main__":
    main()
