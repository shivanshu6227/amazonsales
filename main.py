import pandas as pd

# Load the dataset
file_path = "C:\\Users\\Lenovo\\Downloads\\Amazon Sale Report.csv"
sales_data = pd.read_csv(file_path)

# Display basic info
sales_data.info()

# Convert 'date' column to datetime
sales_data['date'] = pd.to_datetime(sales_data['date'], errors='coerce')

# Filter for shipped/delivered orders only
successful_orders = sales_data[sales_data['Status'].str.contains("Shipped", na=False)]


import matplotlib.pyplot as plt

# Aggregate sales amount and quantity by date
daily_sales = successful_orders.groupby('date').agg({'amount': 'sum', 'qty': 'sum'}).reset_index()

# Plot daily sales amount
plt.figure(figsize=(14, 6))
plt.plot(daily_sales['date'], daily_sales['amount'], label='Sales Amount (INR)', color='blue')
plt.title('Daily Sales Amount Over Time',fontsize=15 )
plt.xlabel('Date',fontsize=15)
plt.ylabel('Sales Amount (INR)',fontsize=15)
plt.legend()
plt.show()

# Group by category and size
category_sales = successful_orders.groupby(['category', 'size']).agg({'qty': 'sum', 'amount': 'sum'}).reset_index()

# Bar plot for quantity by category
plt.figure(figsize=(12, 6))
plt.bar(category_sales['category'], category_sales['qty'], color='skyblue',label='quantity by category')
plt.title('Quantity Sold by Product Category', fontsize=15)
plt.xlabel('Product Category',fontsize=15)
plt.ylabel('Quantity Sold',fontsize=15)
plt.xticks(rotation=45)
plt.legend()
plt.show()


# Count by fulfillment type
fulfillment_counts = successful_orders['fulfilment'].value_counts()

# Pie chart for fulfillment methods
plt.figure(figsize=(7, 7))
ex=[0.0,0.2]
plt.pie(fulfillment_counts, labels=fulfillment_counts.index, autopct='%0.1f%%', startangle=140,explode=ex,shadow=True,radius=1.5,wedgeprops={"linewidth":5})
plt.title('Fulfillment Method Distribution')
plt.show()

# Group by ship-city and ship-state
city_sales = successful_orders.groupby('ship-city').agg({'amount': 'sum'}).sort_values(by='amount', ascending=False).head(10)

# Plot top cities by sales
plt.figure(figsize=(12, 6))
plt.bar(city_sales.index, city_sales['amount'], color='orange')
plt.title('Top 10 Cities by Sales Amount',fontsize=15)
plt.xlabel('City',fontsize=15)
plt.ylabel('Sales Amount (INR)',fontsize=15)
plt.xticks(rotation=45)
plt.show()


# Aggregate data to create a customer profile
customer_profile = successful_orders.groupby('ship-postal-code').agg({
    'amount': 'sum',                    # Total purchase amount per customer
    'order id': 'count',                 # Total orders per customer
    'category': lambda x: x.mode()[0],   # Most frequently purchased category
    'ship-state': 'first',               # State (or city) information
}).reset_index()

# Rename columns for clarity
customer_profile.rename(columns={'order id': 'order_count', 'amount': 'total_spent'}, inplace=True)

# Define thresholds for spending and frequency segments
high_spending_threshold = customer_profile['total_spent'].quantile(0.75)  # Top 25% spenders
frequent_buyer_threshold = customer_profile['order_count'].quantile(0.75)  # Top 25% in frequency

# Segment customers based on thresholds
customer_profile['spending_segment'] = customer_profile['total_spent'].apply(
    lambda x: 'High Spender' if x >= high_spending_threshold else 'Low Spender'
)

customer_profile['frequency_segment'] = customer_profile['order_count'].apply(
    lambda x: 'Frequent Buyer' if x >= frequent_buyer_threshold else 'Occasional Buyer'
)

# Group by spending and frequency segments to find popular categories within each segment
category_segments = customer_profile.groupby(['spending_segment', 'frequency_segment', 'category']).size().unstack().fillna(0)

# Plotting spending segment distribution
plt.figure(figsize=(10, 6))
customer_profile['spending_segment'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Customer Spending Segmentation')
plt.xlabel('Spending Segment')
plt.ylabel('Number of Customers')
plt.show()

# Plotting frequency segment distribution
plt.figure(figsize=(10, 6))
customer_profile['frequency_segment'].value_counts().plot(kind='bar', color='salmon')
plt.title('Customer Frequency Segmentation',fontsize=15)
plt.xlabel('Frequency Segment',fontsize=15)
plt.ylabel('Number of Customers',fontsize=15)
plt.show()    












