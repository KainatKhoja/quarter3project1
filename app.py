import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper" , layout='wide' )

#custom css
st.markdown(
    """
    <style>
    .stApp{
    background-color: black;
    color: white;
    }"
    "</style>"
    """,
    unsafe_allow_html=True
)

#title and description
st.title("🧹Datasweeper Sterling Integerator")
st.write("Convert your files between CSV and Excel formats with integerated data cleaning and visualization")

#file uploader
uploaded_files = st.file_uploader("You can upload your CSV and Excel files here:", type=["csv" , "xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

        #file details
        st.write("🔍 Upload your file to preview the top rows")
        st.dataframe(df.head())

        #data cleaning options
        st.subheader("🛠️Data Cleaning Options") 
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✔️Duplicates Removed!")  

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_detypes(includes=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].means())
                    st.write("✅Missing values have been filled!")

        st.subheader("🎯Select Columns to keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        #data Visualization
        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
             st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #Conversion Options
        
        st.subheader("♻️Conversion Options")
        conversion_type =st.radio(f"Convert {file.name} to:", ["CSV" , "Excel"], key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to.csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mine_type = "text/csv"

            elif conversion_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seak(0) 

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )      

        st.success("🎊All files processed successfully!")     

