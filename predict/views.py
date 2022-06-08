from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
import pandas as pd
import pickle
from tensorflow import keras
from keras.models import load_model
import tensorflow as tf
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.palettes import Spectral4
from bokeh.models import ColumnDataSource

pred_cols = ['reactivity', 'deg_Mg_pH10', 'deg_Mg_50C', 'deg_pH10', 'deg_50C']
# Load model
model = load_model('gru_pub.h5', compile=False)

# submit_result = NULL

# Create your views here.
def predict(request):
    token2int = {x:i for i, x in enumerate('().ACGUBEHIMSX')}
    if request.method == "POST":
        #Get input from form
        sequence = request.POST.get('sequence')
        structure = request.POST.get('structure')
        predicted_loop_type = request.POST.get('predicted_loop_type')
        length = request.POST.get('length')
        score = request.POST.get('score')

        #Convert input from list to DataFrame
        preds_in = [[
            sequence,
            structure,
            predicted_loop_type,
            length,
            score
        ]]
        
        preds_in = pd.DataFrame(preds_in,
               columns =['sequence', 'structure', 'predicted_loop_type', 'seq_length', 'seq_scored'])

        # Preprocess input
        pre_preds_in = preprocess_inputs(preds_in, token2int)
        preds_out = model.predict(pre_preds_in)
        
        # Postprecess
        preds_ls = []
        index_array = []
        bazo_array = []
        
        for i in range(0, 107):
            index_array.append(i)
            bazo_array.append(sequence[i])
            
        for df, preds in [(preds_in, preds_out)]:
            for i, uid in enumerate(df.sequence):
                single_pred = preds[i]

                single_df = pd.DataFrame(single_pred, columns=pred_cols)
                preds_ls.append(single_df)

        preds_df = pd.concat(preds_ls)
        preds_df['bazo'] = bazo_array
        preds_df['index'] = index_array
        
        data = preds_df.values.tolist()
        
        #Plot
        #Countplot
        bazo = ['G','A','C','U']
        counts = preds_df['bazo'].value_counts().reindex(['G','A','C','U'], fill_value=0)

        bazo_plot = get_barplot(bazo, counts)
        #Lineplot
        r_plot = get_lineplot(preds_df, 'index', 'reactivity', 500, 400, 'Reactivity')
        deg_Mg_pH10_plot = get_lineplot(preds_df, 'index', 'deg_Mg_pH10', 500, 400)
        deg_Mg_50C_plot = get_lineplot(preds_df, 'index', 'deg_Mg_50C', 500, 400)
        deg_pH10_plot = get_lineplot(preds_df, 'index', 'deg_pH10', 500, 400)
        deg_50C_plot = get_lineplot(preds_df, 'index', 'deg_50C', 500, 400)
        
        return render(request, 'results.html', {'data': data, 'r_plot': r_plot,
                                                'bazo_plot': bazo_plot, 
                                                'deg_Mg_pH10_plot': deg_Mg_pH10_plot, 
                                                'deg_Mg_50C_plot': deg_Mg_50C_plot,
                                                'deg_pH10_plot': deg_pH10_plot,
                                                'deg_50C_plot': deg_50C_plot
                                                })

    return render(request, 'predict.html')

def results(request):
    return render(request, 'results.html')

def pandas_list_to_array(df):
    """
    Input: dataframe of shape (x, y), containing list of length l
    Return: np.array of shape (x, l, y)
    """
    
    return np.transpose(
        np.array(df.values.tolist()),
        (0, 2, 1)
    )
    
def preprocess_inputs(df, token2int, cols=['sequence', 'structure', 'predicted_loop_type']):
    return pandas_list_to_array(
        df[cols].applymap(lambda seq: [token2int[x] for x in seq])
    )

def get_lineplot(df, x, y, width=None, height=None, title=None):
    plot = figure(width=width, height=height, title=title)
    plot.line(df[x], df[y])
    script, div = components(plot)
    lis =[]
    lis.append(script)
    lis.append(div)
    return lis

def get_barplot(x, counts, width=0.5, height=None, title=None):
    source = ColumnDataSource(data=dict(x=x, counts=counts, color=Spectral4))
    plot = figure(x_range=x, y_range=(0,9), height=300)
    plot = figure(x_range=x, height=300)
    plot.vbar(x='x', top='counts', width=0.5, color='color', legend_field="x", source=source)
    script, div = components(plot)
    lis =[]
    lis.append(script)
    lis.append(div)
    return lis