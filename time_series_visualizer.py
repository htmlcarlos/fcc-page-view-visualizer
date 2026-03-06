import matplotlib.pyplot as plt # pyright: ignore[reportMissingModuleSource]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import seaborn as sns # pyright: ignore[reportMissingModuleSource]
import warnings
import pandas.plotting # pyright: ignore[reportMissingModuleSource]

# 0. Silenciar advertencias de Seaborn/Matplotlib para una terminal limpia
warnings.simplefilter("ignore")

# 1. Importar datos
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# 2. Limpiar datos
# Filtramos el top y bottom 2.5%. Mantenemos solo la columna 'value' para el test_count.
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    df_line = df.copy()
    
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Preparar datos
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    
    # Agrupar y pivotar
    df_pivot = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Reordenar meses
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    df_pivot = df_pivot.reindex(columns=months)

    # Dibujar usando el objeto Axes para mayor control
    ax = df_pivot.plot(kind='bar', figsize=(10, 8))
    fig = ax.get_figure()

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend()

    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Preparar datos
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Configurar el lienzo
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    # Gráfico 1: Year-wise
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Gráfico 2: Month-wise
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, order=month_order)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig


    # ----------------------------------------------------------------------
# "Deja que los warnings ladren, Sancho;
#  señal de que nuestro código cabalga."
# 
# — Crónicas del programador errante (Aportación de la IA aliada) ._.7
#   gitbub: htmlcarlos
# ----------------------------------------------------------------------