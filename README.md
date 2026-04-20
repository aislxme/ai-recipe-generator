# AI Recipe Generator

AI Recipe Generator is a Streamlit web application that uses Google Generative AI to create customized recipes based on available ingredients and user preferences.

## Problem Statement
People often do not know what to cook with the ingredients they already have. This can waste time and lead to food waste. 

## Objective
The objective of this project is to generate complete recipes instantly using AI, make cooking easier and faster, and reduce food waste by using available ingredients.

## Features
- Enter available ingredients
- Select maximum cooking time
- Choose meal type
- Choose dietary preferences
- Select cuisine style
- Select cooking skill level
- Generate a complete recipe instantly
- View recipe name, description, ingredients, instructions, tips, and nutrition highlights
- Download the generated recipe as JSON

## Tech Stack
- Python
- Streamlit
- Google Generative AI
- JSON

## How It Works
1. The user enters available ingredients.
2. The user selects cooking time and meal preferences.
3. The app sends the input to Google Generative AI.
4. The AI generates a recipe in JSON format.
5. The recipe is displayed in the Streamlit app.


## Installation
1. Clone or download the project.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your Gemini API key as an environment variable.
4. Run the app:

```bash
streamlit run app.py
```

## Example Inputs
- Ingredients: egg, onion, tomato
- Cooking time: 20 minutes
- Meal type: Breakfast
- Skill level: Beginner

## Future Scope
- Image generation
- Nutrition analysis
- Mobile app version
- Voice input

## Conclusion
This project combines Python, AI, and Streamlit to make daily cooking easier and show how technology can solve real-world problems.
