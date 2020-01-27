import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display_html



# Выводит на экран количество пропущенных в столбце значений
def na_count(_df, col_name):
    print('В столбце {} {} пропущенных значений.'.format(col_name, _df[col_name].isna().sum()))
	
# Выводит количество игр по годам
def show_games_count_by_year_plot(_df):
    games_count_by_year = _df.groupby(['year_of_release'])['year_of_release'].agg('count')
    ax = games_count_by_year.plot(figsize=(16, 6), grid=True, title='Games released by year')
    ax.set_xticks(games_count_by_year.index.values)
    ax.tick_params(axis='x', rotation=45)
    ax.set_xlabel("Year of release")
    ax.set_ylabel("Games released")
    plt.show()
	
# Выводит распределение прибыли по годам для указанных платформ
def show_platforms_distribution(_df, platforms):
    year_min, year_max = 3000, 0
    _, ax = plt.subplots(figsize=(16, 6))

    for platform_name in platforms:
        grouped_df = _df[_df['platform'] == platform_name].groupby(['year_of_release'])['total_sales'].agg(['sum'])
        grouped_df.plot(ax=ax, grid=True, legend=False, marker='o')
        year_min = min(year_min, grouped_df.index.values.min())
        year_max = max(year_max, grouped_df.index.values.max())

    ax.grid(True)
    ax.set_xlabel("Year")
    ax.set_ylabel("Totla sales")
    ax.set_title('Total sales distribution')
    ax.set_xticks(np.arange(year_min, year_max + 1, 1))
    ax.legend(platforms)
    plt.show()
	
# Выводит диаграмму рассеяния и корреляцию с отзывами критиков и пользователей
def critics_and_users_score_corr_with_total_sales(_df, platform):
    critic_score_not_na = _df['critic_score'].notna() & (_df['platform'] == platform)
    total_sales_for_critic_score = _df[critic_score_not_na]['total_sales']
    critic_score = _df[critic_score_not_na]['critic_score']

    user_score_not_na = _df['user_score'].notna() & (_df['platform'] == platform)
    total_sales_for_user_score = _df[user_score_not_na]['total_sales']
    user_score = _df[user_score_not_na]['user_score']

    info_bbox_props = dict(boxstyle='round', facecolor='white', alpha=0.2)

    fig = plt.figure(figsize=(16, 7))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    ax1.grid(True)
    ax1.set_xlim(0,25)
    ax1.set_title('{} Critics score & Total sales correlation'.format(platform))
    ax1.set_xlabel('Total sales')
    ax1.set_ylabel('Critics score')
    ax1.scatter(total_sales_for_critic_score, critic_score, s = 10)

    ax1.text(0.98, 0.98, 'Corelation: {:.2f}'.format(total_sales_for_critic_score.corr(critic_score)), 
             transform=ax1.transAxes, verticalalignment='top', horizontalalignment='right', bbox=info_bbox_props)    

    ax2.grid(True)
    ax2.set_xlim(0,25)
    ax2.set_title('{} Users score & Total sales correlation'.format(platform))
    ax2.set_xlabel('Total sales')
    ax2.set_ylabel('Users score')
    ax2.scatter(total_sales_for_user_score, user_score, s = 10)
    ax2.text(0.98, 0.98, 'Corelation: {:.2f}'.format(total_sales_for_user_score.corr(user_score)), 
             transform=ax2.transAxes, verticalalignment='top', horizontalalignment='right', bbox=info_bbox_props)

    plt.show()
	
# Выводит переданные в функцию датафреймы в одну строку
def display_side_by_side(df_arr):
    html_str=''
    for df in df_arr:
        html_str+=df.to_html()
    display_html(html_str.replace('table','table style="display:inline"'),raw=True)
	
# Выводит топ 5 результатов столбца 'param' 
def top_5_in_regions_by_param(_df, param):
    _df = _df.copy()
    regions = ['na', 'eu', 'jp']
    data_frames = []
    
    for region in regions:
        region_sales = region+'_sales'
        grouped_df = _df.groupby([param])[region_sales].agg(['sum']).sort_values(by='sum', ascending=False)[:5]
        grouped_df.columns = [region_sales]
        data_frames.append(grouped_df)
        
    display_side_by_side(data_frames)