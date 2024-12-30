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

# Ensure "Check" key exists in the data dictionary
if "numbers_Check" not in data:
    data["numbers_Check"] = list(range(41, 42))
    save_data(data)  # Save the updated data to the pickle file

# Initialize session state for toggling display and random number
if "show_values" not in st.session_state:
    st.session_state["show_values"] = False
if "random_number" not in st.session_state:
    st.session_state["random_number"] = None

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

# Create a dropdown to select option A, B, C, D, or Check
st.markdown('<div class="center-align">', unsafe_allow_html=True)
option = st.selectbox('Choose an option', ['A', 'B', 'C', 'D', 'Check'])
st.markdown('</div>', unsafe_allow_html=True)

# Display the current numbers in the selected option
if option == 'A':
    numbers = data['numbers_A']
elif option == 'B':
    numbers = data['numbers_B']
elif option == 'C':
    numbers = data['numbers_C']
elif option == 'D':
    numbers = data['numbers_D']
else:  # For Check option
    numbers = data['numbers_Check']

# Allow the user to add either a number or a string
st.markdown('<div class="center-align">', unsafe_allow_html=True)
input_value = st.text_input('Enter a number or string to add to the selected option')
st.markdown('</div>', unsafe_allow_html=True)

# Add the value to the list if it's not already present
st.markdown('<div class="center-align">', unsafe_allow_html=True)
if st.button('Add Value'):
    if input_value:
        try:
            new_value = float(input_value)
            new_value = int(new_value) if new_value.is_integer() else new_value
        except ValueError:
            new_value = input_value

        if new_value not in numbers:
            data[f"numbers_{option}"].append(new_value)
            save_data(data)
            st.success(f'Value "{new_value}" added to option {option}!')
        else:
            st.warning(f'Value "{new_value}" already exists in option {option}.')
    else:
        st.error('Please enter a value to add.')
st.markdown('</div>', unsafe_allow_html=True)

# Toggle button to display or hide values
st.markdown('<div class="center-align">', unsafe_allow_html=True)
if st.button('Display'):
    st.session_state["show_values"] = not st.session_state["show_values"]

# Display or hide the values based on session state
if st.session_state["show_values"]:
    st.markdown('<div class="left-align">', unsafe_allow_html=True)
    st.write(f'Appended values in option {option}: {numbers}')
    st.markdown('</div>', unsafe_allow_html=True)

# Refresh button to generate a new random number
if st.button('Refresh'):
    st.session_state["random_number"] = random.choice(numbers)
    st.success(f'New Random Number: {st.session_state["random_number"]}')

# Delete button for the "Check" option
if option == "Check":
    if st.button("Delete"):
        data["numbers_Check"] = list(range(41, 51))  # Reset to the initial list
        save_data(data)  # Save changes to the pickle file
        st.success("All appended values have been deleted from option 'Check'!")
