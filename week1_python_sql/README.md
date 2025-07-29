# Week 1: Python & SQL Fundamentals

## 🎯 Week Goals

Welcome to Week 1 of the AI Knowledge Assistant internship! This week focuses on building a solid foundation in Python programming and SQL database operations. You'll learn to clean, analyze, and visualize data - essential skills for any AI/ML project.

### 📚 Learning Objectives

By the end of this week, you will be able to:

- **Python Programming**
  - Write clean, efficient Python code following best practices
  - Use pandas for data manipulation and analysis
  - Create data visualizations with matplotlib and seaborn
  - Handle errors and exceptions properly
  - Work with different data formats (CSV, JSON, Excel)

- **SQL Database Operations**
  - Write complex SQL queries for data retrieval
  - Design and create database schemas
  - Perform data aggregation and grouping
  - Join multiple tables effectively
  - Optimize queries for performance

- **Data Analysis Skills**
  - Identify and handle missing data
  - Detect and remove outliers
  - Perform exploratory data analysis (EDA)
  - Create meaningful visualizations
  - Generate insights from data

## 📋 Assignments

### Assignment 1: Data Cleaning & Analysis (40 points)
- [ ] Load and examine the provided `data.csv` file
- [ ] Identify data quality issues (missing values, duplicates, outliers)
- [ ] Clean the dataset using pandas
- [ ] Perform basic statistical analysis
- [ ] Create 3-5 meaningful visualizations
- [ ] Write a summary report of findings

### Assignment 2: SQL Database Operations (30 points)
- [ ] Design a database schema for the cleaned data
- [ ] Create SQL tables and insert data
- [ ] Write 5 complex queries demonstrating different SQL concepts
- [ ] Perform data aggregation and grouping operations
- [ ] Create views for commonly accessed data

### Assignment 3: Data Visualization Dashboard (20 points)
- [ ] Create an interactive dashboard using Streamlit or Plotly
- [ ] Include multiple visualization types (bar, line, scatter, heatmap)
- [ ] Add filtering and selection capabilities
- [ ] Make the dashboard responsive and user-friendly

### Assignment 4: Code Quality & Documentation (10 points)
- [ ] Write comprehensive docstrings for all functions
- [ ] Include type hints in Python code
- [ ] Create a requirements.txt file
- [ ] Write a detailed README for your project
- [ ] Follow PEP 8 coding standards

## 📁 Folder Checklist

```
week1_python_sql/
├── README.md                    # This file
├── starter/
│   ├── data.csv                # Sample messy CSV data
│   ├── api_sample_url.txt      # Example API URL for bonus task
│   └── requirements.txt        # Python dependencies
└── submission/
    ├── data_cleaning.py        # Data cleaning script
    ├── sql_operations.py       # SQL database operations
    ├── visualization_dashboard.py # Interactive dashboard
    ├── analysis_report.md      # Summary of findings
    ├── database_schema.sql     # SQL schema design
    └── README.md               # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ installed
- SQLite or PostgreSQL installed
- Jupyter Notebook or VS Code with Python extensions
- Git for version control

### Setup Instructions

1. **Create a virtual environment**
   ```bash
   python -m venv week1_env
   source week1_env/bin/activate  # On Windows: week1_env\Scripts\activate
   ```

2. **Install required packages**
   ```bash
   pip install pandas numpy matplotlib seaborn sqlalchemy streamlit plotly
   pip freeze > requirements.txt
   ```

3. **Download the starter data**
   - Copy `data.csv` from the `starter/` folder
   - Examine the data structure and quality issues

4. **Set up your development environment**
   - Open VS Code or Jupyter Lab
   - Create your Python scripts in the `submission/` folder
   - Use Git for version control

## 📊 Sample Data Description

The `data.csv` file contains:
- **Customer data** with various quality issues
- **Sales transactions** with missing values
- **Product information** with inconsistent formatting
- **Geographic data** with outliers

Your task is to clean this data and extract meaningful insights.

## 🔧 Technical Requirements

### Python Libraries
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib/seaborn**: Data visualization
- **sqlalchemy**: Database operations
- **streamlit/plotly**: Interactive dashboards

### SQL Skills
- **SELECT** statements with WHERE, ORDER BY, GROUP BY
- **JOIN** operations (INNER, LEFT, RIGHT, FULL)
- **Aggregate functions** (COUNT, SUM, AVG, MAX, MIN)
- **Subqueries** and **CTEs** (Common Table Expressions)
- **Window functions** for advanced analytics

## 📝 Submission Instructions

### Due Date
**Friday, 5:00 PM**

### Submission Format
1. **Code Files**: All Python scripts and SQL files
2. **Documentation**: README.md with setup and usage instructions
3. **Report**: Analysis report in Markdown format
4. **Database**: SQLite file or PostgreSQL dump

### Submission Checklist
- [ ] All code runs without errors
- [ ] Documentation is complete and clear
- [ ] Visualizations are properly labeled and explained
- [ ] SQL queries are optimized and well-commented
- [ ] Git repository is properly organized

### Code Review Criteria
- **Functionality**: Code works as expected
- **Readability**: Clean, well-commented code
- **Efficiency**: Optimized algorithms and queries
- **Documentation**: Clear explanations and examples
- **Best Practices**: Follows Python and SQL conventions

## 🎯 Bonus Challenges

### Challenge 1: API Integration (5 extra points)
- Use the API URL in `api_sample_url.txt`
- Fetch additional data and integrate with existing dataset
- Handle API rate limiting and errors

### Challenge 2: Advanced SQL (5 extra points)
- Implement complex window functions
- Create stored procedures or functions
- Optimize query performance with indexes

### Challenge 3: Machine Learning Preview (5 extra points)
- Perform basic clustering analysis
- Create a simple predictive model
- Evaluate model performance

## 📚 Suggested Resources

### Python Learning
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Real Python Tutorials](https://realpython.com/)

### SQL Learning
- [SQL Tutorial by W3Schools](https://www.w3schools.com/sql/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

### Data Analysis
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Pandas Cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html)
- [Matplotlib Tutorial](https://matplotlib.org/stable/tutorials/index.html)

### Best Practices
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [SQL Style Guide](https://www.sqlstyle.guide/)

## 🤝 Office Hours & Support

- **Tuesday**: 2-4 PM - Python programming help
- **Thursday**: 2-4 PM - SQL and database questions
- **Slack**: #week1-python-sql for quick questions
- **Email**: week1-support@company.com

## 📈 Success Metrics

You'll be evaluated on:
- **Technical Skills**: Code quality and functionality (60%)
- **Analysis**: Data insights and visualizations (25%)
- **Documentation**: Clarity and completeness (10%)
- **Bonus**: Extra challenges completed (5%)

---

**Remember**: This week sets the foundation for everything that follows. Take your time to understand the concepts thoroughly. Don't hesitate to ask questions!

**Good luck! 🚀** 