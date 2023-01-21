Starting backend on 01.10.23.

2pm - getting backend set up. Wire frames and data structures have been created.
Created data models
Added environmental variables

01.11.23
Spent today doing lots of research on React w/ Typescript
Got basic CRUD routes working for both data models (requests and holdings)

1.12.23
Spent today working on the auth backend, and working through some basic Typescript tutorials.

1.13.23
Today's goals will be to work on Typescript React frontend, and access all API endpoints. See notes in frontend readme.

1.14.23
Started integrating Plaid Link features.

1.16.23
1. need to create endpoint that user sends their ID to, which then (via middleware) requests a Plaid Link token, and sends it back to user client.
2. Need to add middleware that will make response to above endpoint include a temporary link token
Both items were completed.

1.17.23
This was a busy backend day. Completed:
1. Basic Plaid Link token exchange
2. Ability to request account data based on user ID
3. Ability to transfer holdings object from Plaid to my postgres SQL server completed
4. Fully able to import data, and send to user on frontend.
5. Made changes needed for Heroku deployment.

At this point, the backend is generally complete.