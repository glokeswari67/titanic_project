import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection, read_sql

st.set_page_config(page_title="Titanic Data Analysis", page_icon="🚢", layout="wide")
st.title("🚢 Titanic Dataset Analysis")
st.caption("PostgreSQL • Python • Pandas • Streamlit")

try:
    total_df = read_sql("SELECT COUNT(*) AS total FROM passengers")
    total = int(total_df.iloc[0]["total"])
except Exception as error:
    st.error("Could not connect to the Titanic database. Check the setup instructions and PostgreSQL password.")
    st.code(str(error))
    st.stop()

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Data Explorer", "SQL Practice", "Knowledge Quiz"]
)

if page == "Dashboard":
    st.header("Dashboard")
    summary = read_sql("""
        SELECT COUNT(*) AS total,
               SUM(survived) AS survivors,
               COUNT(*) - SUM(survived) AS not_survived,
               ROUND(100.0 * SUM(survived) / COUNT(*), 2) AS survival_rate
        FROM passengers
    """)
    a, b, c, d = st.columns(4)
    a.metric("Total Passengers", f'{int(summary.iloc[0]["total"]):,}')
    b.metric("Survived", f'{int(summary.iloc[0]["survivors"]):,}')
    c.metric("Did Not Survive", f'{int(summary.iloc[0]["not_survived"]):,}')
    d.metric("Survival Rate", f'{summary.iloc[0]["survival_rate"]}%')

    left, right = st.columns(2)
    with left:
        gender = read_sql("""
            SELECT sex, COUNT(*) AS passengers
            FROM passengers GROUP BY sex ORDER BY sex
        """)
        st.subheader("Passengers by Gender")
        st.plotly_chart(px.pie(gender, names="sex", values="passengers",
                               title="Gender distribution"), use_container_width=True)
    with right:
        survival = read_sql("""
            SELECT CASE WHEN survived=1 THEN 'Survived'
                        ELSE 'Did not survive' END AS result,
                   COUNT(*) AS passengers
            FROM passengers GROUP BY survived ORDER BY survived
        """)
        st.subheader("Survival Distribution")
        st.plotly_chart(px.bar(survival, x="result", y="passengers",
                               color="result"), use_container_width=True)

    class_data = read_sql("""
        SELECT pclass, COUNT(*) AS passengers,
               ROUND(100.0*SUM(survived)/COUNT(*),2) AS survival_rate
        FROM passengers GROUP BY pclass ORDER BY pclass
    """)
    st.subheader("Passenger Class Analysis")
    st.plotly_chart(px.bar(class_data, x="pclass", y="survival_rate",
                           labels={"pclass":"Passenger class",
                                   "survival_rate":"Survival rate (%)"}),
                    use_container_width=True)
    st.dataframe(class_data, use_container_width=True)

elif page == "Data Explorer":
    st.header("Data Explorer")
    filters1, filters2, filters3 = st.columns(3)
    with filters1:
        selected_class = st.selectbox("Passenger class", ["All", 1, 2, 3])
    with filters2:
        selected_sex = st.selectbox("Gender", ["All", "female", "male"])
    with filters3:
        selected_survival = st.selectbox("Survival", ["All", "Survived", "Not survived"])

    query = "SELECT * FROM passengers WHERE 1=1"
    params = []
    if selected_class != "All":
        query += " AND pclass = %s"
        params.append(selected_class)
    if selected_sex != "All":
        query += " AND sex = %s"
        params.append(selected_sex)
    if selected_survival != "All":
        query += " AND survived = %s"
        params.append(1 if selected_survival == "Survived" else 0)
    query += " ORDER BY passengerid"
    data = read_sql(query, params)
    st.write(f"Showing **{len(data)}** passengers")
    st.dataframe(data, use_container_width=True, height=450)
    st.download_button("Download filtered CSV", data.to_csv(index=False).encode("utf-8"),
                       "titanic_filtered.csv", "text/csv")

elif page == "SQL Practice":
    st.header("SQL Practice")
    st.write("Try read-only SELECT queries on the passengers table.")
    examples = {
        "Show first 10 passengers": "SELECT * FROM passengers ORDER BY passengerid LIMIT 10",
        "Count passengers by gender": "SELECT sex, COUNT(*) AS total FROM passengers GROUP BY sex",
        "Survival by passenger class": "SELECT pclass, SUM(survived) AS survivors, COUNT(*) AS total FROM passengers GROUP BY pclass ORDER BY pclass",
        "Average age by gender": "SELECT sex, ROUND(AVG(age)::numeric, 2) AS average_age FROM passengers GROUP BY sex"
    }
    choice = st.selectbox("Example queries", list(examples))
    sql = st.text_area("SQL query", value=examples[choice], height=130)
    if st.button("Run query"):
        cleaned = sql.strip().lower()
        if not cleaned.startswith("select") or ";" in cleaned.rstrip(";"):
            st.warning("Only one SELECT query is allowed.")
        else:
            try:
                result = read_sql(sql)
                st.success(f"Query returned {len(result)} rows.")
                st.dataframe(result, use_container_width=True)
            except Exception as error:
                st.error(f"Query error: {error}")

else:
    st.header("Knowledge Quiz")
    questions = [
        ("How many records are in the training dataset?", ["891", "500", "1200"], "891"),
        ("Which column indicates survival?", ["Pclass", "Survived", "Fare"], "Survived"),
        ("What does Survived = 1 mean?", ["Passenger survived", "Passenger did not survive", "Missing value"], "Passenger survived"),
        ("Which SQL command retrieves data?", ["INSERT", "UPDATE", "SELECT"], "SELECT"),
        ("Which Python library is used for tabular data analysis?", ["Pandas", "Turtle", "Pygame"], "Pandas")
    ]
    score = 0
    answers = []
    with st.form("quiz"):
        for index, (question, options, answer) in enumerate(questions):
            selected = st.radio(question, options, key=f"q{index}")
            answers.append((selected, answer))
        submitted = st.form_submit_button("Submit answers")
    if submitted:
        score = sum(selected == answer for selected, answer in answers)
        st.success(f"Your score: {score} / {len(questions)}")
