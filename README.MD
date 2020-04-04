# Vocabulary Trainer
The vocabulary trainer is a small application that supports Korean language learning.
It takes selected Korean web article URLs as an input, extracts key vocabulary from those articles, and then displays flash cards for learning that vocabulary.

The goal is to better understand the Korean article afterwards.

![](vocabtrainer.png)  


## Getting Started
To run the application locally, clone the repo, and then run:  
`python manage.py runserver`


## Prerequisites
See requirements.txt

## Notes
The app uses the googletrans python module for looking up term translations.  
There is still work to be done in terms of source term preprocessing, contextualizing translations etc.

## References
https://pypi.org/project/googletrans/


### Author
Heidi Duchting | https://www.linkedin.com/in/heididuchting/
