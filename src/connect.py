import snowflake.connector

ctx = snowflake.connector.connect(user='WFM_USER',
                                  password='3LpNAYnLpW79',
                                  account='confie',
                                  role='WFM_ROLE',
                                  warehouse='DS_WH',
                                  database='DATA_ANALYTICS',
                                  schema='WFM_WORKSPACE')
