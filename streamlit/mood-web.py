import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.linear_model import LinearRegression
import ssl

# 0. Set Password
def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("Type Password", type="password", 
                      on_change=lambda: st.session_state.update(password_correct=(st.session_state.password == "0000")), # Put your own password instead of 0000
                      key="password") 
        return False
    return st.session_state["password_correct"]

if not check_password():
    st.stop()  # Stop here if password is wrong

# 1. Title & Layout
st.set_page_config(page_title="Your Mood Dashboard", layout="wide")

# 2. Anti - SSL error
ssl._create_default_https_context = ssl._create_unverified_context
st.title("💓 Your Realtime Mood Dashboard")
st.markdown("---")

# 3. Call & Frame data
url = "your google sheets' url here" # Put your google sheets' .csv url of mood

@st.cache_data(ttl=300) # Renew data in 300 secs
def load_data():
    df = pd.read_csv(url, names=['Date', 'Time', 'Raw_Emotion'], header=None)
    df['Emotion'] = df['Raw_Emotion'].str.strip().str.split(' ').str[0]
    df['Emoji'] = df['Raw_Emotion'].str.strip().str.split(' ').str[1]
    df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    mapping = {'Excited':3, 'Happy': 2, 'Peace':1, 'Tired':0, 'Anxious':-1, 'Angry':-2}  # You can score mood as you want (The larger scale is, the more dramatic graph becomes)
    df['Score'] = df['Emotion'].map(mapping)
    df = df.reset_index()
    return df

# 4. Load data
try:
    df = load_data()

    # Uppper lay out (Bar chart & WordCloud)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Moods Frequency")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.countplot(data=df, x='Emotion', palette='pastel', ax=ax1)
        st.pyplot(fig1)

    with col2:
        st.subheader("☁️ Emoji WordCloud")
        emoji_text = " ".join(df['Emoji'].dropna())
        if emoji_text.strip():
            wc = WordCloud(width=800, height=400, background_color='black', 
                           regexp=r"\S+", colormap='spring', min_font_size=10, max_font_size=300, relative_scaling=1, margin=1).generate(emoji_text)
            st.image(wc.to_array(), use_container_width=True)
        else:
            st.write("Not enough data to create WordCloud")

    st.markdown("---")

    # Bottom layout: Time Series & Linear Regression
    st.subheader("📈 Tendecy & Regression of Moods")

    # Fitting Regression
    X = df[['index']]
    Y = df['Score'].fillna(0) # handling none

    model = LinearRegression()
    model.fit(X, Y)
    Y_pred = model.predict(X)
    slope = model.coef_[0]

    # Interpreation
    if slope > 0:
        st.success(f"Regression analysis shows a steady upward trend in your mood by {model.coef_[0]:.4f} over time. Good job!")
    else:
        st.warning(f"Regression analysis shows a steady downward trend in your mood over time.(Slope: {slope:.4f}) Let's hang in there!")

    # Draw Time Series & Regression Line
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    
    ax2.plot(df['Timestamp'], df['Score'], marker='o', linestyle='-', color='skyblue', alpha=0.7, label='Mood Flow')
    ax2.scatter(df['Timestamp'], df['Score'], color='gray', alpha=0.5, label='Real Mood')
    ax2.plot(df['Timestamp'], Y_pred, color='red', linewidth=3, label=f'Trend Line (slope: {slope:.4f})')
    ax2.axhline(0, color='black', linestyle='--', alpha=0.3) # baseline 0
    plt.xticks(rotation=45)
    ax2.set_ylabel("Mood Score")
    ax2.legend()
    st.pyplot(fig2)

    # Check box for raw data
    if st.checkbox('Show Raw Data Table'):
        st.dataframe(df[['Date', 'Time', 'Emoji', 'Score']].sort_values(by=['Date', 'Time'], ascending=False))

except Exception as e:
    st.error(f"Error when bringing data: {e}")
