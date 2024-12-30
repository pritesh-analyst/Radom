import streamlit as st
import random
import pickle
import os

# Filepath for the pickle file
PICKLE_FILE = "numbers_data.pkl"

# Function to save data to a pickle file
def save_data(data):
    with open(PICKLE_FILE, "wb") as f:
        pickle.dump(data, f)

# Function to load data from a pickle file
def load_data():
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return {
            "numbers_A": list(range(1, 2)),
            "numbers_B": list(range(11, 12)),
            "numbers_C": list(range(21, 22)),
            "numbers_D": list(range(31, 32)),
        }

# Load the data from the pickle file
data = load_data()

# Add custom CSS for alignment
st.markdown(
    """
    <style>
    .left-align {
        text-align: left !important;
    }
    .center-align {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title of the app
st.title('Random Number Generator and Addition')

# Create a dropdown to select option A, B, C, or D
st.markdown('<div class="center-align">', unsafe_allow_html=True)
option = st.selectbox('Choose an option', ['A', 'B', 'C', 'D'])
st.markdown('</div>', unsafe_allow_html=True)

# Display the current numbers in the selected option
if option == 'A':
    numbers = data['numbers_A']
elif option == 'B':
    numbers = data['numbers_B']
elif option == 'C':
    numbers = data['numbers_C']
else:
    numbers = data['numbers_D']

# Show current numbers in the selected option
st.markdown('<div class="left-align">', unsafe_allow_html=True)
# st.write(f'Current numbers in option {option}: {numbers}')
st.markdown('</div>', unsafe_allow_html=True)

# Display a random number from the selected list
st.markdown('<div class="left-align">', unsafe_allow_html=True)
random_number = random.choice(numbers)
st.write(f'Random Number from option {option}: {random_number}')
st.markdown('</div>', unsafe_allow_html=True)

# Allow the user to add either a number or a string
st.markdown('<div class="center-align">', unsafe_allow_html=True)
input_value = st.text_input('Enter a number or string to add to the selected option')
st.markdown('</div>', unsafe_allow_html=True)

# Add the value to the list if it's not already present
st.markdown('<div class="center-align">', unsafe_allow_html=True)
if st.button('Add Value'):
    # Check if the input is not empty
    if input_value:
        # Check if the input is a number (we try to convert it to a float)
        try:
            new_value = float(input_value)  # Try to convert to a float
            if new_value.is_integer():  # If it's an integer (whole number)
                new_value = int(new_value)  # Convert to an integer
            else:
                new_value = float(new_value)  # Otherwise, leave it as a float

        except ValueError:
            # If it's not a number, treat it as a string
            new_value = input_value

        # Add the new value to the list (if it's not already in the list)
        if new_value not in numbers:
            if option == 'A':
                data['numbers_A'].append(new_value)
            elif option == 'B':
                data['numbers_B'].append(new_value)
            elif option == 'C':
                data['numbers_C'].append(new_value)
            else:
                data['numbers_D'].append(new_value)

            # Save the updated data to the pickle file
            save_data(data)

            st.success(f'Value "{new_value}" added to option {option}!')
        else:
            st.warning(f'Value "{new_value}" already exists in option {option}.')
    else:
        st.error('Please enter a value to add.')
st.markdown('</div>', unsafe_allow_html=True)

# Refresh button to show a new random number from the selected list
st.markdown('<div class="center-align">', unsafe_allow_html=True)
if st.button('Refresh'):
    random_number = random.choice(numbers)
st.markdown('</div>', unsafe_allow_html=True)

