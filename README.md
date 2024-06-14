# rental_autocar_chatbot
this code facilitates a conversational interaction with a user to collect necessary details for a service quote, stores the information in an Airtable database, and generates a personalized quote based on the provided details.

# AutoCar-Location Quote Generation and Data Storage

This Python script facilitates the collection of user information for generating travel quotes and storing this data in an Airtable database. It interacts with the user to gather necessary details, processes the information, and stores it securely.

## Prerequisites

1. Python 3.6 or later.
2. Install required packages:
    ```bash
    pip install langchain pyairtable langchain_openai
    ```
3. Set up your environment variables for API keys:
    ```bash
    export OPENAI_API_KEY='your_openai_api_key'
    export AIRTABLE_API_KEY='your_airtable_api_key'
    ```

## Configuration

- Set your Airtable base ID and table name:
    ```python
    BASE_ID = 'your_airtable_base_id'
    TABLE_NAME = 'Form_entries'
    ```

## Usage

1. **Setup API Keys**:
    Ensure that your OpenAI and Airtable API keys are correctly set in the environment.

2. **Define Prompt Templates**:
    Various prompts are predefined to gather information such as civility, name, contact details, travel dates, and more.

3. **Configure Memory and Language Model**:
    A conversation memory and the ChatOpenAI model are configured to manage the dialogue.

4. **Ask Questions**:
    The script prompts the user for information sequentially, storing each response.

5. **Add Data to Airtable**:
    The collected information is formatted and added to an Airtable database.

6. **Generate Quote**:
    A travel quote is generated based on the user's responses.

### Script Execution

Run the script:

# Execute the main script
user_responses = ask_questions(chain, prompts, questions)

# Validate and process the number of participants
if 'NB_PARTICIPANTS' in user_responses:
    try:
        user_responses['NB_PARTICIPANTS'] = int(user_responses['NB_PARTICIPANTS'])
    except ValueError:
        print("Invalid input for number of participants. Please enter a valid number.")
        user_responses['NB_PARTICIPANTS'] = 0

# Map responses to Airtable fields and store the data
record = {
    'Nombre_participants': user_responses.get('NB_PARTICIPANTS', 0),
    'Lieu_depart': user_responses.get('ADRESSE_DEPART_ALLER', ''),
    'Lieu_arrivee': user_responses.get('ADRESSE_ARRIVEE_ALLER', ''),
    'Date_aller_depart': user_responses.get('DATE_DEPART_ALLER', ''),
    'Horaire_aller': user_responses.get('HORAIRE_ALLER', ''),
    'Date_aller_arrivee': user_responses.get('DATE_ARRIVEE_ALLER', ''),
    'Option_aller': user_responses.get('OPTION_ALLER', ''),
    'Date_retour_depart': user_responses.get('DATE_RETOUR_DEPART', ''),
    'Horaire_retour': user_responses.get('HORAIRE_RETOUR', ''),
    'Date_retour_arrivee': user_responses.get('DATE_RETOUR_ARRIVEE', ''),
    'Civilite': user_responses.get('CIVILITE', ''),
    'Nom_prospect': user_responses.get('NOM', ''),
    'Prenom_prospect': user_responses.get('PRENOM', ''),
    'Telephone_prospect': user_responses.get('TELEPHONE', ''),
    'Email_prospect': user_responses.get('MAIL', ''),
}

# Add the data to Airtable
add_data_to_airtable(record)

# Generate and print the quote
quote = generate_quote(user_responses)
print(quote)
