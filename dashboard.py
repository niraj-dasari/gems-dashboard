import streamlit as st
import pandas as pd

# Define function to read data from Excel file
def read_data(file):
    df = pd.read_excel(file)
    return df

# Define function to write data to Excel file
def write_data(df, file):
    writer = pd.ExcelWriter(file)
    df.to_excel(writer, index=False)
    writer.save()

# Define function to add new employee details
def add_employee(data, df):
    new_row = {}
    for column in df.columns:
        new_row[column] = data[column]
    df = df.append(new_row, ignore_index=True)
    return df

# Define function to update existing employee details
def update_employee(data, row_index, df):
    for column in df.columns:
        df.loc[row_index, column] = data[column]
    return df

# Define function to delete existing employee details
def delete_employee(e_deatils, df):
    # st.dataframe(df[~df.isin(e_deatils)])
    df = df[~df.isin(e_deatils)]
    return df

# Define function to search for employee details
def search_employee(keyword, df):
    result_df = df[df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
    return result_df

# Define the main function
def main():
    st.title("Employee Details Management")

    # Allow users to upload their Excel file
    file = st.file_uploader("Upload Excel file", type=["xlsx"])
    if file is not None:
        df = read_data(file)

        # Display the employee details
        st.subheader("Employee Details")

        # Allow users to search for employee details
        keyword = st.text_input("Search by keyword")
        if keyword:
            result_df = search_employee(keyword, df)
            st.dataframe(result_df)
        else:
            st.dataframe(df)

        # Allow users to add new employee details
        st.subheader("Add New Employee")
        data = {}
        for column in df.columns:
            data[column] = st.text_input(column)
        if st.button("Add Employee"):
            df = add_employee(data, df)
            st.success("Employee details added successfully!")
            st.dataframe(df)

        # Allow users to update existing employee details
        st.subheader("Update Employee Details")
        row_index = st.number_input("Row Index", min_value=0, max_value=len(df)-1)
        data = {}
        for column in df.columns:
            data[column] = st.text_input(column, value=df.iloc[row_index][column])
        if st.button("Update Employee"):
            df = update_employee(data, row_index, df)
            st.success("Employee details updated successfully!")
            st.dataframe(df)

        # Allow users to delete existing employee details
        st.subheader("Delete Employee Details")
        e_details = st.text_input("Search employee to delete")
        if e_details:
            result_df = search_employee(e_details, df)
            st.dataframe(result_df)
            if st.button("Delete Employee"):
                df = delete_employee(result_df, df)
                st.success("Employee details deleted successfully!")
                
        st.dataframe(df)


        # Allow users to download the modified Excel file
        st.subheader("Download Modified Excel File")
        if st.button("Download Excel"):
            # determining the name of the file
            file_name = 'data.xlsx'
            
            # saving the excel
            df.to_excel(file_name)



if __name__ == "__main__":
    main()
