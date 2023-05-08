
import streamlit as  st
import pandas as pd
import preprocessor
import help
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


df= pd.read_csv('athlete_events.csv')
df1=pd.read_csv('noc_regions.csv')

df= preprocessor.preprocess(df,df1)
st.sidebar.title('Olympic Analysis')
user_menu = st.sidebar.radio(
    'select an option',
    ('Medal Tally','overal analysis','country-wise analysis')
)


if user_menu== 'Medal Tally':
    st.sidebar.header("Medal Tally")
    year,country= help.country_year_list(df)
    selected_year=st.sidebar.selectbox('select year',year)
    selected_country=st.sidebar.selectbox('select country', country)

    medal_tally= help.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('overall tally')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('medal tally in'  +  str(selected_year))

    st.table(medal_tally)

if user_menu == 'overal analysis':
    editions=df['Year'].unique().shape[0] - 1  # no. of edition
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 =st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nation_over_view = help.participating_nations_over_time(df)
    fig = px.line(nation_over_view, x='Edition', y='No of countries')
    st.plotly_chart(fig)

    st.title("No of Events over time(Every Sport")
    fig,ax =plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot= True)

    st.pyplot(fig)




    st.title("Most successful Athletes")

    x= help.most_successful(df,'Overall')
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    country_df = help.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.plotly_chart(fig)

