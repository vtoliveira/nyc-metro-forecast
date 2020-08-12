# nyc-metro-forecast

Repository where I use Turnstile MTA Dataset to create forecasts.

The notebooks are structured in this way:

 - *00-exploratory-data-analysis:* Basically, data exploration + heavy work of data preprocessing. I discuss details of data thinking in how to structure it
 for forecasting purposes.
 - *01-exploratory-data-analysis:* I continue my exploration, but now exploring data through visualizations and checking data properties.
 - *02-hierarchical-data-definition:* I create visualization showing hierarchical structure and prepare data to be used in forecast notebook.
 - *03-forecasting-metro-users:* I explore basic concepts regarding time series analysis. Cross-validation, baselines, ACF and PACF plots as well basic models
 such as ARIMA and HW. In the end, we fit model based on hierarchical structure.
