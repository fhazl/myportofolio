### Assignment 1

1. section element helped me make an additional row for the new skill section I was adding. The section makes it so the skill section stays tidy and aligns with the middle of the screen. 
2. The skill grid would go out of bounds on mobile browser viewing. So, I made the skill column have a hard limit so it will go down instead of sideways if the browser width is too small.
3. It feels limiting when I want to add more interesting animations.  In the next iteration I want to make appearing and disappearing animation when the img scroll out of view.

### Assignment 2
1. a. The browser sends a request to the server for a page (landing page/experience/education)
b. urls.py (Root): Gives access to database
c. Application urls.py: Routes request to a url
d. View: Fetches and manages the processing of objects
e. Model: Defines data with clases to create objects
f. Template: Turns the objects to visual display
2. - Single Responsibility Principle: Each file should have one responsibility. Model being the one storing data and Template being the one that turns data into UI.
-Scalability and Troubleshooting: When each file has it's own responsibility, it will be easier to add new responsibility with new files and identify problems.
3. makemigrations create the tool for database changes and migrate executes it. For example, when adding experience to models.py, makemigrations detects you made changes and migrate adds those changes to the database
### Week 3 Logs

Added CRUD for experience, education and project.

While, AI makes it easier to create code duplication for similar html files like education_delete_modal.html, AI did not see that we used UUID instead of integer based id.

### Assignment 3
1. We use ModelForm for the sake of reusability. Instead of creating a project/skill one by one, we can simply input data that outputs an object from a model. Additionally, we need csrf_token so that we can check if an action is performed by the user.
2. JSON is much more efficient than XML because XML uses tag markers which makes it harder for people to read and machine to parse compared to key, value format of json.
3. The browsers sends a request to the function path in view. Then view access the database, converting the database object into JSON. Finally, the server returns the JSON file to the browser.
Serialization is needed because it makes Python database objects easier to understand by machine in the format of JSON