#box(
  stroke: 2pt + black,
  inset: 16pt,
  width: 100%
  // padding: 4pt,
  // background: lightgray
)[
  #align(center, text(48pt, weight: "bold")[
        Programming Project Write-up
  ])
 // #align(center, text(18pt, weight: "regular")[ The alternative and more complete guide to python programming ])
]

#pagebreak()
= Analysis
(still working on the structure diagram with pikchr, the svg is being a bit strange right now, i'll fix it soon)
#image("svg-diagram.svg")
//
== The problem
- Write a backend and a frontend for robust user authentication, implementing modern security.

== Success critera
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
