import os
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from pyairtable import Table

# Setup API keys
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

API_KEY = 'your_airtable_api_key'
BASE_ID = 'your_airtable_base_id'
TABLE_NAME = 'Form_entries'

# Define Prompt Templates
prompts = {
    "CIVILITE": ChatPromptTemplate.from_template("Bonjour et bienvenue chez autocar-location ! Afin de vous designer un devis adapté, je vais vous poser quelques questions. Quelle est votre civilité (Monsieur, Madame) ?"),
    "NOM": ChatPromptTemplate.from_template("Quel est votre nom de famille ?"),
    "PRENOM": ChatPromptTemplate.from_template("Quel est votre prénom ?"),
    "TELEPHONE": ChatPromptTemplate.from_template("Quel est votre numéro de téléphone ?"),
    "MAIL": ChatPromptTemplate.from_template("Quelle est votre adresse email ?"),
    "NB_PARTICIPANTS": ChatPromptTemplate.from_template("Combien de passagers vont voyager ?"),
    "DATE_DEPART_ALLER": ChatPromptTemplate.from_template("Quelle est la date de départ (format YYYY-MM-DD) ?"),
    "HORAIRE_ALLER": ChatPromptTemplate.from_template("Quelle est l'heure de départ (format HH:MM) ?"),
    "ADRESSE_DEPART_ALLER": ChatPromptTemplate.from_template("Quelle est l'adresse de départ ?"),
    "DATE_ARRIVEE_ALLER": ChatPromptTemplate.from_template("Quelle est la date d'arrivée (format YYYY-MM-DD) ?"),
    "ADRESSE_ARRIVEE_ALLER": ChatPromptTemplate.from_template("Quelle est l'adresse d'arrivée ?"),
    "OPTION_ALLER": ChatPromptTemplate.from_template("S'agit-il d'un aller simple ou d'un aller-retour ?"),
    "DATE_RETOUR_DEPART": ChatPromptTemplate.from_template("Quelle est la date de départ pour le retour (format YYYY-MM-DD) ?"),
    "HORAIRE_RETOUR": ChatPromptTemplate.from_template("Quelle est l'heure de départ pour le retour (format HH:MM) ?"),
    "DATE_RETOUR_ARRIVEE": ChatPromptTemplate.from_template("Quelle est la date d'arrivée pour le retour (format YYYY-MM-DD) ?")
}

# Configure memory
memory = ConversationBufferMemory()

# Create LLM and Chain
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = ConversationChain(llm=llm, memory=memory)

# Define conversation logic
questions = [
    "CIVILITE",
    "NOM",
    "PRENOM",
    "TELEPHONE",
    "MAIL",
    "NB_PARTICIPANTS",
    "DATE_DEPART_ALLER",
    "HORAIRE_ALLER",
    "ADRESSE_DEPART_ALLER",
    "DATE_ARRIVEE_ALLER",
    "ADRESSE_ARRIVEE_ALLER",
    "OPTION_ALLER",
    "DATE_RETOUR_DEPART",
    "HORAIRE_RETOUR",
    "DATE_RETOUR_ARRIVEE"
]

def ask_questions(chain, prompts, questions):
    responses = {}
    for question in questions:
        prompt_text = prompts[question].format()  # Get the prompt text
        print(prompt_text)  # Show the question to the user
        user_input = input()  # Get the user's response
        response = chain.invoke({"input": user_input})  # Invoke the chain with the user's response
        responses[question] = user_input  # Store the user's response in the dictionary
    return responses

def add_data_to_airtable(record):
    # Create an instance of the Airtable table
    table = Table(API_KEY, BASE_ID, TABLE_NAME)

    # Add the record to the table
    try:
        response = table.create(record)
        print('Record added:', response)
    except Exception as e:
        print('Error adding record:', e)

# Get user responses
user_responses = ask_questions(chain, prompts, questions)

# Convert "Nombre_participants" to an integer
if 'NB_PARTICIPANTS' in user_responses:
    try:
        user_responses['NB_PARTICIPANTS'] = int(user_responses['NB_PARTICIPANTS'])
    except ValueError:
        print("Invalid input for number of participants. Please enter a valid number.")
        user_responses['NB_PARTICIPANTS'] = 0  # Default to 0 or handle accordingly

# Map the responses to Airtable fields
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

# Call the function to add the data to Airtable
add_data_to_airtable(record)

# Generate the quote
def generate_quote(responses):
    quote = f"""
    Merci {responses.get('CIVILITE', '')} {responses.get('NOM', '')} {responses.get('PRENOM', '')} pour votre demande.
    Voici votre devis:
    Nombre de passagers: {responses.get('NB_PARTICIPANTS', '')}
    Départ: {responses.get('ADRESSE_DEPART_ALLER', '')} le {responses.get('DATE_DEPART_ALLER', '')}
    Arrivée: {responses.get('ADRESSE_ARRIVEE_ALLER', '')} le {responses.get('DATE_ARRIVEE_ALLER', '')}
    """
    return quote

quote = generate_quote(user_responses)
print(quote)
