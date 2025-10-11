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
# Set wide layout
st.set_page_config(layout="wide")

# Custom full-page background color using CSS
st.markdown("""
    <style>
        /* Entire page background */
        .stApp {
            background-color: #f0f8ff; /* Light blue */
        }

        /* Optional: Style sidebar too */
        section[data-testid="stSidebar"] {
            background-color: #dbeeff; /* Slightly darker blue for contrast */
        }

        /* Optional: Adjust text color or other elements */
        .custom-table-title {
            font-size: 32px;
            font-weight: bold;
            color: #1f77b4;
            padding: 10px 0;
            animation: fadeInDown 1.5s ease forwards;
        }

        .custom-description {
            font-size: 16px;
            background-color: #eaf1fb;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            line-height: 1.6;
            animation: fadeIn 2s ease forwards;
        }

        @keyframes fadeInDown {
            from {opacity: 0; transform: translateY(-20px);}
            to {opacity: 1; transform: translateY(0);}
        }
    </style>
""", unsafe_allow_html=True)


import streamlit as st
from datetime import datetime

# Sidebar Title
st.sidebar.title("Olympics Analysis")

# Animated Olympic Logo (GIF)
st.sidebar.image("https://drawnjournalism.com/wp-content/uploads/2021/07/di00726-00-800px-25-7-square2-anim-c-olympic-rings-keeping-distance-frits-ahlefeldt.gif?w=640", use_container_width=True)

# Sidebar Menu
user_menu = st.sidebar.radio(
    'Select an Option',
    (
        "Medal Tally",
        "Overall Analysis",
        "Country-Wise Analysis",
        "Athlete-Wise Analysis",
        "Olympic Records",
        "Olympic Timeline",
        "Unexpected Performance",
        "Medal Predictor"

    )
)

# Countdown to next Olympics
next_olympics = datetime(2028, 7, 14)
now = datetime.now()
time_left = next_olympics - now

days = time_left.days
hours, remainder = divmod(time_left.seconds, 3600)
minutes, seconds = divmod(remainder, 60)

st.sidebar.markdown("### 🕒 Countdown to LA 2028 Olympics")
st.sidebar.markdown(f"**{days}** days, **{hours}** hours, **{minutes}** minutes")






#st.dataframe(df)

import streamlit as st
import pandas as pd
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards

# Assuming helper functions and df are already imported

import streamlit as st
import pandas as pd
import altair as alt

# Assuming helper functions and df are already imported

# --- Page setup for wide layout and background ---
st.set_page_config(layout="wide")

