import streamlit as st
import pandas as pd
import json
import os

# File path to store the library
LIBRARY_FILE = 'library.txt'

# Load the library from the file
def load_library():
    """Load library from a file."""
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as file:
            try:
                library = json.load(file)
            except json.JSONDecodeError:
                library = []  # In case the file is empty or corrupted
    else:
        library = []
    return library

# Save the library to the file
def save_library():
    """Save library to a file."""
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(st.session_state.library, file, indent=4)
    st.success("📚 Library saved to file!")

# Initialize the session state with the library data
if 'library' not in st.session_state:
    st.session_state.library = load_library()

def add_book(title, author, year, genre, language, read_status):
    """Add a new book to the library."""
    if not language:  # If language is not provided, set it to "Unknown"
        language = "Unknown"
        
    book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'language': language,
        'read_status': read_status
    }
    st.session_state.library.append(book)
    st.success(f"📖 Book '{title}' added successfully!")

def remove_book(title):
    """Remove a book from the library by title."""
    books_to_remove = [book for book in st.session_state.library if book['title'].lower() == title.lower()]
    if books_to_remove:
        st.session_state.library = [book for book in st.session_state.library if book['title'].lower() != title.lower()]
        st.success(f"🗑️ Book '{title}' removed successfully!")
    else:
        st.error(f"❌ Book '{title}' not found!")

def search_books(keyword):
    """Search for books by title or author."""
    results = [book for book in st.session_state.library if keyword.lower() in book['title'].lower() or keyword.lower() in book['author'].lower()]
    return results

def display_statistics():
    """Display statistics about the library."""
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read_status'])
    if total_books > 0:
        percentage_read = (read_books / total_books) * 100
    else:
        percentage_read = 0
    st.write(f"Total Books: {total_books}")
    st.write(f"Books Read: {read_books} ({percentage_read:.2f}%)")

def display_all_books():
    """Display all books in the library."""
    if len(st.session_state.library) == 0:
        st.write("🚫 No books in the library.")
    else:
        for i, book in enumerate(st.session_state.library, 1):
            status = "Read" if book['read_status'] else "Unread"
            # Use 'Unknown' if the 'language' key is missing
            language = book.get('language', 'Unknown')  
            st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {language} - {status}")

def clear_session():
    """Clear session state to simulate exit."""
    st.session_state.library = []  # Clear the library
    st.write("❌ Session cleared. Exiting...")

# Streamlit UI with styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f8ff;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 16px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>input {
        background-color: #e0f7fa;
        border-radius: 8px;
        font-size: 14px;
    }
    .stTextInput>label {
        color: #00796b;
    }
    .stSelectbox>div>div>input {
        background-color: #e0f7fa;
        border-radius: 8px;
        font-size: 14px;
    }
    .stSelectbox>label {
        color: #00796b;
    }
    .stMarkdown {
        color: #00796b;
    }
    .stSelectbox, .stTextInput, .stButton {
        margin-bottom: 20px;
    }
    .stSuccess, .stError {
        color: #ffffff;
        background-color: #00796b;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stTextInput>div>input:focus {
        border: 2px solid #00796b;
    }
    .stSelectbox>div>div>input:focus {
        border: 2px solid #00796b;
    }
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #e0f7fa;
    }
    .stSidebar>div {
        background-color: #b2dfdb;
        padding: 20px;
        border-radius: 10px;
    }
    .css-10trblm {
        font-size: 20px;
        color: #004d40;
    }
    /* Footer Styling */
    footer {
        font-size: 16px;
        color: #ffffff;
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        background-color: #00796b; /* Green color background */
        border-radius: 10px;
    }
    footer p {
        margin: 0;
    }
    footer a {
        color: #ffeb3b; /* Yellow color for the link (if you add a link) */
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('📖 Personal Library Manager📚')

# Sidebar Menu 
menu = st.sidebar.selectbox('📚 Choose an option:', [
    '🏠 Home',
    '➕ Add a book', 
    '🗑️ Remove a book', 
    '🔎 Search for a book', 
    '📑 Display all books', 
    '📊 Display statistics', 
    '🔚 Exit'
])

if menu == '🏠 Home':
    st.markdown("### 📖 Welcome to your Personal Library!")
    st.write("Manage your books effortlessly!")

elif menu == '➕ Add a book':
    st.subheader('➕ Add a new book')
    title = st.text_input("📘 Enter book title: ")
    author = st.text_input("✍️ Enter author: ")
    year = st.number_input("📅 Enter publication year:", min_value=0, max_value=2025, step=1)
    genre = st.text_input("📚 Genre (e.g. Fiction, Non-Fiction, Fantasy):")
    language = st.text_input("🌍 Language (e.g. English, Spanish):")
    read_status = st.selectbox("✅ Has the book been read?", ['Yes', 'No'])
    read_status = True if read_status == 'Yes' else False

    if st.button('Add Book'):
        add_book(title, author, year, genre, language, read_status)
        save_library()  # Save the library after adding a book

elif menu == '🗑️ Remove a book':
    st.subheader('🗑️ Remove a book')
    title = st.text_input("🔍 Enter the title of the book to remove: ")
    if st.button('Remove Book'):
        remove_book(title)
        save_library()  # Save the library after removing a book

elif menu == '🔎 Search for a book':
    st.subheader('🔎 Search for a book')
    search_option = st.radio("🔍 Search by:", ("Title", "Author"))
    
    if search_option == "Title":
        title = st.text_input("Enter book title to search for: ")
        if st.button("Search by Title"):
            results = search_books(title)
            if results:
                st.write("### Matching Books: ")
                for i, book in enumerate(results, 1):
                    status = "Read" if book['read_status'] else "Unread"
                    language = book.get('language', 'Unknown')  # Handle missing language
                    st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {language} - {status}")
            else:
                st.write("🚫 No books found with that title.")

    elif search_option == "Author":
        author = st.text_input("Enter author name to search for: ")
        if st.button("Search by Author"):
            results = search_books(author)
            if results:
                st.write("### Matching Books: ")
                for i, book in enumerate(results, 1):
                    status = "Read" if book['read_status'] else "Unread"
                    language = book.get('language', 'Unknown')  # Handle missing language
                    st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {language} - {status}")
            else:
                st.write("🚫 No books found by that author.")

elif menu == '📑 Display all books':
    st.subheader('📑 Your Library: ')
    display_all_books()

elif menu == '📊 Display statistics':
    st.subheader('📊 Library Statistics')
    display_statistics()

elif menu == '🔚 Exit':
    st.subheader('🔚 Exit')
    if st.button('Clear Library & Exit'):
        st.write("👋 Exiting... Thank you for using the Library Manager!")
        save_library()  # Save the library before exiting
        clear_session()  # Clear the library session
        st.stop()  # Stops further execution of the app

st.markdown(
    """
    <footer>
        <p>✨ Created by Nimra Ulfat 💻📚</p>
    </footer>
    """,
    unsafe_allow_html=True
)
