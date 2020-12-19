# Vulnerable Django

This project is part of the Securing Software course. This app is insecure by design and only exists to highlight some of the more common security flaws in the wild.

## Tech Stack

| Tech        | Purpose |
| ----------- | ------- |
| Framework   | Django  |
| CSS library | Bulma   |

## How to get started

To install the project you need to have django and django-widget-tweaks installed and then you just run the migrations with python3 manage.py and then start the server with python3 manage.py runserver.

## Vulnerabilities

### Flaw 1. Broken Access Control

This project has broken access control as the user can send messages even without a log in. This is due to the fact that the endpoint isn't properly restricted to the users that should have access to it. It should also check if the user sending the message even exists. Currently the endpoint works even with non-existent users.

The easiest way to fix this would be to add the @login_required annotation for that method.

### Flaw 2. Injection (SQL)

SQL injection can occur when malicious data is sent to an interpreter as part of the input. In this case the user can input data in an input field that is the added to the SQL query as is. Exploiting this is therefore trivial and allows the attacker to fetch admin passwords or even destroy the database. In this project the user id for the receiver of the message is fetched with a easy to exploit SQL query.

This can be solved by sanitizing, escaping and parameterizing the inputs before passing those to the SQL query. Even easier solution would be to use the object relation mapper included in the Django framework as it does all of it by itself. Especially in this case the SQL query is redundant because the query is simple enough.

### Flaw 3. Cross-Site Scripting (XSS)

XSS occurs when an application includes untrusted data in a new web page without proper validation or escaping. This allows the attackers to execute scripts in the victim’s browser and therefore do whatever the user could do, for example hijack the user session. In this case the attacker can drop a script in the message box. This script is then saved to the database and loaded whenever the page is loaded.

Django protects against XSS attacks by default, at least to an extent, by escaping all inputs to the html templates. In this case it would be enough to remove the "safe" word from the HTML tag where Django dynamically includes the sent messages. Then the script wouldn't be executed in the browser but would instead be shown as just text.

### Flaw 4. Insufficient logging and monitoring

This project has no logging enabled. This means that attackers can easily hide their tracks, maintain persistence and tamper with or destroy data. It is almost impossible to detect as no trail is left behind.

This would be easy to solve by using a logging middleware that logs all the requests made to the server. Additional logging could be included by hand to all or at least the sensitive endpoints. There should also be some kind of monitoring for the logging requests so that brute forcing could be easily detected and the harmful IPs banned.

### Flaw 5. Security Misconfiguration

Django has decent security configurations by default. In this case these settings have been changed to being worse in a way that allows various sorts of attacks. For example there's password or username rules so the user can input any password and it will be accepted. This leads to users using insecure passwords such as "password" or "123456". Attacker can then easily hijack the accounts of the users by trying common passwords and usernames by brute force. Also the given session tokens do not expire (set to expire in 10 000 000 seconds) that could also lead to issues. For example an attacker could hijack a session token and use it indefinitely. Django's secret key is also exposed in the settings file that is included in the version control system in an open source project. It would be a good practice to always keep sensitive data out of the VCS but in an open source project is an absolute necessity. This project also is run in DEBUG mode even in production. This allows the attacker to see detailer error pages and easily gain more knowledge of the stack for further attacks.

To fix this it would be enough to revert to django's default configurations. By default it checks the users passwords against both known easy passwords as well as against the username so the user can't just use the username as the password. Session token also have a more limited lifespan. The secret key could be replaced with an environment variable that could be supplied elsewhere. Same should be done for the DEBUG flag as it makes sense to have it on in the development environment but off in the production.
