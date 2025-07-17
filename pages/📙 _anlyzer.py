import streamlit as st # type: ignore
import pandas as pd # type: ignore
import nltk # type: ignore
import random
import matplotlib.pyplot as plt # type: ignore
from nltk.tokenize import word_tokenize # type: ignore
from nltk.corpus import stopwords # type: ignore
import re
import base64

import nltk

# type: ignore

nltk.download('punkt_tab')



try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Define Bloom's Taxonomy levels and their characteristics
blooms_taxonomy = {
    "Remember": {
        "description": "Recall facts and basic concepts",
        "verbs": ["define", "duplicate", "list", "memorize", "recall", "repeat", "reproduce", "state", "identify", "name", "recognize"],
        "question_starters": ["What is...", "Who was...", "When did...", "How would you describe...", "Can you recall...", "How would you define...", "How would you identify..."],
        "example": "What are the six levels of Bloom's Taxonomy?",
       "image_url": r"images/remember-at-10.17.08-copy-1-1024x575.jpg"
    },
    "Understand": {
        "description": "Explain ideas or concepts",
        "verbs": ["classify", "describe", "discuss", "explain", "identify", "locate", "recognize", "report", "select", "translate", "paraphrase", "interpret", "summarize"],
        "question_starters": ["How would you classify...", "How would you compare...", "What is the main idea of...", "Can you explain what is happening...", "How would you summarize...", "How would you rephrase..."],
        "example": "Explain the difference between the Remember and Understand levels in Bloom's Taxonomy.",
        "image_url": r"images/understand-at-10.17.30-copy-1-1024x575.jpg"
    },
    "Apply": {
        "description": "Use information in new situations",
        "verbs": ["execute", "implement", "solve", "use", "demonstrate", "interpret", "operate", "schedule", "sketch", "apply", "employ", "illustrate", "practice"],
        "question_starters": ["How would you use...", "What examples can you find to...", "How would you solve __ using what you've learned...", "How would you organize __ to show...", "How would you apply what you learned to develop..."],
        "example": "Using Bloom's Taxonomy, create a set of questions for teaching photosynthesis.",
        "image_url": r"images/apply-at-10.17.53-copy-1-1024x575.jpg"
    },
    "Analyze": {
        "description": "Draw connections among ideas",
        "verbs": ["differentiate", "organize", "relate", "compare", "contrast", "distinguish", "examine", "experiment", "question", "test", "analyze", "categorize", "criticize", "diagram"],
        "question_starters": ["What are the parts or features of...", "How is __ related to...", "Why do you think...", "What is the theme...", "What motive is there...", "What conclusions can you draw..."],
        "example": "Analyze how different question types affect student engagement in online learning.",
        "image_url": r"images/analyze-at-10.18.16-copy-1-1024x575.jpg"
          
    },
    "Evaluate": {
        "description": "Justify a stand or decision",
        "verbs": ["appraise", "argue", "defend", "judge", "select", "support", "value", "evaluate", "critique", "weigh", "assess", "choose", "compare", "conclude", "measure"],
        "question_starters": ["Do you agree with the actions...", "What is your opinion of...", "How would you prove/disprove...", "How would you evaluate...", "What choice would you have made...", "What data was used to make the conclusion..."],
        "example": "Evaluate the effectiveness of using Bloom's Taxonomy in curriculum design.",
        "image_url": r"images/evaluate-at-10.18.56-copy-1-1024x575.jpg"
    },
    "Create": {
        "description": "Produce new or original work",
        "verbs": ["design", "assemble", "construct", "conjecture", "develop", "formulate", "author", "investigate", "create", "compose", "generate", "plan", "produce", "devise", "invent"],
        "question_starters": ["What would happen if...", "Can you design a __ to...", "Can you see a possible solution to...", "How would you devise your own way to...", "What would you create to change...", "How would you test..."],
        "example": "Design a new educational framework that builds upon Bloom's Taxonomy for the digital age.",
        "image_url": r"images/create-at-10.19.27-copy-1-1024x575.jpg"
    }
}

