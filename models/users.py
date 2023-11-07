class User():
    """
    This class represents a user object.

    Attributes:
        id (int): The customer's unique identifier.
        first name (str): The customer's first name.
        last name (str): The customer's last name.
        email (str): The customer's email address.
        bio (str): The customer's bio.
        username (str): The customer's username.
        password (str): The customer's password.
        user image (url): The customer's image.
        created_on data (int): Date the customer was created.
        active (bool): Is user active or not.
    """

    def __init__(self, id, first_name, last_name, email, bio, username, password, profile_image_url, created_on, active):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.bio = bio
        self.username = username
        self.password = password
        self.profile_image_url = profile_image_url
        self.created_on = created_on
        self.active = active
        

# Creating a new Customer object
new_user = User(
    1, "John", "Smith", "jsmith@email.com", "I love to mountain bike", "jsmith", "password",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQX6aiBxhteng980rfwzcL7xz8EXnR3eN3K4Q&usqp=CAU", 
    "10/3/23", True)
