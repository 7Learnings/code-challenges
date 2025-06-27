# 7Learnings backend Code Challenges

The 7Learnings code challenge is an opportunity to demonstrate proficiency in the problem solving skills we expect you to use at 7Learnings.

## Coding environment

At 7Learnings, we use Python 3.12 as the main coding language. So it's strongly encouraged to create isolated Python environment using [virtualenv](https://virtualenv.pypa.io/en/latest/) to prepare yourself for the challenge.

First, create a python environment and install required packages:

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Include any additional dependencies you need in `requirements.txt`.

## The Challenge

In this Django project, it already contains 2 Django models, dummy data and basic setup.

1. Category
2. Book

The **first task** is to migrate `tags` field (semicolon separated string) from existing `Book` model to seperated Django model. You're free to modify the Book model and decide fields in the new model.


The **second task** is implementation the following APIs (using [Django Ninja](https://django-ninja.dev/)):

1. List all Category
2. List all Tag
3. Create Book

### Time Allotment

We respect your time and don't want you spending more 3 hours on your challenge. We just want to get a sense of your thought process and development patterns. If there are features you don't have time to implement, feel free to use pseudo code to describe the intended behavior.

## What We Review

Your code will be reviewed by our engineers. The aspects of your code we will judge include:

- ability to get the technical environment set up
- completion of tasks
- code cleanness
- reasoning of the solution

## Submitting your results

Send us your final code, preferably as either one of the following:
- git-bundle: `git bundle create my_changes.bundle origin/main..`
- patches: `git format-patch origin/main..`
