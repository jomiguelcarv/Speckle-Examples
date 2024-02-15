# If this thows you a Module Error, do:
# pip install pandas plotly
import pandas as pd
import plotly.graph_objects as go

# Import the csv we created in versioning.py
df = pd.read_csv("commit_data.csv")

# Assign a unique y value to each branch
# So that we can display all the commits of the same branch in the same Y-axis position
branch_mapping = {branch: i for i, branch in enumerate(df['branch'].unique())}
df['y_value'] = df['branch'].map(branch_mapping)

# Create an interactive scatter plot
fig = go.Figure()

# Organize our CSV into "groups", where each group is made of commits of the same branch
for branch, group in df.groupby('branch'):

    # We draw a line connecting the commits of the same branch
    # We also make the plot dots show us the commit message if we hover it
    trace = go.Scatter(x=group['date'], y=group['y_value'], mode='markers+lines',
                      marker=dict(symbol='circle', size=8),
                      name=branch, hovertemplate='%{text}', text=group['message'],
                      showlegend=False)
    fig.add_trace(trace)

    # And we draw the dates along the X-axis
    for date, y_value, author in zip(group['date'], group['y_value'], group['author']):
        fig.add_annotation(
            x=date,
            y=y_value+0.1,
            text=author,
            showarrow=False,
            font=dict(size=8)
        )

# All done! Just add last minute things like a title and the legend
# This is also where you control the color, stroke widths, etc to make it look like you want to
fig.update_layout(
    title='Commit History',
    xaxis_title='Date',
    yaxis_title='Branch',
    yaxis=dict(tickvals=list(branch_mapping.values()), ticktext=list(branch_mapping.keys()), gridcolor='lightgrey'),
    legend_title='Branch',
    plot_bgcolor='rgba(0, 0, 0, 0)'
)

# And we show the interactive plot on the browser
fig.show()
