from github import Github
import json
import streamlit as st

# GitHub Configuration
GITHUB_TOKEN = "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"
REPO_NAME = "pritesh-analyst/Radom"
FILE_PATH = "data.json"

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Load data from GitHub
def load_data_from_github():
    try:
        file = repo.get_contents(FILE_PATH)
        data = json.loads(file.decoded_content.decode("utf-8"))
        return data
    except Exception as e:
        st.error(f"Error loading data from GitHub: {e}")
        return {
            "numbers_A": [],
            "numbers_B": [],
            "numbers_C": [],
            "numbers_D": [],
            "numbers_Check": [],
        }

# Save data to GitHub
def save_data_to_github(data):
    try:
        file = repo.get_contents(FILE_PATH)
        repo.update_file(
            file.path,
            "Update numbers data",
            json.dumps(data, indent=4),
            file.sha,
        )
        st.success("Data successfully saved to GitHub!")
    except Exception as e:
        st.error(f"Error saving data to GitHub: {e}")

# Initialize or load data
data = load_data_from_github()

# Example for adding a value (similar logic to before)
if st.button("Save Data"):
    save_data_to_github(data)# Add custom CSS for alignment
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
        data["numbers_Check"] = []
        save_data(data)
        st.success("All appended values have been deleted from option 'Check'!")

# Reset All button to clear all dictionaries
# if st.button("Reset All"):
#     data = {
#         "numbers_A": [],
#         "numbers_B": [],
#         "numbers_C": [],
#         "numbers_D": [],
#         "numbers_Check": [],
#     }
#     save_data(data)
#     st.success("All dictionaries have been reset to empty!")
