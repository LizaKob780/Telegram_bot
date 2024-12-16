import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_table

# Данные для графика
df = pd.DataFrame({
    'Product': ['Диван', 'Кресло', 'Стол', 'Стул'],
    'Price': [25000, 15000, 10000, 5000],
    'Quantity': [10, 20, 30, 40]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    # Заголовок
    html.H1("Dashboard для магазина мебели"),

    # График количества продаж
    dcc.Graph(id='sales-graph',
              figure=px.bar(df, x='Product', y='Quantity', title='Количество проданных товаров')),

    # Таблица с корзиной пользователя
    html.H2("Корзина пользователя"),
    dcc.Dropdown(id='user-dropdown',
                 options=[{'label': user, 'value': user} for user in ['User1', 'User2']],
                 value='User1'),
    dash_table.DataTable(id='cart-table')
])


@app.callback(Output('cart-table', 'data'),
              Input('user-dropdown', 'value'))
def update_table(user):
    # Здесь должна быть логика получения данных о корзине пользователя
    df_user = pd.DataFrame({
        'Product': ['Диван', 'Кресло'],
        'Price': [25000, 15000],
        'Quantity': [1, 2]
    })
    return df_user.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
