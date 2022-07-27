# 7Learnings DevOps Code Challenges

The 7Learnings code challenge is an opportunity to demonstrate proficiency in the problem solving skills we expect you to use at 7Learnings.

## Coding environment

At 7Learnings, we use Python 3.10 as the main coding language. So it's strongly encourage to create isolated Python using [virtualenv](https://virtualenv.pypa.io/en/latest/) to prepare yourself for the following challenges.

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

#### Time Allotment

We respect your time and don't want you spending more 3 hours on your challenge. We just want to get a sense of your thought process and development patterns. If there are features you don't have time to implement, feel free to use pseudo code to describe the intended behavior.


