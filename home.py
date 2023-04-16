import streamlit as st
import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page
import base64
from PIL import Image
from pyrebase import pyrebase
from datetime import datetime
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from streamlit_extras.let_it_rain import rain
from streamlit_extras.badges import badge
###################################################################################################

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

#Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Database
db = firebase.database()
storage = firebase.storage()


with st.sidebar.container():
    image = Image.open(r"C:\Users\taash\Downloads\FYPAPP\WoofHealth Logo.png")
    st.image(image, use_column_width=True)

#st.sidebar.image(r"C:\Users\taash\Downloads\FYPAPP\WoofHealth Logo.jpg", use_column_width=True)

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

st.sidebar.title("Welcome To WoofHealth!")


#Authentication
choice  = st.sidebar.selectbox('Log In/Sign Up/Log Out', ['Log In', 'Sign Up', 'Log Out'])

email = st.sidebar.text_input('Please Enter Your Email Address')
password = st.sidebar.text_input('Please Enter Your Password', type = "password")

if choice == 'Sign Up':
    handle = st.sidebar.text_input('Please Input Your User Name', value = 'Default')
    submit = st.sidebar.button('Create My Account')

    if submit:
        user = auth.create_user_with_email_and_password(email,password)
        st.success('Your Account Is Created Successfully')
        st.balloons()
        #SignIn
        user = auth.sign_in_with_email_and_password(email,password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome' + " " + handle)
        st.info('Login Via The Dropdown Option In The Sidebar!')

if choice == 'Log In':
    #login = st.sidebar.checkbox('Log In')
    login = st.sidebar.button('Log In')
    if login:
        user = auth.sign_in_with_email_and_password(email,password)
        st.success('You Have Successfully Logged In!')
        st.balloons()

        bio = st.radio('Jump to',['Home','Pet Feed', 'ChatBot', 'About', 'Settings'])

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
                exp = st.beta_expander('Change Bio and Image')
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

                post = st.text_input("Let's share my current mood as a post!",max_chars = 100)
                add_post = st.button('Share Posts')
            if add_post:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                post = {'Post:' : post,
                        'Timestamp' : dt_string}
                results = db.child(user['localId']).child("Posts").push(post)
                st.balloons()

            # This coloumn for the post Display
            with col2:

                all_posts = db.child(user['localId']).child("Posts").get()
                if all_posts.val() is not None:
                    for Posts in reversed(all_posts.each()):
                            #st.write(Posts.key()) # Morty
                            st.code(Posts.val(),language = '')


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
            choice = st.selectbox('My Collegues',res)
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


#############################################################################################################################################################
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
            """
            Get the user input text.
            Returns:
                (str): The text entered by the user
            """
            input_text = st.text_input("You: ", st.session_state["input"], key="input",
                                    placeholder="Ask me anything doggo related!",
                                    label_visibility='hidden')
            return input_text

        # Define function to start a new chat
        def new_chat():
            """
            Clears session state and starts a new chat.
            """
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
                st.download_button('Download The Answers/Replies',download_str)

        # Display stored conversation sessions in the sidebar
        for i, sublist in enumerate(st.session_state.stored_session):
                with st.sidebar.expander(label= f"Conversation-Session:{i}"):
                    st.write(sublist)

        # Allow the user to clear all stored conversation sessions
        if st.session_state.stored_session:
            if st.sidebar.button("Clear-all"):
                del st.session_state.stored_session


#    add_radio = st.radio(
#        "Choose Your Preferred Chatbot",
#        ("Normal (Standard Dog Only Info)", "Extreme (ChatGPT-Fied)")
#    )



 # ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
