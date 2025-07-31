# Week 1 Submission

## 📁 Submission Contents

This folder contains your Week 1 Python & SQL assignments.

### Required Files
- [ ] `data_cleaning.py` - Data cleaning and analysis script
- [ ] `sql_operations.py` - SQL database operations
- [ ] `visualization_dashboard.py` - Interactive dashboard
- [ ] `analysis_report.md` - Summary of findings
- [ ] `database_schema.sql` - SQL schema design
- [ ] `README.md` - Project documentation (this file)

### Submission Checklist
- [ ] All code runs without errors
- [ ] Documentation is complete and clear
- [ ] Visualizations are properly labeled
- [ ] SQL queries are optimized
- [ ] Git repository is organized

## 🚀 How to Run

1. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r ../starter/requirements.txt
   ```

2. **Run data cleaning**
   ```bash
   python data_cleaning.py
   ```

3. **Run SQL operations**
   ```bash
   python sql_operations.py
   ```

4. **Run dashboard**
   ```bash
   streamlit run visualization_dashboard.py
   ```

## 📊 Results Summary

- Most customers come from USA, Canada and Australia.
- Highest spending product categories: Electronics, Clothing, and Home & Garden.
- Average spending is highest among customers aged 25–35.
- Customer spending tends to increase near the end of the year (especially Nov–Dec).
- The dataset initially contained some invalid data such as future countries and dates, which were cleaned.

## 🎯 Learning Outcomes

- Learned how to clean and validate data using Python and Pandas.
- Practiced using SQLite to store, query, and manage customer data.
- Gained experience creating dashboards using Streamlit for data visualization.
- Understood the importance of removing invalid entries like future dates or fake country names to maintain data integrity.
- Improved confidence using Visual Studio Code, managing environments, and debugging issues.

## Streamlit

  You can now view Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.16.0.135:8501

  ## Project Overview
Analyze customer purchasing behavior from different countries and product categories using:
- Python (Pandas, SQLite)
- Streamlit (dashboard)
- SQL queries