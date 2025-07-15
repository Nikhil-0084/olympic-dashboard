import streamlit as st
import pandas  as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")

df=preprocessor.preprocess(df,region_df)


st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://clipart-library.com/2023/olympic-games-logo-clipart-xl.png")
user_menu= st.sidebar.radio(
    'Select an Option',
    ("Medal Tally","Overall Analysis","Country-Wise Analysis","Athlete-Wise Analysis")
)

#st.dataframe(df)

if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")

    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # CSS Styling
    st.markdown("""
        <style>
            .main {
                background-color: #f4f4f4;
                font-family: 'Helvetica Neue', sans-serif;
                color: #333333;
            }
            .custom-table-title {
                font-size: 32px;
                font-weight: bold;
                color: #1f77b4;
                padding: 10px 0;
            }
            .custom-description {
                font-size: 16px;
                background-color: #eaf1fb;
                padding: 15px;
                border-radius: 8px;
                margin-top: 10px;
                line-height: 1.6;
            }
        </style>
    """, unsafe_allow_html=True)

    # Dynamic Titles
    if selected_year == "Overall" and selected_country == "Overall":
        st.markdown("<div class='custom-table-title'>Overall Tally</div>", unsafe_allow_html=True)
    elif selected_year != "Overall" and selected_country == "Overall":
        st.markdown(f"<div class='custom-table-title'>Medal Tally in {selected_year} Olympics</div>",
                    unsafe_allow_html=True)
    elif selected_year == "Overall" and selected_country != "Overall":
        st.markdown(f"<div class='custom-table-title'>{selected_country} Overall Performance</div>",
                    unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='custom-table-title'>{selected_country} Performance in {selected_year} Olympics</div>",
                    unsafe_allow_html=True)

    # 📝 Explanation of the Table
    st.markdown("""
    <div class='custom-description'>
        <b>Table Explanation</b>:<br>
        - This table displays the <b>total medal count</b> based on your selected filters (year and country).<br>
        - It includes the number of <b>Gold</b>, <b>Silver</b>, and <b>Bronze</b> medals won.<br>
        - The <b>Total</b> column sums up all the medals.<br><br>
        Use the sidebar to change the year or country to analyze different medal tallies.
    </div>
    """, unsafe_allow_html=True)

    # Display the Table
    st.table(medal_tally)

if user_menu=="Overall Analysis":
    editions=df["Year"].unique().shape[0]-1
    cities=df["City"].unique().shape[0]
    sports=df["Sport"].unique().shape[0]
    events=df["Event"].unique().shape[0]
    athletes=df["Name"].unique().shape[0]
    nations=df["region"].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nations_over_time=helper.data_over_time(df,"region")
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over The years")
    st.plotly_chart(fig)
    events_over_time = helper.data_over_time(df,"Event")
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Event  over The years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, "Name")
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title("Athletes  over The years")
    st.plotly_chart(fig)
    st.title("No of Events over Time (Every Sport)")

    # Drop duplicates to count unique events per year/sport
    x = df.drop_duplicates(["Year", "Sport", "Event"])

    # Correct variable name
    heatmap_data = x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype(int)

    # Create a clean figure
    fig, ax = plt.subplots(figsize=(20, 15))

    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt="d",
        cmap="YlGnBu",  # also corrected 'YlGnB' to 'YlGnBu'
        cbar=False,
        linewidths=0.5,
        linecolor='gray',
        ax=ax
    )

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    ax.tick_params(left=False, bottom=False)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()


    st.pyplot(fig)
    st.title("Most Successful Athletes")
    sport_list=df["Sport"] .unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")
    selected_sport=st.selectbox("Select a Sport",sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == "Country-Wise Analysis":
    st.sidebar.title("Country-Wise Analysis")
    st.image("https://www.freepnglogos.com/uploads/world-map-png/world-map-this-the-most-hard-working-country-the-world-7.png")

    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select A Country", country_list)

    # Choropleth map for selected country
    st.title("Geographical View: " + selected_country)
    map_df = pd.DataFrame({
        'country': [selected_country],
        'value': [1]  # dummy value just to highlight the country
    })
    fig_map = px.choropleth(
        map_df,
        locations="country",
        locationmode="country names",
        color="value",
        color_continuous_scale=["lightblue", "blue"],
        title=f"{selected_country} Highlighted on Map"
    )
    st.plotly_chart(fig_map)

    # Medal Tally Over Years
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal", title=selected_country + " Medal Tally Over The Years")
    st.plotly_chart(fig)

    # Heatmap of Sport Performance
    st.title(selected_country + " Excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    # Top 10 Athletes
    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)
if user_menu == "Athlete-Wise Analysis":
    athlete_df = df.drop_duplicates(subset=["Name", "region"])

    # Age Distribution
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()

    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ["Overall Age", "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
        show_hist=False,
        show_rug=False
    )
    fig.update_layout(
        autosize=False,
        width=1000,
        height=688,
        plot_bgcolor='#f5f5f5',  # Plot area background
        paper_bgcolor='#e6f2ff',  # Outer area background
        font=dict(color='black', size=14),
        title=dict(text="Distribution of Age", x=0.5)
    )


    st.title("Distribution of Age")
    st.plotly_chart(fig)

    # Age Distribution per Sport
    x = []
    name = []

    famous_sports = [
        "Basketball", "Judo", "Football", "Tug-Of-War", "Athletics", "Swimming", "Badminton",
        "Sailing", "Gymnastics", "Art Competition", "Handball", "Weightlifting", "Wrestling",
        "Water Polo", "Hockey", "Rowing", "Fencing", "Shooting", "Boxing", "Taekwondo", "Cycling",
        "Diving", "Canoeing", "Tennis", "Golf", "Softball", "Archery", "Volleyball", "Table Tennis",
        "Rhythmic Gymnastics", "Rugby Sevens", "Beach Volleyball", "Triathlon", "Rugby", "Polo",
        "Ice Hockey", "Synchronized Swimming"
    ]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        age_data = temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna()

        if not age_data.empty:
            x.append(age_data)
            name.append(sport)

    if x:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=688)
        st.title("Distribution of Age wrt Sports")
        st.plotly_chart(fig)
    else:
        st.warning("No valid age data available for the selected sports.")

    # Height vs Weight Analysis

    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox("Select A Sport", sport_list)

    temp_df = helper.weight_v_height(df, selected_sport)

    # Create plot
    fig, ax = plt.subplots()

    # Set background color to light blue
    fig.patch.set_facecolor('#ADD8E6')  # light blue background for figure
    ax.set_facecolor('#ADD8E6')  # light blue background for axes

    # Create scatterplot
    sns.scatterplot(
        x=temp_df["Weight"],
        y=temp_df["Height"],
        hue=temp_df["Medal"],
        style=temp_df["Sex"],
        s=100,
        ax=ax
    )

    # Add title
    ax.set_title("Height vs Weight", fontsize=16, fontweight='bold')

    # Display plot in Streamlit
    st.pyplot(fig)

    st.title("Men Vs Women Partition Over The Year")

    final = helper.men_vs_women(df)

    # Create line chart
    fig = px.line(final, x="Year", y=["Male", "Female"])

    # Set background colors
    fig.update_layout(
        plot_bgcolor='#ADD8E6',  # Background color of the plot area
        paper_bgcolor='#ADD8E6',  # Background color of the entire figure
        title_font=dict(size=20, color='black')
    )

    # Display chart
    st.plotly_chart(fig)

