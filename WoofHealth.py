#Import All Libraries & Modules
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chains.conversation.memory import ConversationEntityMemory
from streamlit_extras.switch_page_button import switch_page
from langchain.chains import ConversationChain
from streamlit_extras.app_logo import add_logo
from streamlit_extras.let_it_rain import rain
from streamlit_extras.badges import badge
import streamlit_authenticator as stauth
from langchain.llms import OpenAI
from pyrebase import pyrebase
from datetime import datetime
import streamlit as st
from PIL import Image
import base64

#Configuration Key
firebaseConfig = {
  'apiKey': "AIzaSyDG52-_xfL3lgz7iQQk4mAxGzzfk3oiO_c",
  'authDomain': "pethealth-e1fee.firebaseapp.com",
  'projectId': "pethealth-e1fee",
  'databaseURL':"https://pethealth-e1fee-default-rtdb.asia-southeast1.firebasedatabase.app/",
  'storageBucket': "pethealth-e1fee.appspot.com",
  'messagingSenderId': "554455864755",
  'appId': "1:554455864755:web:b29de3c0b60adf4f0867c6",
  'measurementId': "G-D8RPEC9CPR"
}
# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

st.set_page_config(
page_title="WoofHealth",
page_icon="🐕"
)

#Background & Sidebar Customizations
st.checkbox("Use url", value=True):
    add_logo("https://ibb.co/y0QSxQg")

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''

    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://s29938.pcdn.co/wp-content/uploads/2021/02/Wallpaper-Linz-Doggies-Green-1.jpg.optimal.jpg");
             background-size: cover
             opacity = 0.2;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack_url()

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #eb9761;
    }
