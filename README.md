# StudyFlow Task Planner

## Project Overview

StudyFlow Task Planner is a Django web application designed to help students organize schoolwork across multiple courses. The application lets a registered user create courses, add academic tasks for each course, assign due dates, choose priority levels, update progress status, and view a dashboard that summarizes what still needs attention. The goal is to give students one simple place to manage assignments, study goals, and project steps without needing a complicated project management tool.

This project matches my Lesson 13 Assignment 1 capstone plan. In that plan, I proposed an academic task planning application with Course and Task models, user authentication, a dashboard, a JavaScript-powered no-refresh completion button, a Django JsonResponse endpoint, and a responsive layout for mobile screens. The finished project follows that plan closely so the planning document and the completed application describe the same idea.

## Distinctiveness and Complexity

StudyFlow is distinct from the other standard course projects because it is not a social network, not an e-commerce store, and not a simple one-table CRUD application. It is an academic planning tool that organizes related information around real student responsibilities. The user is not posting to a public feed, following other users, or buying products. Instead, the main purpose is personal task organization. Every course belongs to a specific logged-in user, and every task belongs to a specific course. That means the app has a clear real-world structure: one student can have many courses, and each course can contain many assignments or study tasks.

The project is genuinely more complex than a basic CRUD app because it combines several course concepts at the same time. First, it uses related database models with ownership rules. A Course is connected to Django's built-in User model through a ForeignKey, and a Task is connected to Course through another ForeignKey. The views filter the database so students only see their own data. Second, the dashboard is more than a record list. It calculates total tasks, completed tasks, and a progress percentage, then displays those values in summary cards. Third, the JavaScript feature allows a user to mark a task complete or reopen it without refreshing the page. The button sends a fetch() request to a Django API endpoint, the endpoint returns JsonResponse data, and JavaScript updates the DOM by changing the task status, button text, card styling, and progress numbers.

Another important complexity is the responsive interface. The dashboard uses cards and grids that display nicely on a laptop, but the CSS media query changes the layout into a single-column phone view on smaller screens. Forms, navigation links, and action buttons are adjusted so they remain usable on a narrow viewport. This makes the project feel like a complete application instead of only a classroom exercise.

## File Structure and What Each File Does

`manage.py` is the standard Django command file used to run the development server, create migrations, apply migrations, and run tests.

`requirements.txt` lists the Python dependency for this project. It includes Django so another person can install the correct package before running the app.

`.gitignore` prevents local environment files, Python cache files, and the SQLite database from being pushed accidentally.

`.github/workflows/django.yml` is an optional GitHub Actions workflow. It installs dependencies, checks migrations, applies migrations, and runs tests when code is pushed.

`myproject/settings.py` contains the project settings, installed apps, middleware, database configuration, static file settings, and login redirect settings.

`myproject/urls.py` connects the project-level URL configuration to the StudyFlow app URLs and the Django Admin.

`myproject/asgi.py` and `myproject/wsgi.py` are standard Django deployment entry files.

`studyflow/models.py` defines the Course and Task models. Course stores a user's class information, and Task stores assignment details such as title, description, due date, priority, and status.

`studyflow/forms.py` defines RegisterForm, CourseForm, and TaskForm. These forms collect and validate user input for registration, course creation, and task creation or editing.

`studyflow/views.py` contains all main application logic. It includes dashboard, registration, course list, course create, task create, task detail, task edit, task delete, and the JSON task toggle API view.

`studyflow/urls.py` maps readable URL paths to the correct views. Templates use `{% url %}` instead of hardcoded links.

`studyflow/admin.py` registers Course and Task in Django Admin so the data can be reviewed and managed during testing.

`studyflow/tests.py` includes basic tests for model relationships, login protection, and the JSON toggle endpoint.

`studyflow/migrations/0001_initial.py` creates the database tables for Course and Task.

`studyflow/templates/studyflow/layout.html` is the base template. It uses `{% block %}` so all other pages can extend the same layout.

`studyflow/templates/studyflow/dashboard.html` displays the main dashboard, summary cards, progress bar, filters, and task cards. It uses `{% for %}`, `{% if %}`, and `{% url %}`.

`studyflow/templates/studyflow/register.html` and `login.html` provide authentication pages.

`studyflow/templates/studyflow/course_list.html` lists all courses owned by the signed-in user.

`studyflow/templates/studyflow/course_form.html` and `task_form.html` display Django forms for adding courses and tasks.

`studyflow/templates/studyflow/task_detail.html` displays one task with full details and action buttons.

`studyflow/static/studyflow/styles.css` controls the complete visual design, including cards, forms, buttons, navigation, progress bars, and mobile responsiveness.

`studyflow/static/studyflow/script.js` contains the JavaScript logic for the no-refresh task status feature. It listens for click events, sends fetch() requests, receives JSON data, and updates the DOM.

## How to Run the Application

1. Download or clone the project repository.
2. Open a terminal in the root folder where `manage.py` is located.
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment. On Windows, run `venv\Scripts\activate`. On Mac or Linux, run `source venv/bin/activate`.
5. Install dependencies: `pip install -r requirements.txt`
6. Apply migrations: `python manage.py migrate`
7. Create an admin account if you want to use Django Admin: `python manage.py createsuperuser`
8. Start the development server: `python manage.py runserver`
9. Open the local site in your browser at `http://127.0.0.1:8000/`.
10. Register a new account, create a course, add tasks, and test the dashboard.

## How to Test the Application

Run the test suite with this command:

```bash
python manage.py test
```

The tests check that the Course and Task relationship works, that the dashboard requires login, and that the JavaScript API endpoint returns JSON after toggling a task's status.

## JavaScript and API Explanation

The main interactive feature is the task completion button on the dashboard. When the user clicks the button, `script.js` handles the click event and sends a POST request with fetch() to `/api/tasks/<id>/toggle/`. The Django view checks that the task belongs to the signed-in user, changes the status to Completed or In Progress, saves the task, recalculates progress totals, and returns a JsonResponse. JavaScript then updates the task card, the visible status label, the button text, the completed count, and the progress bar without a full page reload.

## Mobile Responsiveness

The application is mobile-friendly through CSS media queries. On wide screens, task cards and summary cards appear in multi-column grids. On small screens, the layout stacks into one column, the navigation becomes vertical, and buttons become easier to tap. This should be tested in browser DevTools using a mobile viewport before submission.

## Additional Information

For the final video, show the application live instead of walking through code. A strong video demo should begin with a slide or text showing the required edX and GitHub usernames, then demonstrate registration or login, course creation, task creation, the dashboard filter, the no-refresh Mark Complete button, and the responsive mobile viewport. The README is intentionally detailed because the assignment emphasizes that a short or vague README can cause the project to fail.