# Function to analyze a question and determine its Bloom's level
def analyze_question(question):
    question = question.lower()
    tokens = word_tokenize(question)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in tokens if w.isalpha() and w not in stop_words]
    
    # Check for question starters
    starter_matches = {}
    for level, data in blooms_taxonomy.items():
        for starter in data["question_starters"]:
            starter_lower = starter.lower().replace("...", "")
            if question.startswith(starter_lower):
                if level not in starter_matches:
                    starter_matches[level] = 0
                starter_matches[level] += 3  # Give more weight to question starters
    
    # Check for verbs
    verb_matches = {}
    for level, data in blooms_taxonomy.items():
        for verb in data["verbs"]:
            if verb in filtered_tokens:
                if level not in verb_matches:
                    verb_matches[level] = 0
                verb_matches[level] += 1
    
    # Combine matches
    all_matches = {}
    for level in blooms_taxonomy.keys():
        all_matches[level] = starter_matches.get(level, 0) + verb_matches.get(level, 0)
    
    # If no clear matches, use a more sophisticated approach
    if sum(all_matches.values()) == 0:
        # Look for patterns in the question
        if re.search(r'what is|who is|when|where|list|name|identify', question):
            all_matches["Remember"] += 1
        if re.search(r'describe|explain|summarize|interpret|infer', question):
            all_matches["Understand"] += 1
        if re.search(r'apply|use|demonstrate|illustrate|show', question):
            all_matches["Apply"] += 1
        if re.search(r'analyze|compare|contrast|examine|investigate', question):
            all_matches["Analyze"] += 1
        if re.search(r'evaluate|assess|justify|critique|recommend', question):
            all_matches["Evaluate"] += 1
        if re.search(r'create|design|develop|compose|construct|formulate', question):
            all_matches["Create"] += 1
    
    # Determine the most likely level
    if sum(all_matches.values()) == 0:
        return "Remember", 0  # Default to lowest level if no matches
    
    max_level = max(all_matches, key=all_matches.get)
    confidence = all_matches[max_level] / sum(all_matches.values()) * 100
    
    return max_level, confidence

# Function to generate a question based on a topic and Bloom's level
def generate_question(topic, level):
    if level not in blooms_taxonomy:
        return "Invalid Bloom's Taxonomy level selected."
    
    starter = random.choice(blooms_taxonomy[level]["question_starters"])
    verb = random.choice(blooms_taxonomy[level]["verbs"])
    
    # Replace placeholder with topic
    question = starter.replace("...", f" {topic}")
    
    # If the starter doesn't have a placeholder, append the topic
    if "..." in starter:
        return question
    else:
        return f"{question} {topic}?"

# Function to create a downloadable CSV
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="bloom_questions.csv">Download CSV File</a>'
    return href