</style>
""", unsafe_allow_html=True)

#Background & Sidebar Customizations

#################################################################################################################################################

#Make it rain dogs
rain(
    emoji="🐕",
    font_size=24,
    falling_speed=10,
    animation_length="infinite",
)




# Authentication
choice = st.sidebar.selectbox('Log In or Sign Up', ['Login', 'Sign up'])

# Obtain User Input for email and password
email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password',type = 'password')

# App

# Sign up Block
if choice == 'Sign up':
    handle = st.sidebar.text_input(
        'Enter Your User Name', value='Default...')
    submit = st.sidebar.button('Create An Account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your Account Is Created Successfully!')
        st.balloons()
        # Sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome' + ' ' + handle)
        st.info('Login Via Drop Down Selection')

# Login Block
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email,password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        bio = st.radio('Jump to',['Home','Pet Feed', 'Chat Bot', 'Settings', 'About'])

# SETTINGS PAGE
        if bio == 'Settings':
            # CHECK FOR IMAGE
            nImage = db.child(user['localId']).child("Image").get().val()
            # IMAGE FOUND
            if nImage is not None:
                # We plan to store all our image under the child image
                Image = db.child(user['localId']).child("Image").get()
                for img in Image.each():
                    img_choice = img.val()
                    #st.write(img_choice)
                st.image(img_choice)
                exp = st.expander('Change Bio and Image')
                # User plan to change profile picture
                with exp:
                    newImgPath = st.text_input('Enter full path of your profile imgae')
                    upload_new = st.button('Upload')
                    if upload_new:
                        uid = user['localId']
                        fireb_upload = storage.child(uid).put(newImgPath,user['idToken'])
                        a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                        db.child(user['localId']).child("Image").push(a_imgdata_url)
                        st.success('Success!')
            # IF THERE IS NO IMAGE
            else:
                st.info("No profile picture yet")
                newImgPath = st.text_input('Enter full path of your profile image')
                upload_new = st.button('Upload')
                if upload_new:
                    uid = user['localId']
                    # Stored Initated Bucket in Firebase
                    fireb_upload = storage.child(uid).put(newImgPath,user['idToken'])
                    # Get the url for easy access
                    a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                    # Put it in our real time database
                    db.child(user['localId']).child("Image").push(a_imgdata_url)
 # HOME PAGE
        elif bio == 'Home':
            col1, col2 = st.columns(2)

            # col for Profile picture
            with col1:
                nImage = db.child(user['localId']).child("Image").get().val()
                if nImage is not None:
                    val = db.child(user['localId']).child("Image").get()
                    for img in val.each():
                        img_choice = img.val()
                    st.image(img_choice,use_column_width=True)
                else:
                    st.info("No profile picture yet. Go to Edit Profile and choose one!")



                name = st.text_input("Enter Dog's Name", max_chars = 30)

                dog_breeds = [
                    "Afghan Hound",
                    "Airedale Terrier",
                    "Akita",
                    "Alaskan Malamute",
                    "American Bulldog",
                    "American Eskimo Dog",
                    "American Pit Bull Terrier",
                    "Australian Cattle Dog",
                    "Australian Shepherd",
                    "Basset Hound",
                    "Beagle",
                    "Bernese Mountain Dog",
                    "Bichon Frise",
                    "Bloodhound",
                    "Border Collie",
                    "Boston Terrier",
                    "Boxer",
                    "Bulldog",
                    "Bullmastiff",
                    "Cavalier King Charles Spaniel",
                    "Chihuahua",
                    "Chinese Crested",
                    "Chow Chow",
                    "Cocker Spaniel",
                    "Corgi",
                    "Dachshund",
                    "Doberman Pinscher",
                    "English Bulldog",
                    "French Bulldog",
                    "German Shepherd",
                    "Golden Retriever",
                    "Great Dane",
                    "Greyhound",
                    "Havanese",
                    "Jack Russell Terrier",
                    "Japanese Chin",
                    "Labrador Retriever",
                    "Lhasa Apso",
                    "Maltiff",
                    "Maltese",
                    "Miniature Pinscher",
                    "Miniature Schnauzer",
                    "Mongrel",
                    "Newfoundland",
                    "Old English Sheepdog",
                    "Pekingese",
                    "Pomeranian",
                    "Poodle",
                    "Pug",
                    "Rottweiler",
                    "Saint Bernard",
                    "Shar Pei",
                    "Shetland Sheepdog",
                    "Shih Tzu",
                    "Siberian Husky",
                    "Staffordshire Bull Terrier",
                    "Toy Poodle",
                    "Vizsla",
                    "Weimaraner",
                    "West Highland White Terrier",
                    "Whippet",
                    "Xoloitzcuintli",
                    "Yorkshire Terrier"
                ]

                selected_breed = st.multiselect("Select a dog breed", dog_breeds)
                st.write("You selected:", selected_breed)

                age = st.number_input("Enter Your Dog's Age", 1, 50)

                post = st.text_input("Let's share my current mood as a post!",max_chars = 100)
                add_post = st.button('Share Posts')
            if add_post:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                post = {'Name': name, 'Age':age, 'Breed': selected_breed, 'Post:' : post, 'Timestamp' : dt_string}

                results = db.child(user['localId']).child("Posts").push(post)
                st.balloons()

            # This coloumn for the post Display
            with col2:

                all_posts = db.child(user['localId']).child("Posts").get()
                if all_posts.val() is not None:
                    for Posts in reversed(all_posts.each()):
                            #st.write(Posts.key()) # Morty
                            st.code(Posts.val(),language = '')

        elif bio == 'About':

            st.write('## About This Project')
            st.markdown('<div style="text-align:justify;color:black;">Welcome to my Pet Health Monitoring System, WoofHealth!</div>', unsafe_allow_html=True)
            st.markdown("\n")

            st.markdown('<div style="text-align:justify;color:black;">My name is Taashwin Reddy, and I am the proud creator of this innovative platform. As a lifelong pet owner, I understand the importance of keeping our furry friends healthy and happy. Thats why I developed this system, to help pet owners keep a watchful eye on their pets health and well-being. With this system, you can easily track your pets diet, exercise, and medical records, all in one convenient location. You will receive alerts and reminders for important health check-ups and medication schedules.</div>', unsafe_allow_html=True)
            st.markdown("\n")

            st.markdown('<div style="text-align:justify;color:black;">Plus, the system provides you with personalized recommendations and resources to help you maintain your pets optimal health. \nAs a pet owner, I know how stressful it can be when your furry friend is not feeling well. That is why I made sure to include a section on the system that provides you with tips and advice on what to do if your pet seems unwell. And if you ever have any questions or concerns, you can reach out to me personally for support. Thank you for choosing my pet health monitoring system, and I hope you and your furry friend enjoy all the benefits it has to offer!</div>', unsafe_allow_html=True)
            st.markdown("\n")

            st.write('#### Benefits Of Using WoofHealth!')
            lst = ['Strengthen Your Bond With Your Doggo', 'Understand The Way They Perceive The World', 'Level Up Yourself As A Dog Owner']

            #List of Benefits
            s = ''

            for i in lst:
                s += "- " + i + "\n"

            st.markdown(s)


            #BUYMEACOFFEEBUTTON FUNCTION
            with st.sidebar:


                from streamlit.components.v1 import html
                button = """
                <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="winter24" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
                """

                html(button, height=70, width=220)

                st.markdown(
                    """
                    <style>
                        iframe[width="220"] {
                            position: fixed;
                            bottom: 45px;
                            right: 420px;
                        }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

        elif bio == "Chat Bot":
            # Set Streamlit page configuration
            #st.set_page_config(page_title='Woof Bot', layout='wide')
            # Initialize session states
            if "generated" not in st.session_state:
                st.session_state["generated"] = []
            if "past" not in st.session_state:
                st.session_state["past"] = []
            if "input" not in st.session_state:
                st.session_state["input"] = ""
            if "stored_session" not in st.session_state:
                st.session_state["stored_session"] = []

            # Define function to get user input
            def get_text():

                input_text = st.text_input("You: ", st.session_state["input"], key="input",
                                        placeholder="Ask me anything doggo related!",
                                        label_visibility='hidden')
                return input_text

            # Define function to start a new chat
            def new_chat():

                save = []
                for i in range(len(st.session_state['generated'])-1, -1, -1):
                    save.append("User:" + st.session_state["past"][i])
                    save.append("Bot:" + st.session_state["generated"][i])
                st.session_state["stored_session"].append(save)
                st.session_state["generated"] = []
                st.session_state["past"] = []
                st.session_state["input"] = ""
                st.session_state.entity_memory.store = {}
                st.session_state.entity_memory.buffer.clear()

            # Set up sidebar with various options

            with st.sidebar.expander("🛠️ ", expanded=False):
                MODEL = "gpt-3.5-turbo"
                K = st.number_input('Summary of prompts to consider',min_value=3,max_value=1000)

            # Set up the Streamlit app layout
            st.title("Hey There, I'm WoofBot 🐕")

            # Create an OpenAI instance
            llm = OpenAI(temperature=0,
                    openai_api_key="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",
                    model_name="gpt-3.5-turbo",
                    verbose=False)


            # Create a ConversationEntityMemory object if not already created
            if 'entity_memory' not in st.session_state:
                st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K )

            # Create the ConversationChain object with the specified configuration
            Conversation = ConversationChain(
                llm=llm,
                prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
                memory=st.session_state.entity_memory )

            # Add a button to start a new chat
            st.sidebar.button("New Chat", on_click = new_chat, type='primary')

            # Get the user input
            user_input = get_text()

            # Generate the output using the ConversationChain object and the user input, and add the input/output to the session
            if user_input:
                output = Conversation.run(input=user_input)
                st.session_state.past.append(user_input)
                st.session_state.generated.append(output)

            # Allow to download as well
            download_str = []
            # Display the conversation history using an expander, and allow the user to download it
            with st.expander("Conversation", expanded=True):
                for i in range(len(st.session_state['generated'])-1, -1, -1):
                    st.info(st.session_state["past"][i],icon="🧐")
                    st.success(st.session_state["generated"][i], icon="🤖")
                    download_str.append(st.session_state["past"][i])
                    download_str.append(st.session_state["generated"][i])

                # Can throw error - requires fix
                download_str = '\n'.join(download_str)
                if download_str:
                    st.download_button('Download',download_str)

            # Display stored conversation sessions in the sidebar
            for i, sublist in enumerate(st.session_state.stored_session):
                    with st.sidebar.expander(label= f"Conversation-Session:{i}"):
                        st.write(sublist)

            # Allow the user to clear all stored conversation sessions
            if st.session_state.stored_session:
                if st.sidebar.button("Clear-all"):
                    del st.session_state.stored_session
