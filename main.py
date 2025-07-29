import streamlit as st
from gpt_analysis import *
import matplotlib.pyplot as plt


import concurrent.futures

st.set_page_config(page_title="AI Idea Validator")

st.title("IdeaBoost: Validate, Refine, and Launch Your Startup Idea")
st.markdown("**Enter your startup idea below to validate it using AI!**")

idea = st.text_area(" Describe your startup idea here")

if st.button("Validate Idea"):
    if not idea.strip():
        st.warning("Please enter an idea.")
    else:
        with st.spinner("Analyzing your idea..."):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
            "market_size": executor.submit(get_market_size, idea),
            "competitors": executor.submit(get_competitors, idea),
            "pain_points": executor.submit(get_pain_points, idea),
            "monetization": executor.submit(get_monetization, idea),
            "improvements": executor.submit(get_improvements, idea),
            "personas": executor.submit(get_customer_personas,idea),
            "validation_scores": executor.submit(get_validation_scores, idea)
        }
                results = {k: f.result() for k, f in futures.items()}

        market_size = results["market_size"]
        competitors = results["competitors"]
        pain_points = results["pain_points"]
        monetization = results["monetization"]
        improvements = results["improvements"]
        validation_scores = results["validation_scores"]
        sections = list(validation_scores.keys())
        scores = list(validation_scores.values())

        personas = results["personas"]
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

        st.subheader("👥 Ideal Customer Personas")
        if "👤" in personas:
            persona_blocks = personas.split("👤 Persona")[1:]
            for idx, block in enumerate(persona_blocks):
                full_block = "👤 Persona" + block.strip()
                with st.expander(f"Persona {idx + 1}"):
                    st.markdown(full_block)
        else:
            st.markdown(personas)


        st.subheader(" Visual Summary")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(sections, scores, color='skyblue')
        ax.set_title('AI Idea Validation Overview')
        ax.set_ylabel('Impact Score')
        ax.set_xlabel('Validation Sections')
        ax.set_ylim(0, 10)
        ax.grid(axis='y')

        st.pyplot(fig)

