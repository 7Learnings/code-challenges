# 7Learnings DevOps Code Challenges

The 7Learnings code challenge is an opportunity to demonstrate proficiency in the problem solving skills we expect you to use at 7Learnings.

## Coding environment

At 7Learnings, we use Python 3.10 as the main coding language. So it's strongly encourage to create isolated Python using [virtualenv](https://virtualenv.pypa.io/en/latest/) to prepare yourself for the following challenges.
You will need a Google account and enable [default application credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc#local-dev) locally before running the code snippet below.

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

We also provide a helper function (`table_to_parquet`) in the `utils.py` to let you focus on the challenges. But feel free to change it if you find a better way to do it. You can find example code below.

```python
from google.cloud import bigquery_storage as bqs
from utils import table_to_parquet

table_to_parquet(
    bqs.BigQueryReadClient(), "candidate-01-7l.devops.transactions", "downloaded_data"
)
```

## The Challenge

The challenge is to implement a "pipeline" command that prepares data for model training. 
It does so in two steps: `get-data` and `check-data`.

`get-data` retrieves the data from a BigQuery table and stores it locally. 
As mentioned above, helper method that returns a parquet file given a BigQuery table is already provided for your convenience.

You will need to modify `get-data` step for the following tasks:

  1a. Table is relatively big with ~5 million rows. It contains train, evaluation and test datasets.
      Split parquet file into 3 separate (in-memory) datasets: train, eval, test. 
      Use `_data_split` column to determine which dataset the sample should correspond to.

  1b. Shuffle datasets according to `_data_shuffle` column in a reproducible way.
      Row order after shuffling needs to be the same between separate runs.

`check-data` makes sure that training and evaluation datasets are similarly distributed.
There is only one task to implement in this step:

  2. Compare distributions between train and eval datasets.
     Raise an error or display a warning if distributions are significantly different.

     (Optional) In case of significantly different distributions, plo


Feel the task is too easy? We have a bonus task for you.
It would be nice if splitting and sorting by the `_data_split` and `_data_shuffle` columns would already happen when when writing to the parquet files, so we could stream it during model training.

#### Time Allotment

We respect your time and don't want you spending more 3 hours on your challenge. We just want to get a sense of your thought process and development patterns. If there are features you don't have time to implement, feel free to use pseudo code to describe the intended behavior.

## What We Review

Your code will be reviewed by our engineers. The aspects of your code we will judge include:

- ability to get the technical environment set up
- completion of tasks
- code cleanness
- reasoning of the solution

## Submission

Email a link to a repository with your implementation or zip file with your repository to your 7Learnings contact.