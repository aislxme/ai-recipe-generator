import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime
import time

# Configure the page
st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🧑‍🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .recipe-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .recipe-title {
        font-size: 2rem;
        font-weight: 600;
        color: #2E8B57;
        margin-bottom: 1rem;
    }
    
    .recipe-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .time-badge {
        background: #2E8B57;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .ingredient-item {
        background: #f8f9fa;
        padding: 0.5rem 1rem;
        border-left: 4px solid #2E8B57;
        margin: 0.5rem 0;
        color:#000000;
        font-weight:500;
    }
    
    .step-number {
        background: #2E8B57;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
    }
    
    .sidebar-title {
        color: #2E8B57;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .error-message {
        background: #ffebee;
        color: #c62828;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #c62828;
    }
    
    .success-message {
        background: #e8f5e8;
        color: #2e7d32;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recipe_generated' not in st.session_state:
    st.session_state.recipe_generated = False
if 'current_recipe' not in st.session_state:
    st.session_state.current_recipe = None

# API Configuration
def configure_gemini():
    """Configure Gemini AI with API key"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("🔑 Please set your GEMINI_API_KEY in the environment variables or Streamlit secrets.")
        st.stop()
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

# Recipe Generation Function
def generate_recipe(ingredients, cooking_time, meal_type, dietary_preferences, cuisine_style, skill_level):
    """Generate recipe using Gemini AI with structured output"""
    
    model = configure_gemini()
    
    # Create structured prompt
    prompt = f"""
    Generate a detailed recipe using these specifications:
    
    **Ingredients Available:** {ingredients}
    **Maximum Cooking Time:** {cooking_time} minutes
    **Meal Type:** {meal_type}
    **Dietary Preferences:** {dietary_preferences}
    **Cuisine Style:** {cuisine_style}
    **Cooking Skill Level:** {skill_level}
    
    Please provide a complete recipe with:
    1. Creative recipe name
    2. Brief description
    3. Prep time, cook time, and total time (ensure total time ≤ {cooking_time} minutes)
    4. Number of servings
    5. Complete ingredients list with measurements
    6. Step-by-step cooking instructions
    7. Tips for best results
    8. Nutritional highlights
    
    Format as JSON with this structure:
    {{
        "name": "Recipe Name",
        "description": "Brief appetizing description",
        "prep_time": number,
        "cook_time": number,
        "total_time": number,
        "servings": number,
        "ingredients": ["ingredient 1", "ingredient 2", ...],
        "instructions": ["step 1", "step 2", ...],
        "tips": ["tip 1", "tip 2", ...],
        "nutrition_highlights": ["highlight 1", "highlight 2", ...]
    }}
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json"
            }
        )
        
        recipe_data = json.loads(response.text)
        return recipe_data, None
        
    except Exception as e:
        return None, str(e)

