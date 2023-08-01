import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the data
df = pd.read_csv('Amazon Sale Report.csv')
#df['ship-postal-code'] = df['ship-postal-code'].astype(int)
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.date

# Main section
st.title("Amazon Sales Analysis Dashboard")

# Selectbox for Date
selected_date = st.sidebar.selectbox('Select Date', df['Date'].sort_values().unique())

# Selectbox for State
selected_state = st.sidebar.selectbox('Select State', df['ship-state'].unique())

# Selectbox for Country
selected_country = st.sidebar.selectbox('Select Country', df['ship-country'].unique())

# Selectbox for Status
selected_status = st.sidebar.selectbox('Select Status', df['Status'].unique())

# Filter the data based on the selected values
filtered_df = df[(df['Date'] == selected_date) &
                 (df['ship-state'] == selected_state) &
                 (df['ship-country'] == selected_country) &
                 (df['Status'] == selected_status)]

# Show the dataset overview table with selected columns
st.header("Data Overview")
overview_columns = ['Order ID', 'Category', 'Courier Status', 'Qty', 'Amount']
st.dataframe(filtered_df[overview_columns])

# Basic statistics
st.header("Basic Statistics")
st.write(filtered_df.describe())

# Missing values check
#st.header("Missing Values Check")
#st.write(pd.isnull(filtered_df).sum())

# Most used cloth size
st.header("Most Used Cloth Size")
most_used_size = filtered_df['Size'].value_counts().idxmax()
st.write(f"The most used cloth size is {most_used_size}")
st.set_option('deprecation.showPyplotGlobalUse', False)

# Cloth size count plot
#st.header("Cloth Size Count Plot")
#plt.figure(figsize=(8, 5))
#ax = sns.countplot(x='Size', data=filtered_df)
#for bars in ax.containers:
 #   ax.bar_label(bars)
#st.pyplot()

# Cloth size quantity sum plot
st.header("Cloth Size Quantity Sum Plot")
size_bar = filtered_df.groupby('Size', as_index=False)['Qty'].sum().sort_values(by='Qty', ascending=False)
plt.figure(figsize=(10, 5))
ax1 = sns.barplot(x='Size', y='Qty', data=size_bar)
for bars in ax1.containers:
    ax1.bar_label(bars)
st.pyplot()

# Courier Status count plot
st.header("Courier Status Count Plot")
plt.figure(figsize=(10, 5))
ax2 = sns.countplot(data=filtered_df, x='Courier Status', hue='Status')
st.pyplot()

# Category count plot
st.header("Category Count Plot")
plt.figure(figsize=(10, 5))
ax3 = sns.countplot(data=filtered_df, x='Category')
for bars in ax3.containers:
    ax3.bar_label(bars)
st.pyplot()

# B2B Pie chart
st.header("B2B Percentage")
b2b_check = filtered_df['B2B'].value_counts()
plt.figure(figsize=(10, 5))
plt.pie(b2b_check, labels=b2b_check.index, autopct='%1.1f%%')
st.pyplot()

# Scatter plot for Category and Size
st.header("Scatter Plot for Category and Size")
plt.figure(figsize=(10, 5))
plt.scatter(filtered_df['Category'], filtered_df['Size'])
plt.xlabel('Category')
plt.ylabel('Size')
st.pyplot()
