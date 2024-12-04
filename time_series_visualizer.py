import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
data = 'fcc-forum-pageviews.csv'

df = pd.read_csv(data,
    parse_dates = ['date'],
    index_col = 0)

# Clean data

upper_bound = df.value.quantile(0.975)
lower_bound = df.value.quantile(0.025)

df =  df[
        (df['value'] < upper_bound) &
        (df['value'] > lower_bound)
        ]

def draw_line_plot():
    # Draw line plot
    plt.figure(figsize=(13, 5))
    fig1 = plt.plot(df.index,
                df.value,
                c='r',
                linewidth = 1)

    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.ylim(10000, 190000) 

    # Save image and return fig (don't change this part)
    fig = plt.gcf()
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.reset_index()
    df_bar['year'] = pd.DatetimeIndex(df_bar.date).year
    df_bar['Months'] = pd.DatetimeIndex(df_bar.date).month
    df_bar['day'] = pd.DatetimeIndex(df_bar.date).day

    month_names = [
        "January", "February", "March", "April", "May", "June", "July", "August", 
        "September", "October", "November", "December"
    ]

    df_bar['Months'] = df_bar['Months'].apply(lambda x: month_names[x - 1])
    df_bar= df_bar.groupby(['year','Months'])['value'].mean()
    df_bar = pd.DataFrame(df_bar).reset_index()


    month_order = [
            "January", "February", "March", "April", "May", "June", "July", "August", 
            "September", "October", "November", "December"
    ]

    palette = sns.color_palette("tab10", n_colors=12)

    facet = sns.catplot(data = df_bar,
                        x = 'year',
                        y = 'value',
                        hue = 'Months',
                        kind = 'bar',
                        palette = palette,
                        legend_out = False,
                        hue_order = month_order 
    )

    facet.set_axis_labels('Years', 'Average Page Views')
    facet.set_xticklabels(rotation=90)

    # Save image and return fig (don't change this part)
    fig = plt.gcf()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    plt.rcParams.update({'font.family': 'sans-serif'})

    fig , (ax1,ax2) = plt.subplots(1, 2, figsize = (26,5))

    sns.boxplot(data = df_box, x = df_box.year, y = df_box.value,
                hue = df_box.year,
                ax = ax1,
                legend = False,
                palette = sns.color_palette(n_colors = 4),
                flierprops = dict(marker ='d', markersize = 1.5, markerfacecolor ='black'),
                linewidth = .5
            )

    ax1.set_ylim(0, 200000)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")
    ax1.set_yticks(np.arange(0, 200001, 20000))
    ax1.set_title("Year-wise Box Plot (Trend)")

    fig3 = sns.boxplot(data = df_box, x = df_box.month, y = df_box.value,
                hue = df_box.month,
                legend = False,
                ax = ax2,
                flierprops = dict(marker ='d', markersize = 1.5, markerfacecolor ='black'),
                linewidth = .5,
                order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep',"Oct", "Nov", "Dec"],
                palette = sns.color_palette("husl", 12), 
                hue_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep',"Oct", "Nov", "Dec"] 
            )

    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")
    ax2.set_yticks(np.arange(0, 200001, 20000))
    ax2.set_ylim(0, 200000)  

    # Save image and return fig (don't change this part)
    fig = plt.gcf()
    fig.savefig('box_plot.png')
    return fig
