#imports
import streamlit as st
import streamlit.components.v1 as components
import pydeck as pdk
import numpy as np
import pandas as pd 
from functools import reduce
import altair as alt

st.title("Department Overview")

#Loading data
@st.experimental_singleton
def load_data():
    manager_survey = pd.read_csv('manager_survey_data.csv',  sep = ',')
    return manager_survey

manager_survey = load_data()

@st.experimental_singleton
def load_data():
    general_data = pd.read_csv('general_data.csv',  sep = ',')
    return general_data

general_data = load_data()

@st.experimental_singleton
def load_data():
    employee_data = pd.read_csv('employee_survey_data.csv',  sep = ',')
    return employee_data

employee_data = load_data()

emp_man = pd.merge(manager_survey, employee_data, on='EmployeeID')
data_hr = pd.merge(emp_man, general_data, on='EmployeeID')

data_hr.dropna(inplace=True)
data_hr.drop(['Over18', 'EmployeeCount', 'StandardHours'], inplace=True, axis=1)

data_hr = data_hr.astype({'EnvironmentSatisfaction':'int64','JobSatisfaction':'int64','WorkLifeBalance':'int64','NumCompaniesWorked':'int64'})
data_hr['Attrition'] = data_hr['Attrition'].replace(['Yes'],True)
data_hr['Attrition'] = data_hr['Attrition'].replace(['No'],False)
AttritionFalse = data_hr[data_hr.Attrition == False]

#Select box

option = st.selectbox(
    'Department',
    ('Human Resources', 'Research & Development', 'Sales'))

st.write('You selected:', option)

AttritionFalse['AgeGroups'] = pd.cut(AttritionFalse['Age'], bins=[18, 25, 30, 40, 50, 60, 70, np.inf], include_lowest=True)
filtered_df = AttritionFalse[AttritionFalse['Department'] == option]
#Education Plot

education_chart = pd.crosstab(filtered_df.EducationField, filtered_df.EducationField.count())
st.bar_chart(education_chart)

#Age Plot

Age_chart = pd.crosstab(filtered_df.AgeGroups, filtered_df.AgeGroups.count())
st.bar_chart(education_chart)

#