# Streamlit UI
def main():
    st.set_page_config(page_title="Bloom's Taxonomy Tool", layout="wide")
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f3f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    .bloom-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🧠 Bloom's Taxonomy Question Tool")
    st.markdown("Analyze and generate questions based on Bloom's Taxonomy cognitive levels")
    
    tabs = st.tabs(["Question Analyzer", "Question Generator", "Bloom's Taxonomy Guide"])
    
    # Question Analyzer Tab
    with tabs[0]:
        st.header("Question Analyzer")
        st.markdown("Paste your questions below to analyze their Bloom's Taxonomy levels")
        
        text_area = st.text_area("Enter one or more questions (one per line):", height=150)
        
        if st.button("Analyze Questions"):
            if text_area:
                questions = text_area.strip().split('\n')
                results = []
                
                for q in questions:
                    if q.strip():
                        level, confidence = analyze_question(q)
                        results.append({
                            "Question": q,
                            "Bloom's Level": level,
                            "Confidence": f"{confidence:.1f}%"
                        })
                
                if results:
                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Create visualization
                    level_counts = results_df["Bloom's Level"].value_counts()
                    
                    col1, col2 = st.columns([3, 2])
                    
                    with col1:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        bars = ax.bar(level_counts.index, level_counts.values, color=['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462'])
                        ax.set_xlabel('Bloom\'s Taxonomy Level')
                        ax.set_ylabel('Number of Questions')
                        ax.set_title('Distribution of Questions by Bloom\'s Taxonomy Level')
                        
                        # Add count labels on top of bars
                        for bar in bars:
                            height = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.0f}', 
                                    ha='center', va='bottom')
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    with col2:
                        st.markdown("### Summary")
                        st.markdown(f"Total questions analyzed: **{len(results)}**")
                        
                        # Calculate percentages
                        for level, count in level_counts.items():
                            percentage = (count / len(results)) * 100
                            st.markdown(f"- **{level}**: {count} questions ({percentage:.1f}%)")
                        
                        st.markdown("### Export Results")
                        st.markdown(get_table_download_link(results_df), unsafe_allow_html=True)
                else:
                    st.warning("No valid questions found. Please enter at least one question.")
            else:
                st.warning("Please enter at least one question to analyze.")
    
    # Question Generator Tab
    with tabs[1]:
        st.header("Question Generator")
        st.markdown("Generate questions based on a topic and Bloom's Taxonomy level")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Enter a topic or subject:", "photosynthesis")
        
        with col2:
            level = st.selectbox("Select Bloom's Taxonomy level:", list(blooms_taxonomy.keys()))
        
        if st.button("Generate Question"):
            if topic:
                question = generate_question(topic, level)
                st.success(f"Generated Question: **{question}**")
                
                # Show example verbs for this level
                st.markdown(f"### Sample verbs for {level} level")
                st.markdown(", ".join(blooms_taxonomy[level]["verbs"][:10]))
                
                # Option to generate multiple questions
                st.markdown("### Generate Multiple Questions")
                num_questions = st.slider("Number of questions to generate:", 1, 20, 5)
                
                if st.button("Generate Multiple Questions"):
                    questions = []
                    for _ in range(num_questions):
                        questions.append({
                            "Question": generate_question(topic, level),
                            "Bloom's Level": level
                        })
                    
                    questions_df = pd.DataFrame(questions)
                    st.dataframe(questions_df, use_container_width=True)
                    st.markdown(get_table_download_link(questions_df), unsafe_allow_html=True)
            else:
                st.warning("Please enter a topic to generate questions.")
        
        # Multi-level generator
        st.markdown("### Generate Questions for All Levels")
        if st.button("Generate Questions for All Levels"):
            if topic:
                all_questions = []
                for bloom_level in blooms_taxonomy.keys():
                    question = generate_question(topic, bloom_level)
                    all_questions.append({
                        "Bloom's Level": bloom_level,
                        "Question": question,
                        "Description": blooms_taxonomy[bloom_level]["description"]
                    })
                
                all_questions_df = pd.DataFrame(all_questions)
                st.dataframe(all_questions_df, use_container_width=True)
                st.markdown(get_table_download_link(all_questions_df), unsafe_allow_html=True)
            else:
                st.warning("Please enter a topic to generate questions.")
    
    # Bloom's Taxonomy Guide Tab
    with tabs[2]:
        st.header("Bloom's Taxonomy Guide")
        st.markdown("""
        Bloom's Taxonomy is a framework used to classify educational learning objectives into levels of complexity and specificity.
        The taxonomy was first presented in 1956 and has since been revised. The cognitive domain is organized into six levels:
        """)
        
        for level, data in blooms_taxonomy.items():

            st.image(data["image_url"], caption=level, use_container_width=True)

           
            st.markdown(f"""
            <div class="bloom-card style="border:1px solid #ccc; padding:16px; border-radius:8px;">
               
                       
        

        
            </div>
            """, unsafe_allow_html=True)
        
          

        
        st.markdown("""
        ### Tips for Using Bloom's Taxonomy in Education
        
        1. **Balance your questions** across different cognitive levels to promote higher-order thinking
        2. **Start with lower levels** and progressively move to higher levels
        3. **Use the appropriate verbs** when formulating learning objectives and questions
        4. **Align assessments** with the cognitive level of your learning objectives
        5. **Provide scaffolding** to help students move from lower to higher cognitive levels
        """)

if __name__ == "__main__":
    main()