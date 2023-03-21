# companydb_fbprophet

This code uses FBProphet library to perform time-series analysis and make predictions on the prices of a company's main products. It first reads a clean CSV file containing the sales data, and then prompts the user to input the name of the product they want to analyze. It also gets the USD/BRL conversion rate using the bcb package.

Also the function called 'general' generates a graphic with the monthly sales price of a specific product imported from the company DB.
We used a Bollinger based model to analyze price, using the Bollinger bands priciples.

The data is grouped, filtered, and merged to collect dollarized values. The user can choose to analyze the data in either USD or BRL. The code includes functions for plotting price over time and for creating Bollinger bands, as well as a function that uses Prophet modeling to predict future prices.

Overall, this code provides a useful tool for businesses to analyze their price buying data and make informed decisions about pricing and forecasting.
