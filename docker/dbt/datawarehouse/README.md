Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](http://slack.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


CREATE EXTERNAL SCHEMA glue_data_lake_processed
FROM DATA CATALOG
DATABASE 'database_mvp_processed'
REGION 'us-east-2'
iam_role 'arn:aws:iam::736529293817:role/redshift-IamProductionRedshiftSpectrumRole-LGW3N55ZVXBV'
;


CREATE EXTERNAL SCHEMA glue_data_lake_raw
FROM DATA CATALOG
DATABASE 'database_mvp_raw'
REGION 'us-east-2'
iam_role 'arn:aws:iam::736529293817:role/redshift-IamProductionRedshiftSpectrumRole-LGW3N55ZVXBV'
;