import pandas as pd

def run_transformation():
    data = pd.read_csv(r"zipco_transaction.csv")
    
    # Remove Duplicates
    data.drop_duplicates(inplace=True)
    
    # Handle missing values (filling missing numeric values with the mean or median)
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        data.fillna({col: data[col].mean()}, inplace=True)

    # Handle missing values (fill missing string/object values with unknown)
    string_columns = data.select_dtypes(include=['object']).columns
    for col in string_columns:
        data.fillna({col: 'unknown'}, inplace=True)
    
    # Cleaning the Date column: assigning the right data type
    data['Date'] = pd.to_datetime(data['Date'])

    # Creating fact and dimension tables
    # Create Product Table

    products = data[['ProductName']].drop_duplicates().reset_index(drop=True)
    products.index.name = 'ProductID'
    products = products.reset_index()
    
    # Create Customer Table
    customers = data[['CustomerName', 'CustomerAddress', 'Customer_PhoneNumber','CustomerEmail']].drop_duplicates().reset_index(drop=True)
    customers.index.name = 'CustomerID'
    customers = customers.reset_index()
    
    # Create Staff Table
    staff = data[['Staff_Name', 'Staff_Email']].drop_duplicates().reset_index(drop=True)
    staff.index.name = 'StaffID'
    staff = staff.reset_index()
    
    # Create Transaction Table

    transaction = data.merge(products, on='ProductName', how='left') \
        .merge(customers, on=['CustomerName', 'CustomerAddress', 'Customer_PhoneNumber','CustomerEmail'], how='left') \
        .merge(staff, on=['Staff_Name', 'Staff_Email'], how='left')
        
    transaction.index.name = 'TransactionID'
    transaction = transaction.reset_index() \
                            [['Date', 'TransactionID', 'ProductID', 'Quantity', 'UnitPrice', 'StoreLocation', 'PaymentType', 'PromotionApplied', \
                                            'Weather', 'Temperature', 'StaffPerformanceRating', 'CustomerFeedback', 'DeliveryTime_min', 'OrderType', \
                                            'CustomerID', 'StaffID', 'DayOfWeek', 'TotalSales']]
                            
    # Save data as csv files
    data.to_csv('cleaned_data.csv', index=False)
    products.to_csv('product.csv', index=False)
    customers.to_csv('customer.csv', index=False)
    staff.to_csv('staff.csv', index=False)
    transaction.to_csv('transaction.csv', index=False)

    print("Data cleaning and Transformation Completed Successfully.")