if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")

    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if "Total" not in medal_tally.columns:
        medal_tally["Total"] = medal_tally[["Gold", "Silver", "Bronze"]].sum(axis=1)

    # --- Custom CSS: background color + animation ---
    st.markdown("""
        <style>
            body {
                background-color: #f0f8ff; /* light blue background */
            }
            .main {
                background-color: #f0f8ff;
            }
            .custom-table-title {
                font-size: 32px;
                font-weight: bold;
                color: #1f77b4;
                padding: 10px 0;
                animation: fadeInDown 1.5s ease forwards;
            }
            .custom-description {
                font-size: 16px;
                background-color: #eaf1fb;
                padding: 15px;
                border-radius: 8px;
                margin-top: 10px;
                line-height: 1.6;
                animation: fadeIn 2s ease forwards;
            }
            @keyframes fadeIn {
                from {opacity: 0;}
                to {opacity: 1;}
            }
            @keyframes fadeInDown {
                from {opacity: 0; transform: translateY(-20px);}
                to {opacity: 1; transform: translateY(0);}
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Title based on selection ---
    if selected_year == "Overall" and selected_country == "Overall":
        st.markdown("<div class='custom-table-title'>Overall Tally</div>", unsafe_allow_html=True)
    elif selected_year != "Overall" and selected_country == "Overall":
        st.markdown(f"<div class='custom-table-title'>Medal Tally in {selected_year} Olympics</div>", unsafe_allow_html=True)
    elif selected_year == "Overall" and selected_country != "Overall":
        st.markdown(f"<div class='custom-table-title'>{selected_country} Overall Performance</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='custom-table-title'>{selected_country} Performance in {selected_year} Olympics</div>", unsafe_allow_html=True)

    # --- Description box ---
    st.markdown("""
        <div class='custom-description'>
            <b>Table Explanation</b>:<br>
            - This table displays the <b>total medal count</b> based on your selected filters (year and country).<br>
            - It includes the number of <b>Gold</b>, <b>Silver</b>, and <b>Bronze</b> medals won.<br>
            - The <b>Total</b> column sums up all the medals.<br><br>
            Use the sidebar to change the year or country to analyze different medal tallies.
        </div>
    """, unsafe_allow_html=True)

    # --- Display the medal tally table with zoom/scroll ---
    st.dataframe(medal_tally, use_container_width=True)

    # --- CSV download ---
    if not medal_tally.empty:
        csv = medal_tally.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Medal Tally as CSV",
            data=csv,
            file_name='medal_tally.csv',
            mime='text/csv'
        )

    # --- Metric summary counters ---
    if not medal_tally.empty:
        total_gold = medal_tally["Gold"].sum()
        total_silver = medal_tally["Silver"].sum()
        total_bronze = medal_tally["Bronze"].sum()
        total_medals = medal_tally["Total"].sum()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="🥇 Total Gold", value=total_gold)
        with col2:
            st.metric(label="🥈 Total Silver", value=total_silver)
        with col3:
            st.metric(label="🥉 Total Bronze", value=total_bronze)
        with col4:
            st.metric(label="🏅 Total Medals", value=total_medals)

    # --- Altair interactive bar chart with hover ---
    if not medal_tally.empty:
        chart_data = medal_tally.melt(
            id_vars=medal_tally.columns[0],
            value_vars=["Gold", "Silver", "Bronze"]
        )

        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X(f'{medal_tally.columns[0]}:N', sort='-y', title="Country"),
            y=alt.Y('value:Q', title="Medal Count"),
            color=alt.Color('variable:N', title="Medal Type"),
            tooltip=[
                alt.Tooltip(f'{medal_tally.columns[0]}:N', title="Country"),
                alt.Tooltip('variable:N', title="Medal Type"),
                alt.Tooltip('value:Q', title="Count")
            ]
        ).properties(
            width=700,
            height=400,
            title="Medal Distribution by Type"
        ).interactive()

        st.altair_chart(chart, use_container_width=True)


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Streamlit config
st.set_page_config(layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
        .section-box {
            background-color: #eaf6fb;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            animation: fadeIn 1.2s ease-in-out;
        }
        .section-title {
            font-size: 28px;
            color: #0077b6;
            font-weight: 600;
            padding-bottom: 10px;
        }
        .metric-box .element-container {
            background-color: #ffffff !important;
            border-radius: 8px;
            padding: 10px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Main Section ----------
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
        .section-box {
            background-color: #eaf6fb;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            animation: fadeIn 1.2s ease-in-out;
        }
        .section-title {
            font-size: 28px;
            color: #0077b6;
            font-weight: 600;
            padding-bottom: 10px;
        }
        .metric-box .element-container {
            background-color: #ffffff !important;
            border-radius: 8px;
            padding: 10px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

if user_menu == "Overall Analysis":

    editions = df["Year"].nunique() - 1
    cities = df["City"].nunique()
    sports = df["Sport"].nunique()
    events = df["Event"].nunique()
    athletes = df["Name"].nunique()
    nations = df["region"].nunique()

    # Top Statistics Section
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Top Statistics</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Editions", editions)
    with col2:
        st.metric("Hosts", cities)
    with col3:
        st.metric("Sports", sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Events", events)
    with col2:
        st.metric("Nations", nations)
    with col3:
        st.metric("Athletes", athletes)

    st.markdown("</div>", unsafe_allow_html=True)

    # Participating Nations Over the Years Line Chart
    nations_over_time = helper.data_over_time(df, "region")
    fig = px.line(nations_over_time, x="Edition", y="region", title="")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Participating Nations Over the Years</div>", unsafe_allow_html=True)
    st.plotly_chart(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # Events Over the Years Line Chart
    events_over_time = helper.data_over_time(df, "Event")
    fig = px.line(events_over_time, x="Edition", y="Event", title="")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Events Over the Years</div>", unsafe_allow_html=True)
    st.plotly_chart(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # Athletes Over the Years Line Chart
    athletes_over_time = helper.data_over_time(df, "Name")
    fig = px.line(athletes_over_time, x="Edition", y="Name", title="")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Athletes Over the Years</div>", unsafe_allow_html=True)
    st.plotly_chart(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # Heatmap and Top Sports Tabs
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Sports & Events Analysis</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Events Heatmap", "🏅 Top Sports by Medal Count"])

    with tab1:
        x = df.drop_duplicates(["Year", "Sport", "Event"])
        heatmap_data = x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype(int)

        fig, ax = plt.subplots(figsize=(20, 15))
        sns.heatmap(
            heatmap_data,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            linewidths=0.5,
            linecolor='gray',
            ax=ax
        )
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='y', labelsize=12)
        ax.set_title("Events per Sport (by Year)", fontsize=18, color="#0077b6", pad=20)
        sns.despine()
        plt.tight_layout()

        st.pyplot(fig)

    with tab2:
        top_sports = df[df['Medal'].notnull()].groupby('Sport').count()['Medal'].sort_values(ascending=False).head(10).reset_index()
        fig2 = px.bar(top_sports, x="Sport", y="Medal", title="Top 10 Sports by Total Medals", text_auto=True)
        st.plotly_chart(fig2)

    st.markdown("</div>", unsafe_allow_html=True)

    # Most Successful Athletes Section
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Most Successful Athletes</div>", unsafe_allow_html=True)

    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Select a Sport", sport_list)

    x = helper.most_successful(df, selected_sport)
    st.dataframe(x, use_container_width=True)

    # Download button for most successful athletes table
    csv = x.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Table as CSV",
        data=csv,
        file_name="most_successful_athletes.csv",
        mime="text/csv"
    )

    st.markdown("</div>", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

def country_to_flag(country_name):
    flags = {
        'USA': '🇺🇸',
        'India': '🇮🇳',
        'China': '🇨🇳',
        'Russia': '🇷🇺',
        'Germany': '🇩🇪',
        'Canada': '🇨🇦',
        # Add more as needed
    }
    return flags.get(country_name, '')

if user_menu == "Country-Wise Analysis":
    st.sidebar.title("Country-Wise Analysis")
    st.image("https://www.freepnglogos.com/uploads/world-map-png/world-map-this-the-most-hard-working-country-the-world-7.png")

    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select A Country", country_list)
    flag = country_to_flag(selected_country)
    st.sidebar.markdown(f"### {flag} {selected_country}")

    st.markdown(f"<h2 style='color:#005b96;'>Geographical View: {selected_country}</h2>", unsafe_allow_html=True)

    medal_count = df[df['region'] == selected_country]['Medal'].count()
    map_df = pd.DataFrame({
        'country': [selected_country],
        'medal_count': [medal_count]
    })

    fig_map = px.choropleth(
        map_df,
        locations="country",
        locationmode="country names",
        color="medal_count",
        color_continuous_scale=px.colors.sequential.Blues,
        title=f"{selected_country} Total Medals: {medal_count}",
        hover_data={'medal_count': True, 'country': False}
    )
    st.plotly_chart(fig_map)

    # Summary Box with key stats
    total_medals = df[(df['region'] == selected_country) & (df['Medal'].notna())].shape[0]
    gold_medals = df[(df['region'] == selected_country) & (df['Medal'] == 'Gold')].shape[0]
    first_year = df[df['region'] == selected_country]['Year'].min()
    best_year = df[df['region'] == selected_country].groupby('Year')['Medal'].count().idxmax()

    st.markdown(f"""
    <div style="background-color:#eaf1fb; padding:15px; border-radius:10px; margin-bottom:20px;">
        <h3 style="color:#1f77b4;">Key Statistics for {selected_country}</h3>
        <ul>
            <li><b>Total Medals:</b> {total_medals}</li>
            <li><b>Gold Medals:</b> {gold_medals}</li>
            <li><b>First Participation Year:</b> {first_year}</li>
            <li><b>Best Year (most medals):</b> {best_year}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal", title=selected_country + " Medal Tally Over The Years")
    st.plotly_chart(fig)

    sports_list = df[df['region'] == selected_country]['Sport'].unique().tolist()
    sports_list.sort()
    selected_sports = st.multiselect("Filter Sports", sports_list, default=sports_list)

    filtered_df = df[(df['region'] == selected_country) & (df['Sport'].isin(selected_sports))]

    st.markdown(f"<h2 style='color:#005b96;'> {selected_country} Excels in the following sports </h2>", unsafe_allow_html=True)
    pt = helper.country_event_heatmap(filtered_df, selected_country)  # Assuming this returns a pivot table

    # Plotly heatmap with hover
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=pt.values,
        x=pt.columns.astype(str),
        y=pt.index,
        colorscale='YlGnBu',
        hoverongaps=False,
        hovertemplate='Sport: %{y}<br>Year: %{x}<br>Events: %{z}<extra></extra>'
    ))
    fig_heatmap.update_layout(
        xaxis_title='Year',
        yaxis_title='Sport',
        autosize=False,
        width=900,
        height=600,
        margin=dict(l=100, r=50, t=50, b=100)
    )
    st.plotly_chart(fig_heatmap)

    st.markdown(f"<h2 style='color:#005b96;'>Top 10 athletes of {selected_country}</h2>", unsafe_allow_html=True)
    top10_df = helper.most_successful_countrywise(filtered_df, selected_country)
    st.table(top10_df)

    csv = top10_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Top Athletes as CSV",
        data=csv,
        file_name=f'top_athletes_{selected_country}.csv',
        mime='text/csv',
    )




