# GCSE Extended Programming Project

## Analysis
The goal of this mini-project is the write a backend and frontend for robust, local, user authentication: implementing modern security. 
### Success critera
- Provide a mostly intuitive user interface (not just a cli tool)
    - Something like a TUI
    - The UI must handle user error gracefully
- Separate the fronted and backed
    - The backend need not know of the frontend
    - Use dependency injection over inheritance
- Have the option to sign in and to sign up, and when signing in, if the user provided an email address and a username, they can use either to sign in
- Use modern hashing algorithms (hashing the password using SHA256 or similar, not just MD5) to store the password, the password must NEVER be kept in plain text
- Store the user credentials in a separate file (a 'database' if you will)
- Helpfully suggest options through the frontend menu system, such as to generate a random password, either randomly or invoking a tool like diceware.
- Allow code to be reusable and useable for other projects that require user auth.
### Main parts
There will be two main sections:
- Backend
- Frontent

The backend handles the database and the password/username lookups, and the frontend provides the user-facing side, with the input fields and text boxes in the terminal. 

## Design
I have not included a full flowchart because the program is quite large, however here's a part of the logic, in a more high-level overview rather than specific implementation, nevertheless showing the processes: 
```
flowchart TD
    A([Start TUI]) --> B[/Display Menu: Sign In, Sign Up, Exit/]
    B --> C{Menu Option?}
    C -->|Sign In| D[/Get username & password/]
    C -->|Sign Up| H[/Get username & password twice/]
    C -->|Exit| Z[[Save users and exit]]
    D --> E{User exists?}
    E -->|No| F[/Display "User not found"/]
    F --> B
    E -->|Yes| G{Password correct?}
    G -->|No| I[/Display "Password incorrect"/]
    I --> B
    G -->|Yes| J[/Display "Sign in successful"/]
    J --> K[[Call signed_in]]
    K --> B
    H --> L{User exists?}
    L -->|Yes| M[/Display "User already exists"/]
    M --> B
    L -->|No| N[[Create user object]]
    N --> O[[Add user to backend]]
    O --> P[/Display "User added successfully"/]
    P --> K
```

## Implementation
The fully coded solution to this program is available [here](src/auth.py).
## Testing
Proper testing would involve writing unit tests that would take up approximately 30% of the codebase, and live next to the code, but for this mini-project I just put a simple testing table:
|Test number | Test description | Expected outcome | Actual outcome |
| -----       | -------------- | ----------------- | ------------- |
| 1. | 

## Evaluation