######################################################################################################################################################################
   # WORKPLACE FEED PAGE
        else:
            all_users = db.get()
            res = []
            # Store all the users handle name
            for users_handle in all_users.each():
                k = users_handle.val()["Handle"]
                res.append(k)
            # Total users
            nl = len(res)
            st.write('Total users here: '+ str(nl))

            # Allow the user to choose which other user he/she wants to see
            choice = st.selectbox('Pet Owners',res)
            push = st.button('Show Profile')

            # Show the choosen Profile
            if push:
                for users_handle in all_users.each():
                    k = users_handle.val()["Handle"]
                    #
                    if k == choice:
                        lid = users_handle.val()["ID"]

                        handlename = db.child(lid).child("Handle").get().val()

                        st.markdown(handlename, unsafe_allow_html=True)

                        nImage = db.child(lid).child("Image").get().val()
                        if nImage is not None:
                            val = db.child(lid).child("Image").get()
                            for img in val.each():
                                img_choice = img.val()
                                st.image(img_choice)
                        else:
                            st.info("No profile picture yet. Go to Edit Profile and choose one!")

                        # All posts
                        all_posts = db.child(lid).child("Posts").get()
                        if all_posts.val() is not None:
                            for Posts in reversed(all_posts.each()):
                                st.code(Posts.val(),language = '')

##################################################################################################################################

 # ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