if user_menu == "Athlete-Wise Analysis":
    athlete_df = df.drop_duplicates(subset=["Name", "region"])


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



    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox("Select A Sport", sport_list)

    temp_df = helper.weight_v_height(df, selected_sport)


    fig, ax = plt.subplots()


    fig.patch.set_facecolor('#ADD8E6')
    ax.set_facecolor('#ADD8E6')

    # Create scatterplot
    sns.scatterplot(
        x=temp_df["Weight"],
        y=temp_df["Height"],
        hue=temp_df["Medal"],
        style=temp_df["Sex"],
        s=100,
        ax=ax
    )


    ax.set_title("Height vs Weight", fontsize=16, fontweight='bold')


    st.pyplot(fig)

    st.title("Men Vs Women Partition Over The Year")

    final = helper.men_vs_women(df)


    fig = px.line(final, x="Year", y=["Male", "Female"])


    fig.update_layout(
        plot_bgcolor='#ADD8E6',  # Background color of the plot area
        paper_bgcolor='#ADD8E6',  # Background color of the entire figure

        title_font=dict(size=20, color='black')
    )


    st.plotly_chart(fig)

if user_menu == "Olympic Records":
    st.title("🏆 Olympic Records & Milestones")

    st.markdown("### 🧒 Youngest Medalist")
    youngest = df[df["Medal"].notnull()].sort_values("Age").head(1)
    st.dataframe(youngest[["Name", "Age", "Sport", "Event", "Year", "Medal", "region"]])

    st.markdown("### 👴 Oldest Medalist")
    oldest = df[df["Medal"].notnull()].sort_values("Age", ascending=False).head(1)
    st.dataframe(oldest[["Name", "Age", "Sport", "Event", "Year", "Medal", "region"]])

    st.markdown("### 🥇 Most Decorated Athletes")
    top_athletes = df[df["Medal"].notnull()].groupby(["Name", "region"]).size().reset_index(name='Total Medals')
    top_athletes = top_athletes.sort_values("Total Medals", ascending=False).head(10)
    st.dataframe(top_athletes)

    st.markdown("### 🌍 First-Time Medal Winning Countries")
    df_medal = df[df["Medal"].notnull()]
    first_medal = df_medal.groupby("region")["Year"].min().reset_index()
    first_medal = first_medal.sort_values("Year")
    st.dataframe(first_medal)

    st.markdown("### 📈 Highest Medal Haul in a Single Edition (by an Athlete)")
    df_medals = df[df["Medal"].notnull()]
    haul = df_medals.groupby(["Name", "Year", "region"]).size().reset_index(name="Medals Won")
    top_haul = haul.sort_values("Medals Won", ascending=False).head(10)
    st.dataframe(top_haul)

