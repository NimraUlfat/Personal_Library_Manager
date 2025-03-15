# Imports
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Database file
LIBRARY_DB = 'library.db'

# Create the database and table
def create_table():
    """Create books table in the database if it doesn't exist."""
    conn = sqlite3.connect(LIBRARY_DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        genre TEXT,
        language TEXT,
        read_status BOOLEAN
    )
    """)
    conn.commit()
    conn.close()

# Add a new book to the database
def add_book(title, author, year, genre, language, read_status):
    """Add a new book to the database."""
    conn = sqlite3.connect(LIBRARY_DB)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO books (title, author, year, genre, language, read_status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (title, author, year, genre, language, read_status))
    conn.commit()
    conn.close()
    st.success(f"📖 Book '{title}' added successfully!")

# Remove a book from the database
def remove_book(title):
    """Remove a book from the database by title."""
    conn = sqlite3.connect(LIBRARY_DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    st.success(f"🗑️ Book '{title}' removed successfully!")

# Update book details in the database
def update_book(title, new_read_status=None, new_genre=None):
    """Update book details (e.g., read status, genre)."""
    conn = sqlite3.connect(LIBRARY_DB)
    cursor = conn.cursor()
    
    if new_read_status is not None:
        cursor.execute("UPDATE books SET read_status = ? WHERE title = ?", (new_read_status, title))
    
    if new_genre is not None:
        cursor.execute("UPDATE books SET genre = ? WHERE title = ?", (new_genre, title))
    
    conn.commit()
    conn.close()
    st.success(f"📚 Book '{title}' updated successfully!")

# Retrieve and display books from the database in table format
def display_all_books():
    """Display all books in the library from the database in table format."""
    try:
        conn = sqlite3.connect(LIBRARY_DB)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        
        conn.close()  
        
        if len(books) == 0:
            st.write("🚫 No books in the library.")
        else:
            # Create a DataFrame for better table display
            books_df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Year", "Genre", "Language", "Read Status"])
            # Convert read status to "Read" or "Unread"
            books_df["Read Status"] = books_df["Read Status"].apply(lambda x: "Read" if x else "Unread")
            
            st.write("### Library Books")
            st.dataframe(books_df)  # Display the DataFrame in a table format
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")

# Search for books by title or author
def search_books(keyword):
    """Search for books by title or author."""
    conn = sqlite3.connect(LIBRARY_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    books = cursor.fetchall()
    conn.close()
    return books

# Calculate and display statistics
def display_statistics():
    """Display statistics about the library."""
    conn = sqlite3.connect(LIBRARY_DB)
    cursor = conn.cursor()

    # Count total books
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    # Count read books
    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = cursor.fetchone()[0]

    # Count unread books
    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 0")
    unread_books = cursor.fetchone()[0]

    # Get most frequent genres
    cursor.execute("SELECT genre, COUNT(*) FROM books GROUP BY genre ORDER BY COUNT(*) DESC LIMIT 5")
    genres = cursor.fetchall()

    # Get most frequent languages
    cursor.execute("SELECT language, COUNT(*) FROM books GROUP BY language ORDER BY COUNT(*) DESC LIMIT 5")
    languages = cursor.fetchall()

    conn.close()

    # Create a DataFrame for displaying the statistics
    stats_data = {
        "Stat": ["Total Books", "Read Books", "Unread Books"],
        "Count": [total_books, read_books, unread_books]
    }

    # Show statistics as table
    stats_df = pd.DataFrame(stats_data)
    st.write("### Library Statistics")
    st.table(stats_df)

    # Display most frequent genres
    st.write("### Most Frequent Genres")
    if genres:
        st.write(pd.DataFrame(genres, columns=["Genre", "Count"]))
    else:
        st.write("No genres found.")

    # Display most frequent languages
    st.write("### Most Frequent Languages")
    if languages:
        st.write(pd.DataFrame(languages, columns=["Language", "Count"]))
    else:
        st.write("No languages found.")


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
    /* Home Page Styling */
    .home-page-title {
        font-size: 40px;
        color: #00796b;
        font-weight: bold;
        text-align: center;
        margin-top: 30px;
        padding: 10px;
    }
    .home-page-description {
        font-size: 18px;
        color: #004d40;
        text-align: center;
        margin-top: 20px;
    }
    .home-page-statistics {
        font-size: 20px;
        color: #004d40;
        text-align: center;
        margin-top: 30px;
    }
    .home-banner {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
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

# Initialize the database
create_table()

if menu == '🏠 Home':
    st.markdown('<div class="home-page-title">Welcome to Your Personal Library 📚</div>', unsafe_allow_html=True)

    # Add a banner image
    st.image("https://static.vecteezy.com/system/resources/thumbnails/051/261/350/small_2x/library-desk-with-books-and-laptop-representing-education-technology-photo.jpeg", caption="Manage your books with ease!", use_container_width=True)

    st.markdown('<div class="home-page-description">Organize your collection of books, track your reading progress, and explore your library with ease!</div>', unsafe_allow_html=True)

    # Quick Statistics
    total_books = 0
    read_books = 0
    unread_books = 0

    conn = sqlite3.connect(LIBRARY_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 0")
    unread_books = cursor.fetchone()[0]

    conn.close()

    st.markdown(
        f"""
        <div class="home-page-statistics">
            <b>Total Books:</b> {total_books} <br>
            <b>Read Books:</b> {read_books} <br>
            <b>Unread Books:</b> {unread_books}
        </div>
        """, unsafe_allow_html=True)

elif menu == '➕ Add a book':
    st.subheader('➕ Add a new book')
    title = st.text_input("📘 Enter book title: ")
    author = st.text_input("✍️ Enter author: ")
    
    current_year = datetime.now().year
    year = st.number_input("📅 Enter publication year:", min_value=0, max_value=2025, step=1, value=current_year)
    
    genre = st.text_input("📚 Genre (e.g. Fiction, Non-Fiction, Fantasy):")
    language = st.text_input("🌍 Language (e.g. English, Spanish):")
    read_status = st.selectbox("✅ Has the book been read?", ['Yes', 'No'])
    read_status = True if read_status == 'Yes' else False

    if st.button('Add Book'):
        add_book(title, author, year, genre, language, read_status)

elif menu == '🗑️ Remove a book':
    st.subheader('🗑️ Remove a book')
    title = st.text_input("🔍 Enter the title of the book to remove: ")
    if st.button('Remove Book'):
        remove_book(title)

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
                    _, title, author, year, genre, language, read_status = book
                    status = "Read" if read_status else "Unread"
                    st.write(f"{i}. {title} by {author} ({year}) - {genre} - {language} - {status}")
            else:
                st.write("🚫 No books found with that title.")

    elif search_option == "Author":
        author = st.text_input("Enter author name to search for: ")
        if st.button("Search by Author"):
            results = search_books(author)
            if results:
                st.write("### Matching Books: ")
                for i, book in enumerate(results, 1):
                    _, title, author, year, genre, language, read_status = book
                    status = "Read" if read_status else "Unread"
                    st.write(f"{i}. {title} by {author} ({year}) - {genre} - {language} - {status}")
            else:
                st.write("🚫 No books found by that author.")

elif menu == '📑 Display all books':
    st.subheader('📑 Your Library: ')
    display_all_books()

elif menu == '📊 Display statistics':
    display_statistics()

elif menu == '🔚 Exit':
    st.subheader('🔚 Exit')
    if st.button('Clear Library & Exit'):
        st.write("👋 Exiting... Thank you for using the Library Manager!")
        st.stop() 

# Footer
st.markdown(
    """
    <footer>
        <p>✨ Created by Nimra Ulfat 💻📚</p>
    </footer>
    """,
    unsafe_allow_html=True
)