def display_recipe(recipe_data):
    """Display the generated recipe with professional styling"""

    st.markdown('<div class="recipe-container">', unsafe_allow_html=True)

    # Recipe Title and Description
    st.markdown(f'<div class="recipe-title">🍽️ {recipe_data["name"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size: 1.1rem; color: #666; font-style: italic;">{recipe_data["description"]}</p>', unsafe_allow_html=True)
    st.markdown("</div",unsafe_allow_html=True)
    # Time Information
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<span class="time-badge">⏲️ Prep: {recipe_data["prep_time"]}min</span>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<span class="time-badge">🔥 Cook: {recipe_data["cook_time"]}min</span>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<span class="time-badge">⏰ Total: {recipe_data["total_time"]}min</span>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<span class="time-badge">👥 Serves: {recipe_data["servings"]}</span>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Ingredients Section
        st.markdown("""<div class="recipe-section"><h3 style="margin-top:0;color:#2E8B57;">🛒 Ingredients</h3>""", unsafe_allow_html=True)
        for ingredient in recipe_data["ingredients"]:
            st.markdown(f'<div class="ingredient-item">• {ingredient}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tips Section
        if recipe_data.get("tips"):
            st.markdown("""<div class="recipe-section"><h3 style="margin-top:0;color:#2E8B57;">💡 Chef's Tips</h3>""", unsafe_allow_html=True)
            for tip in recipe_data["tips"]:
                st.markdown(f"💡 {tip}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Instructions Section
        st.markdown("""<div class="recipe-section"><h3 style="margin-top:0;color:#2E8B57;">👨‍🍳 Instructions</h3>""", unsafe_allow_html=True)
        for i, instruction in enumerate(recipe_data["instructions"], 1):
            st.markdown(f"""
            <div style="display: flex; align-items: flex-start; margin: 1rem 0;">
                <span class="step-number">{i}</span>
                <span>{instruction}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Nutrition Highlights
        if recipe_data.get("nutrition_highlights"):
            st.markdown("""<div class="recipe-section"><h3 style="margin-top:0;color:#2E8B57;">🥗 Nutritional Highlights</h3>""", unsafe_allow_html=True)
            for highlight in recipe_data["nutrition_highlights"]:
                st.markdown(f"🌟 {highlight}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main App Layout
def main():
    # Header
    st.markdown('<div class="main-header">🧑‍🍳 AI Recipe Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create delicious recipes from your ingredients with AI-powered suggestions</div>', unsafe_allow_html=True)
    
    # Sidebar for inputs
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🔧 Recipe Settings</div>', unsafe_allow_html=True)
        
        # Main inputs
        ingredients = st.text_area(
            "🥕 Available Ingredients",
            placeholder="e.g., chicken breast, rice, onions, garlic, tomatoes...",
            help="Enter the ingredients you have available, separated by commas"
        )
        
        cooking_time = st.slider(
            "⏰ Maximum Cooking Time (minutes)",
            min_value=15,
            max_value=180,
            value=45,
            step=5,
            help="How much time do you have for cooking?"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            meal_type = st.selectbox(
                "🍽️ Meal Type",
                ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]
            )
        
        with col2:
            skill_level = st.selectbox(
                "👨‍🍳 Skill Level",
                ["Beginner", "Intermediate", "Advanced"]
            )
        
        dietary_preferences = st.multiselect(
            "🥗 Dietary Preferences",
            ["Vegetarian", "Non-Veg", "Gluten-Free", "Dairy-Free", "Low-Carb", "Keto", "Paleo"],
            help="Select any dietary restrictions or preferences"
        )
        
        cuisine_style = st.selectbox(
            "🌍 Cuisine Style",
            ["Any", "Italian", "Indian", "Chinese", "Mexican", "Mediterranean", "Thai", "Japanese", "American", "French"]
        )
        
        # Generate button
        st.markdown("<br>", unsafe_allow_html=True)
        generate_button = st.button(
            "✨ Generate Recipe",
            use_container_width=True,
            type="primary"
        )
        
        # API Key info
        st.markdown("---")
        st.markdown("### ⚙️ Setup")
        st.info("💡 Make sure to set your GEMINI_API_KEY in environment variables or Streamlit secrets")
        
        if st.button("🔗 Get Gemini API Key", use_container_width=True):
            st.markdown("[Get your API key here](https://aistudio.google.com/app/apikey)")
    
    # Main content area
    if generate_button:
        if not ingredients.strip():
            st.error("🚨 Please enter some ingredients to get started!")
            return
        
        # Processing message
        with st.spinner("🤖 AI Chef is creating your recipe..."):
            time.sleep(1)  # Small delay for better UX
            
            # Generate recipe
            recipe_data, error = generate_recipe(
                ingredients,
                cooking_time,
                meal_type,
                ", ".join(dietary_preferences) if dietary_preferences else "None",
                cuisine_style,
                skill_level
            )
            
            if error:
                st.markdown(f'<div class="error-message">❌ Error generating recipe: {error}</div>', unsafe_allow_html=True)
                st.markdown("### 🔧 Troubleshooting Tips:")
                st.markdown("- Check your API key configuration")
                st.markdown("- Verify your internet connection")
                st.markdown("- Try with different or fewer ingredients")
                return
            
            if recipe_data:
                st.session_state.current_recipe = recipe_data
                st.session_state.recipe_generated = True
                st.markdown('<div class="success-message">✅ Recipe generated successfully!</div>', unsafe_allow_html=True)
    
    # Display recipe if available
    if st.session_state.recipe_generated and st.session_state.current_recipe:
        display_recipe(st.session_state.current_recipe)
        
        # Download recipe as JSON
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            recipe_json = json.dumps(st.session_state.current_recipe, indent=2)
            st.download_button(
                label="📄 Download Recipe (JSON)",
                data=recipe_json,
                file_name=f"{st.session_state.current_recipe['name'].replace(' ', '_')}.json",
                mime="application/json"
            )
        
        with col2:
            if st.button("🔄 Generate New Recipe", use_container_width=True):
                st.session_state.recipe_generated = False
                st.session_state.current_recipe = None
                st.rerun()
    
    elif not st.session_state.recipe_generated:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 2rem 0;">
            <h2>🎯 How to Use</h2>
            <p style="font-size: 1.1rem; margin: 1rem 0;">
                1. 📝 Enter your available ingredients<br>
                2. ⏰ Set your cooking time preference<br>
                3. 🎛️ Choose your meal preferences<br>
                4. ✨ Click "Generate Recipe" to get started!
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