if user_menu == "Olympic Timeline":
    st.title("📅 Olympic Timeline: Host Cities & Highlights")

    # Step 1: Get unique Olympic editions
    timeline_df = df.drop_duplicates(subset=["Year", "City", "region"]).sort_values("Year")

    # Clean and ensure no missing data
    timeline_df = timeline_df.dropna(subset=["Year", "City", "region"])
    timeline_df["Year"] = timeline_df["Year"].astype(int)

    st.markdown("### 🏛️ Host Cities by Year")
    st.dataframe(timeline_df[["Year", "City", "region"]].reset_index(drop=True))

    st.markdown("### 📈 Timeline of Olympic Games")

    # Create a tooltip label
    timeline_df["Host_Info"] = timeline_df["Year"].astype(str) + " - " + timeline_df["City"] + " (" + timeline_df["region"] + ")"

    import plotly.express as px

    fig = px.scatter(
        timeline_df,
        x="Year",
        y="region",
        color="region",
        hover_name="Host_Info",
        size=[10]*len(timeline_df),  # Fixed bubble size
        title="Olympic Games: Host Cities Over the Years"
    )

    fig.update_layout(
        height=600,
        showlegend=False,
        paper_bgcolor="#eaf6fb",
        plot_bgcolor="#ffffff",
        xaxis_title="Year",
        yaxis_title="Host Country / Region"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        <div style="background-color:#eaf6fb; padding:15px; border-radius:10px;">
        💡 <b>Tip:</b> Hover over the dots to see which city hosted the Olympics in which year.
        </div>
    """, unsafe_allow_html=True)

if user_menu == "Unexpected Performance":
    st.title("🎯 Unexpected Performances at the Olympics")

    st.markdown("""
    <div style="background-color:#eaf6fb; padding:15px; border-radius:10px;">
        🌟 Some athletes and countries have stunned the world with their outstanding performances, 
        while others, once considered strong contenders, have delivered underwhelming results.
    </div>
    """, unsafe_allow_html=True)

    st.header("🚀 Surprise Medal Winners")
    underdog_data = pd.DataFrame({
        "Year": [2012, 2016, 2020],
        "Country": ["Grenada", "Kosovo", "Fiji"],
        "Athlete": ["Kirani James", "Majlinda Kelmendi", "Fiji Rugby Team"],
        "Medal": ["Gold", "Gold", "Gold"],
        "Sport": ["Athletics", "Judo", "Rugby Sevens"]
    })

    fig1 = px.bar(
        underdog_data,
        x="Country",
        y="Year",
        color="Sport",
        hover_data=["Athlete", "Medal"],
        title="🏅 Underdog Countries That Won Gold"
    )
    fig1.update_layout(
        paper_bgcolor="#eaf6fb",
        plot_bgcolor="#ffffff"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 😢 Major Letdowns & Heartbreaks")

    letdown_data = pd.DataFrame({
        "Year": [2016, 2020, 2020],
        "Country": ["USA", "India", "Japan"],
        "Athlete": ["Allyson Felix (Relay team DQ)", "Vinesh Phogat", "Naomi Osaka"],
        "Sport": ["Athletics", "Wrestling", "Tennis"],
        "Note": [
            "Disqualified in relay event despite being medal favorite.",
            "Shocking early exit after strong performance in qualifiers.",
            "Lost early in front of home crowd under pressure."
        ]
    })

    fig2 = px.scatter(
        letdown_data,
        x="Year",
        y="Country",
        color="Sport",
        size=[20, 30, 40],
        hover_data=["Athlete", "Note"],
        title="💔 Heartbreaking Moments from Top Athletes"
    )
    fig2.update_layout(
        paper_bgcolor="#eaf6fb",
        plot_bgcolor="#ffffff"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
        <div style="background-color:#fce4e4; padding:15px; border-radius:10px;">
            💡 <b>Did You Know?</b> Fiji's win in Rugby Sevens in 2016 was the country's first Olympic medal ever, turning them into national heroes overnight.
        </div>
        """, unsafe_allow_html=True)

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import streamlit as st
import plotly.express as px

