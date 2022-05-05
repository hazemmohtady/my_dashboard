#!/usr/bin/env python
# coding: utf-8

# # Project

# In[1]:


import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input,Output,State



# In[2]:


def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    
    if 'M' in x:
        return float(x.replace('M', ''))/ 1000
        
    if 'B' in x:
        return float(x.replace('B', ''))
   


# In[3]:


df=pd.read_excel('forbes-2021.xlsx')
df = df.replace([',','\$'],'', regex=True) 
df.drop(columns=['Rank','Year','Assets'],inplace=True)
df['Market Value']=df['Market Value'].apply(value_to_float)
df['Profit']=df['Profit'].apply(value_to_float)
df['Sales']=df['Sales'].apply(value_to_float)
df.loc[~df['Country'].isin(['United States', 'China', 'Japan','United Kingdom','Hong Kong','South Korea','Germany']),'Country']='other'
df.head()


# In[4]:


df.groupby('Country', as_index=False).count()


# In[ ]:





# In[5]:


fig1=px.histogram(df.sort_values(by='Sales',ascending=False).head(10),x='Name',y='Sales',color='Country',hover_data=df.columns,
            title='Top 10 companies',labels={'Sales':'Sales (billions)'})

fig1.update_layout({'paper_bgcolor':'#C0C0C0'})




fig2=px.scatter(df,x='Sales',y='Profit',
           color='Country',
           size='Market Value',
           size_max=60, #size-max to increase size of circles
          hover_name='Name',
          log_x=True, #log-x to take the log of x instead of using log of pandas first to make data transformation
          title='Sales to Profit',
           labels={'Sales':'Sales (billions)', 'Profit':'Profit (billions)'}
          
          )
fig2.update_layout({'paper_bgcolor':'#C0C0C0'})

fig3=px.pie(df.groupby('Country', as_index=False).count(), values='Name', names='Country', title='Countries percentage')
fig3.update_layout({'paper_bgcolor':'#C0C0C0'})


contList=[{'label':'All','value':'All'}]
for i in df['Country'].unique():
    contList.append({'label':i,'value':i})
contList



# In[6]:


#cssPath='C:\Users\hazem\Desktop\style.css'
app=dash.Dash()
app.layout=html.Div([
    html.H1('Forbes Top 2000 Companies 2021',style={'textAlign':'center' , 'color': 'blue'}),
    html.Div([
        html.Div([
              dcc.Graph(figure=fig1)
       ],style={'width':'45%','margin':'auto','background-color':'#C0C0C0'})
     ,
        html.Div([
        dcc.Dropdown(
        id='demo-dropdown',
        options=contList,
        value='All'
    ),
            
        dcc.Graph(id='myfig',figure=fig2),
    html.Div(id='dd-output-container')
],style={'width':'45%','margin':'auto','background-color':'#C0C0C0'})
    ],style={'display':'flex','align-items':'center','justify-content':'center'}) ,
    
    
    html.Div([
        dcc.Graph(figure=fig3)
    ],style={'width':'50%','margin':'auto','background-color':'#C0C0C0'})
       
],style={'height':'100%','background-color':'#C0C0C0'})


# In[7]:


@app.callback(
    Output(component_id='myfig',component_property='figure'),
    Input(component_id='demo-dropdown',component_property='value')
    
)
def myFunc(cont):
    if cont=='All':
        fig=px.scatter(df,x='Sales',y='Profit',
           color='Country',
           size='Market Value',
           size_max=60, #size-max to increase size of circles
          hover_name='Name',
          log_x=True, #log-x to take the log of x instead of using log of pandas first to make data transformation
          title='Sales to Profit',
           labels={'Sales':'Sales (billions)', 'Profit':'Profit (billions)'}
          
          )
        
    else:
        fig=px.scatter(df[df['Country']==cont],x='Sales',y='Profit',
           color='Country',
           size='Market Value',
           size_max=60, #size-max to increase size of circles
          hover_name='Name',
          log_x=True, #log-x to take the log of x instead of using log of pandas first to make data transformation
          title='Countries portions',
           labels={'Sales':'Sales (billions)', 'Profit':'Profit (billions)'}
          
          )
    
        
    
    fig.update_layout({'paper_bgcolor':'#C0C0C0'})
    
    
    return fig
    
    



# In[ ]:


app.run_server()


# In[ ]:





# In[ ]:





# In[ ]:






# In[ ]:





# In[ ]:





# In[ ]:




