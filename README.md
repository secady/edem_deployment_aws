# edem_deployment_aws

This is Bootcamp final project in which we, as Data Science students worked together with Full Stack, Cibersecurity and UX/UI students to create a social media app for EDEM (Escuela de Empresarios).
The objective of the app was to engage students with the Marina de Empresas' ecosystem (EDEM, Lanzadera and Angels).

Here are the tasks done by Data Science team:
1. We created a PostgreSQL database on AWS RDS that contains EDEM students profile and the program studies they enroll in. Due to data protection and privacy issue, we didn't have any access to EDEM's student database.
   So, our database was created using synthetic/artificial data based on the figures provided by the client (EDEM).
2. We provided the following data: 
   - Student database
   - Event database
   - Lanzadera's startup company database --> we collected this data using web scraping technique
   - Recommendation to add friends --> we used Machine Learning for this task
   - Event recommendation --> We used our own code for this task
   - Bad words filter to ensure that all the posts in the social media post do not contain inappropriate words --> we used a NLP library for this task
3. All the above data was provided through API (Application Programming Interface) to the Full-Stack team in which we used AWS EC2 Virtual Machine for cloud deployment.
