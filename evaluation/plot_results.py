import os
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots


directory = 'output/GDP/GKD-b_n50'
files = ['results_1.csv', 'ref_results_1.csv']

colors = px.colors.qualitative.Plotly

instances = os.listdir(directory)
fig = make_subplots(rows=3, cols=2)
col, row = 1, 1
for count, inst in enumerate(instances):
    inst_path = os.path.join(directory, inst)
    # files = os.listdir(inst_path)
    for file_count, file in enumerate(files):
        plot_name = 'B-GRASP-VND' if file == 'results_1.csv' else 'NSGA-II'

        filename = os.path.join(inst_path, file)

        result_table = pd.read_csv(filename)

        legend_name = 'Constraint values'
        result_table[legend_name] = ('Cost: ' + result_table.Cost.astype(str) +
                                     ' & Capacity: ' + result_table.Capacity.astype(str))

        fig.add_scatter(x=result_table['MaxMin'], y=result_table['MaxSum'],
                        text=result_table[legend_name],
                        mode='markers', line_color=colors[file_count], row=row, col=col,
                        name=plot_name, legendgroup=plot_name,
                        showlegend=True if count == 0 else False)
    # fig = px.scatter(result_table, x='MaxMin', y='MaxSum', color=legend_name,
    #                  color_discrete_sequence=px.colors.qualitative.Light24)
    fig.update_traces(marker={'size': 8})
    fig.update_xaxes(title_text='MaxMin')
    fig.update_yaxes(title_text='MaxSum')
    fig.update_layout(title_text=inst)

    if col == 2:
        row += 1
        col = 1
    else:
        col += 1

fig.show()
