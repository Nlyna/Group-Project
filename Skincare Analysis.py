import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv('skincaresurvey.csv')  # Replace with your file path
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
logo = Image.open('skincarelogo.png')

# Layout for header
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.markdown("""
    <style>
    img {
        max-width: 100%;
        height: auto;
    }
    </style>
""", unsafe_allow_html=True)
    st.image(logo, width=150)

html_title = """
    <style>
    .title-test {
    font-weight: bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Skincare Business Insights Dashboards</h1></center>"""

with col2:
    st.markdown(html_title, unsafe_allow_html=True)

# Sidebar for dashboard selection
dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    ["Consumer Behavior & Preferences", "Target Market", "Technology"]
)

# Dynamic subtitle based on selected dashboard
subtitle = dashboard
st.markdown(f"<h2 style='text-align:center;'>{subtitle}</h2>", unsafe_allow_html=True)

# Standardized subheader style
subheader_style = """
    <style>
    .subheader {
        text-align: center;
        font-size: 24px;
        font-weight: normal;
        margin-top: 30px;
    }
    </style>
"""

st.markdown(subheader_style, unsafe_allow_html=True)

# Row A - Survey Outcome
if dashboard == "Consumer Behavior & Preferences":
    # Survey Outcome Section
    st.markdown('<h3 style="text-align: center; margin-bottom: 20px;">Survey Outcome</h3>', unsafe_allow_html=True)

    # Add metric boxes with custom CSS
    custom_css = """
    <style>
    .metric-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 15px;
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px;
        height: 150px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 20px;
        color: #555;
        text-align: center;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Create metric boxes
    col3, col4, col5, col6 = st.columns(4)
    with col3:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-value">7,354</div>
            <div class="metric-label">Number of Respondents</div>
        </div>
        """, unsafe_allow_html=True)

    # Count "Yes" in the specified column for Skincare Importance
    agree_count = data['Do you agree that skincare is important?'].str.lower().value_counts().get('yes', 0)

    with col4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{agree_count}</div>
            <div class="metric-label">Agree on Skincare Importance</div>
        </div>
        """, unsafe_allow_html=True)

    # Count "Yes" in the specified column for Willingness to Try New Products
    try_new_count = data['How willing are you to try different skin care products?'].str.lower().value_counts().get('willing', 0)

    with col5:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{try_new_count}</div>
            <div class="metric-label">Are Willing to Try New Products</div>
        </div>
        """, unsafe_allow_html=True)

    # Count "Yes" in the specified column for Desire for Skincare Knowledge
    knowledge_count = data['I want to gain knowledge of skincare regime in easy and understandable way.'].str.lower().value_counts().get('yes', 0)

    with col6:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{knowledge_count}</div>
            <div class="metric-label">Have the Desire for Skincare Knowledge</div>
        </div>
        """, unsafe_allow_html=True)

    # Row B - Consumer Behavior & Preferences
    if dashboard == "Consumer Behavior & Preferences":
        col3, col4 = st.columns([0.5, 0.5])

        # Preferred Type of Ingredients
        with col3:
            st.markdown('<h3 class="subheader">Preferred Type of Ingredients</h3>', unsafe_allow_html=True)
            ingredient_counts = data['Preferred Type of Ingredients'].value_counts()
            fig_ingredients = px.bar(
                ingredient_counts,
                x=ingredient_counts.index,
                y=ingredient_counts.values,
                labels={'x': 'Ingredient Type', 'y': 'Count'},
                title="Preferred Type of Ingredients",
                color=ingredient_counts.index.astype(str), 
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            st.plotly_chart(fig_ingredients)

        # Product Selection Criteria
        with col4:
            st.markdown('<h3 class="subheader">How do you choose your products?</h3>', unsafe_allow_html=True)
            product_choice_text = " ".join(data['How do you choose your products?'].dropna().astype(str))
            product_choice_wordcloud = WordCloud(
                width=800, 
                height=500, 
                background_color='black',
                colormap='cool'
            ).generate(product_choice_text)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(product_choice_wordcloud, interpolation='bilinear')
            ax.axis("off")  # Turn off axes
            st.pyplot(fig)

    # Monthly Spending on Skincare
        st.markdown('<h3 class="subheader">Average Monthly Spending on Skincare</h3>', unsafe_allow_html=True)
        spending = data['Average monthly spending on skincare products'].value_counts()
        fig_spending = px.bar(
            spending,
            x=spending.index,
            y=spending.values,
            labels={'x': 'Spending Range', 'y': 'Count'},
            title="Average Monthly Spending on Skincare",
            color=spending.index.astype(str), 
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig_spending)

# 2. Target Market Dashboard
elif dashboard == "Target Market":

# Row A - Income Insights

    # Income Insights Section
    st.markdown('<h3 class="subheader">Mean Income by State</h3>', unsafe_allow_html=True)

    # Load the income dataset
    income_data = pd.read_csv("hh_income_state.csv")  # Replace with your actual file path
    
    # Calculate the mean income by state
    mean_income = income_data.groupby('state')['income_mean'].mean().reset_index()

    # Plot horizontal bar chart
    fig_income = px.bar(
        mean_income,
        x='income_mean',
        y='state',
        orientation='h',
        title="Mean Income by State",
        labels={'income_mean': 'Mean Income', 'state': 'State'},
        color='income_mean',
        color_continuous_scale='Plasma'
    )

    # Adjust layout for better visuals
    fig_income.update_layout(
        xaxis_title="Mean Income",
        yaxis_title="State",
        coloraxis_colorbar=dict(title="Income"),
        template="plotly_white"
    )

    # Display chart in Streamlit
    st.plotly_chart(fig_income)

# Row B - Target Market Insights
    col3, col4 = st.columns([0.5, 0.5])
    # Gender Distribution
    with col3:
        st.markdown('<h3 class="subheader">Gender</h3>', unsafe_allow_html=True)
        gender = data['Gender'].value_counts()
        fig_gender = px.pie(
            names=gender.index,
            values=gender.values,
            color=gender.index.astype(str),
            color_discrete_sequence=px.colors.qualitative.Pastel1,
            title="Gender"
        )
        st.plotly_chart(fig_gender)

    # Age Distribution
    with col4:
        st.markdown('<h3 class="subheader">Age</h3>', unsafe_allow_html=True)
        age = data['Age'].value_counts()
        fig_age = px.bar(
            x=age.index,
            y=age.values,
            labels={'x': 'Age Group', 'y': 'Count'},
            color=age.index.astype(str),  # Treat age groups as categorical values
            color_discrete_sequence=px.colors.qualitative.Pastel2,
            title="Age"
        )
        st.plotly_chart(fig_age)

# Second row: Race Distribution and Occupation Distribution
    col5, col6 = st.columns([0.5, 0.5])

    # Race Distribution
    with col5:
        st.markdown('<h3 class="subheader">Race</h3>', unsafe_allow_html=True)
        race = data['Race'].value_counts()
        fig_race = px.bar(
            race,
            x=race.index,
            y=race.values,
            labels={'x': 'Race', 'y': 'Count'},
            color=race.index.astype(str), 
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Race"
        )
        st.plotly_chart(fig_race)

    # Occupation Distribution
    with col6:
        st.markdown('<h3 class="subheader">Occupation</h3>', unsafe_allow_html=True)
        occupation = data['Occupation'].value_counts()
        fig_occupation = px.bar(
            occupation,
            x=occupation.index,
            y=occupation.values,
            labels={'x': 'Occupation', 'y': 'Count'},
            color=occupation.index.astype(str),  # Color based on occupation
            color_discrete_sequence=px.colors.qualitative.Set3, # Use a discrete color scale
            title="Occupation"
        )
        st.plotly_chart(fig_occupation)

    # Third row: Skin Conditions and Skincare Usage
    col7, col8 = st.columns([0.5, 0.5])

    # Skin Conditions
    with col7:
        st.subheader("Reported Skin Conditions")
        skin_conditions = data['Skin Conditions'].value_counts().head(10)  # Show top 10
        fig_skin_conditions = px.bar(
            skin_conditions,
            x=skin_conditions.index,
            y=skin_conditions.values,
            labels={'x': 'Skin Condition', 'y': 'Count'},
            color=skin_conditions.index.astype(str), 
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig_skin_conditions)

    # Skincare Usage
    with col8:
        st.markdown('<h3 class="subheader">Have you ever used any skin care products?</h3>', unsafe_allow_html=True)
        skincareusage = data['Have you ever used any skin care products?'].value_counts()
        fig_skincareusage = px.bar(
            skincareusage,
            x=skincareusage.index,
            y=skincareusage.values,
            labels={'x': 'Have you ever used any skin care products?', 'y': 'Count'},
            title="Have you ever used any skin care products?",
            color=skincareusage.index.astype(str), 
            color_discrete_sequence=px.colors.qualitative.Pastel2,
        )
        st.plotly_chart(fig_skincareusage)

    # Fourth row: Sample Usage and Preferred Purchase Channels
    col9, col10 = st.columns([0.5, 0.5])

    # Sample Usage Before Purchase
    with col9:
        st.markdown('<h3 class="subheader">Sample Usage Before Purchase</h3>', unsafe_allow_html=True)
        samples = data['Do you use samples before buying skincare products?'].value_counts()
        fig_samples = px.pie(
            names=samples.index,
            values=samples.values,
            title="Sample Usage Before Purchase",
            color=samples.index.astype(str), 
            color_discrete_sequence=px.colors.qualitative.Pastel2,
        )
        st.plotly_chart(fig_samples)

    # Preferred Purchase Channels
    with col10:
        st.markdown('<h3 class="subheader">Preferred Purchase Channels</h3>', unsafe_allow_html=True)
        channels = data['Where do you purchase your skin care products?'].value_counts()
        fig_channels = px.bar(
            channels,
            x=channels.index,
            y=channels.values,
            labels={'x': 'Channels', 'y': 'Count'},
            title="Preferred Purchase Channels",
            color=channels.index.astype(str), 
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig_channels)

# 3. Technology Dashboard
elif dashboard == "Technology":
    col1, col2 = st.columns([0.5, 0.5])

    # Awareness of AI
    with col1:
        st.markdown('<h3 class="subheader">Awareness of AI</h3>', unsafe_allow_html=True)
        ai_awareness = data['Have you heard about AI (Artificial Intelligence)?'].value_counts()
        fig_ai_awareness = px.pie(
            names=ai_awareness.index,
            values=ai_awareness.values,
            title="Awareness of AI",
            color=ai_awareness.index.astype(str), 
            color_discrete_sequence=px.colors.qualitative.Pastel1,
        )
        st.plotly_chart(fig_ai_awareness)

    # Interest in Skin-Scanning App
    with col2:
        st.markdown('<h3 class="subheader">Interest in Skin-Scanning App</h3>', unsafe_allow_html=True)
        interest = data['Do you want to have a skin scanning app that can customize skincare regime?'].value_counts()
        fig_interest = px.pie(
            names=interest.index,
            values=interest.values,
            title="Interest in Skin-Scanning App",
            color=interest.index.astype(str), 
            color_discrete_sequence=px.colors.qualitative.Pastel2,
        )
        st.plotly_chart(fig_interest)

    # Excitement for Skin-Scanning App
    st.markdown('<h3 class="subheader">Excitement to Use Skin-Scanning App</h3>', unsafe_allow_html=True)
    excitement = data['How excited  would you be to use the skin scanning application?'].value_counts()
    fig_excitement = px.bar(
        excitement,
        x=excitement.index,
        y=excitement.values,
        labels={'x': 'Excitement Level', 'y': 'Count'},
        title="Excitement to Use Skin-Scanning App",
        color=excitement.index.astype(str), 
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(fig_excitement)