# -----------------------------
# Olympic Medal Data
# -----------------------------
data = {
    'Country': (
        ['USA']*6 + ['China']*6 + ['India']*6 + ['Kenya']*6 + ['Russia']*6 +
        ['Japan']*6 + ['Germany']*6 + ['Australia']*6 + ['UK']*6 + ['Brazil']*6
    ),
    'Year': [2000, 2004, 2008, 2012, 2016, 2020]*10,
    'Medals': [
        93, 101, 110, 104, 121, 113,       # USA
        58, 63, 100, 88, 70, 88,           # China
        1, 1, 3, 6, 2, 7,                  # India
        7, 8, 14, 11, 13, 10,              # Kenya
        88, 90, 72, 82, 56, 71,            # Russia
        18, 37, 25, 38, 41, 58,            # Japan
        56, 49, 41, 44, 42, 37,            # Germany
        58, 50, 46, 35, 29, 46,            # Australia
        28, 30, 47, 65, 67, 65,            # UK
        12, 10, 15, 17, 19, 21             # Brazil
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("🏆 Olympic Insights")
user_menu = st.sidebar.radio(
    "Navigate to:",
    ["Medal Predictor"]
)

# -----------------------------
# Medal Predictor Section
# -----------------------------
if user_menu == "Medal Predictor":
    st.title("🌍 Olympic Medal Predictions")
    st.markdown("Predicted medal counts based on historical data using Linear Regression.")

    # Sidebar controls for this page
    st.sidebar.subheader("⚙️ Prediction Settings")
    year = st.sidebar.number_input("Predict for Year:", min_value=2024, max_value=2100, value=2028, step=4)
    view_option = st.sidebar.radio("Select View:", ["All Countries", "Specific Country"])

    predictions = []
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country]
        if len(country_data['Year'].unique()) >= 2:
            X = country_data[['Year']]
            y = country_data['Medals']
            model = LinearRegression()
            model.fit(X, y)
            pred = model.predict(np.array([[year]]))
            predictions.append({
                'Country': country,
                'Predicted Medals': max(0, int(pred[0]))
            })

    pred_df = pd.DataFrame(predictions).sort_values(by='Predicted Medals', ascending=False).reset_index(drop=True)

    # Filter if user selects a specific country
    if view_option == "Specific Country":
        selected_country = st.sidebar.selectbox("Choose Country:", df['Country'].unique())
        pred_df = pred_df[pred_df['Country'] == selected_country]

    # Display predictions table
    st.markdown(f"### 🏅 Predicted Medal Counts ({year})")
    st.dataframe(pred_df)

    # Bar chart for top 10 countries
    if view_option == "All Countries":
        st.markdown("### 🥇 Top 10 Predicted Performers")
        st.bar_chart(pred_df.head(10).set_index('Country'))

    # -----------------------------
    # Map Visualization
    # -----------------------------
    st.markdown("### 🗺️ Predicted Medals on World Map")
    iso_codes = {
        'USA':'USA', 'China':'CHN', 'India':'IND', 'Kenya':'KEN', 'Russia':'RUS',
        'Japan':'JPN', 'Germany':'DEU', 'Australia':'AUS', 'UK':'GBR', 'Brazil':'BRA'
    }
    pred_df['ISO_Code'] = pred_df['Country'].map(iso_codes)

    fig = px.choropleth(
        pred_df,
        locations='ISO_Code',
        color='Predicted Medals',
        hover_name='Country',
        color_continuous_scale='Viridis',
        title=f'Olympic Medal Predictions ({year})'
    )
    st.plotly_chart(fig)





