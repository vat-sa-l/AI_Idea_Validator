import streamlit as st
from gpt_analysis import *
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Idea Validator")

st.title("IdeaBoost: Validate, Refine, and Launch Your Startup Idea")
st.markdown("**Enter your startup idea below to validate it using AI!**")

idea = st.text_area(" Describe your startup idea here")

if st.button("Validate Idea"):
    if not idea.strip():
        st.warning("Please enter an idea.")
    else:
        with st.spinner("Analyzing your idea..."):
            market_size = get_market_size(idea)
            competitors = get_competitors(idea)
            pain_points = get_pain_points(idea)
            monetization = get_monetization(idea)
            improvements = get_improvements(idea)

     
        st.subheader(" Market Size")
        st.write(market_size)

        st.subheader("Possible Competitors")
        st.write(competitors)

        st.subheader(" Pain Points Solved")
        st.write(pain_points)

        st.subheader(" Monetization Ideas")
        st.write(monetization)

        st.subheader(" Suggested Tweaks to Improve Your Idea")
        st.write(improvements)

        
        st.subheader(" Visual Summary")

        sections = ['Market Size', 'Competitors', 'Pain Points', 'Monetization', 'Tweaks']
        scores = [8, 5, 7, 6, 4]  

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(sections, scores)
        ax.set_title('AI Idea Validation Overview')
        ax.set_ylabel('Impact Score')
        ax.set_xlabel('Validation Sections')
        ax.grid(axis='y')

        st.pyplot(fig)
