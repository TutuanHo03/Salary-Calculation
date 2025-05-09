import streamlit as st
import pandas as pd
import requests
import io
import base64
import os

# Page Configuration
st.set_page_config(
    page_title="Salary Calculator",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🧮 Salary Calculator")
st.markdown("---")

# Lấy API URL từ biến môi trường hoặc dùng giá trị mặc định
API_URL = os.environ.get("API_URL", "http://backend:8000")

tab1, tab2 = st.tabs(["Single Calculation", "Bulk Upload"])

# Tab single calculation
with tab1:
    st.header("Calculate Net Salary")
    
    # Form salary calculation
    with st.form("salary_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            gross_salary = st.number_input("Gross Salary (VND)", min_value=0.0, step=1000000.0, format="%f")
        
        with col2:
            dependents = st.number_input("Number of Dependents", min_value=0, step=1)
        
        submit_button = st.form_submit_button("Calculate")
        
        if submit_button:
            try:
                response = requests.post(
                    f"{API_URL}/api/salary/calculate",
                    json={"gross_salary": gross_salary, "number_of_dependents": dependents}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Calculation successful!")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Gross Salary", f"{result['gross_salary']:,.0f} VND")
                        st.metric("Insurance Amount", f"{result['insurance_amount']:,.0f} VND")
                    
                    with col2:
                        st.metric("Net Salary", f"{result['net_salary']:,.0f} VND")
                        st.metric("Personal Income Tax", f"{result['personal_income_tax']:,.0f} VND")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error connecting to server: {str(e)}")

# Tab upload file
with tab2:
    st.header("Bulk Salary Calculation")
    
    st.subheader("Download Template")
    
    def create_template():
        df = pd.DataFrame({
            'ID': [1, 2],
            'Employee Name': ['John Doe', 'Jane Smith'],
            'Gross Salary': [10000000, 15000000],
            'Number of Dependents': [0, 1]
        })
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        return buffer
    
    template_buffer = create_template()
    template_data = base64.b64encode(template_buffer.getvalue()).decode('utf-8')
    st.download_button(
        label="📥 Download Excel Template",
        data=template_buffer,
        file_name="salary_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.subheader("Upload Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())
        
        if st.button("Process Salaries"):
            try:
                files = {'file': uploaded_file.getvalue()}
                
                response = requests.post(
                    f"{API_URL}/api/salary/upload",
                    files={'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    result_df = pd.DataFrame(result['result'])
                    
                    st.success("Calculation successful!")
                    st.dataframe(result_df)
                    
                    buffer = io.BytesIO()
                    result_df.to_excel(buffer, index=False)
                    st.download_button(
                        label="📥 Download Results",
                        data=buffer,
                        file_name="salary_results.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

st.markdown("---")
st.caption("Salary Calculator App | Made with Streamlit by TutuanHo03")
