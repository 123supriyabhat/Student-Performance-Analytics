import streamlit as st
import pandas as pd
st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
    color: #222222;
}

.stApp h1, .stApp h2, .stApp h3 {
    color: #222222 !important;
}

.stApp p, .stApp label, .stApp span {
    color: #333333;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Student Performance Analytics Dashboard")
st.write(
    "An interactive dashboard to analyze student performance, "
    "compare subject-wise marks, and identify academic insights."
)

# Load student data
df = pd.read_csv("student_data.csv")

# Dashboard Filters
st.sidebar.header("⚙️ Dashboard Filters")

selected_student = st.sidebar.selectbox(
    "👤 Select Student",
    df["Student"]
)

subjects = ["Maths", "Science", "English", "Computer"]
# Check missing values
missing_values = df.isnull().sum()

# Count duplicate records
duplicate_count = df.duplicated().sum()

# Remove duplicate records
df = df.drop_duplicates()

# Fill missing marks with subject average
df[subjects] = df[subjects].fillna(df[subjects].mean())

st.header("🧹 Data Quality Report")

st.write("Missing values before cleaning:")
st.write(missing_values)

st.write("Duplicate records removed:", duplicate_count)

st.success("Data Cleaning Completed!")

subjects = ["Maths", "Science", "English", "Computer"]
df["Average"] = df[subjects].mean(axis=1)
df["Result"] = df["Average"].apply(
    lambda marks: "Pass" if marks >= 40 else "Needs Improvement"
)

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Students", len(df))
col2.metric("Class Average", round(df["Average"].mean(), 2))

topper = df.loc[df["Average"].idxmax()]
col3.metric("Top Performer", topper["Student"])

st.divider()

st.header("📋 Student Records")

df["Result"] = df["Average"].apply(
    lambda marks: "Pass" if marks >= 40 else "Needs Improvement"
)

st.dataframe(df, use_container_width=True)
st.download_button(
    label="Download Student Report",
    data=df.to_csv(index=False),
    file_name="student_report.csv",
    mime="text/csv"
)

st.header("📚 Subject-wise Average Analysis")

selected_subject = st.sidebar.selectbox(
    "📚 Select Subject",
    subjects
)
st.write(
    "Average Marks:",
    round(df[selected_subject].mean(), 2)
)

st.bar_chart(
    df.set_index("Student")[selected_subject]
)

st.header("👤 Individual Student Analysis")

student = df[df["Student"] == selected_student].iloc[0]

st.write("Student Name:", selected_student)
st.write("Average Marks:", round(student["Average"], 2))
st.write("Result:", student["Result"])

st.bar_chart(student[subjects])

st.header("📊 Student Performance Trends")

st.line_chart(
    df.set_index("Student")["Average"]
)
st.header("📈 Overall Class Performance")

st.write("Highest Average:", round(df["Average"].max(), 2))
st.write("Lowest Average:", round(df["Average"].min(), 2))
st.header("📚 Subject Performance Analysis")

subject_averages = df[subjects].mean()

st.bar_chart(
    subject_averages.sort_values(ascending=False)
)
best_subject = subject_averages.idxmax()
lowest_subject = subject_averages.idxmin()

st.header("💡 Key Performance Insights")

col1, col2 = st.columns(2)

col1.success(f"🏆 Best Subject: {best_subject}")
col2.info(f"📊 Lowest Subject: {lowest_subject}")
st.header("🎯 Student Result Overview")

result_count = df["Result"].value_counts().reindex(
    ["Pass", "Needs Improvement"],
    fill_value=0
)
col1, col2 = st.columns(2)

col1.metric("Total Pass", result_count["Pass"])
col2.metric("Needs Improvement", result_count["Needs Improvement"])
st.caption("Number of students in each result category")
st.bar_chart(result_count, color="#1f77b4")
total = result_count.sum()

pass_percentage = (result_count.get("Pass", 0) / total) * 100

st.success(f"🎯 Class Pass Percentage: {pass_percentage:.1f}%")
st.header("🏆 Top 5 Performing Students")
st.dataframe(
    df.nlargest(5, "Average")[["Student", "Average"]]
)
st.bar_chart(
    df.nlargest(5, "Average").set_index("Student")["Average"]
)
