import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
#Add an overweight column to the data. 
BMI=df['weight']/((df['height']*0.01) ** 2)
df['overweight'] = (BMI>25).astype(int)

# 3 Normalize the data by making 0 always good and 1 always bad. 
# If the value of cholesterol or gluc is 1, make the value 0. 
# If the value is more than 1, make the value 1.
df['cholesterol']=(df['cholesterol']>1).astype(int)
df['gluc']=(df['gluc']>1).astype(int)


# 4
def draw_cat_plot():
    # 5Create a DataFrame for the cat plot using pd.melt with values from cholesterol, 
    # gluc, smoke, alco, active, and overweight in the df_cat variable.

    df_cat = pd.melt(df, id_vars=['id','cardio'],value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'], var_name='Variable', value_name='Value')


    # 6 Group and reformat the data in df_cat to split it by cardio. 
    # Show the counts of each feature. You will have to rename one of the columns for 
    # the catplot to work correctly.

    df_value_counts=df_cat.groupby(['cardio','Variable'])['Value'].value_counts()
    df_value_counts.name='total'
    value_counts_df = df_value_counts.reset_index()
    value_counts_df.columns = ['cardio', 'variable','value','total'] 

    # 7nvert the data into long format and create a chart that shows the value counts of 
    # the categorical features using the following method provided by the seaborn
    #  library import : sns.catplot()
    g=sns.catplot(x="variable", y="total", hue="value", col="cardio", data=value_counts_df, kind='bar')
    
    # 8 Get the figure for the output and store it in the fig variable
    fig=g.fig

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11 Clean the data in the df_heat variable by filtering out the following patient segments that represent incorrect data:
    #height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
    #height is more than the 97.5th percentile
    #weight is less than the 2.5th percentile
    #weight is more than the 97.5th percentile
    df_heat = df[(df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) 
                & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))
                &(df['ap_lo'] <= df['ap_hi'])]


    # 12 Calculate the correlation matrix and store it in the corr variable
    corr = df_heat.corr()

    # 13 Generate a mask for the upper triangle and store it in the mask variable
    mask = np.triu(np.ones_like(corr, dtype=bool))


    # 14 Set up the matplotlib figure
    fig, ax = plt.subplots()

    # 15 Plot the correlation matrix using the method provided by the seaborn library import: sns.heatmap()
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', linewidths=0.5)  
    

    # 16
    fig.savefig('heatmap.png')
    return fig
