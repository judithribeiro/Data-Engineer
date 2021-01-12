/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{
    config(
        materialized='table', bind=False
    )
}}

with source_data as (

    Select
    description,
    createdat,
    portal,
    price
    From {{ source('database_mvp_processed', 'zapimoveis') }}
    union all
    select
    descricao as description,
    extracted_at as createdat,
    'netimoveis' as portal,
    cast(valorimovel as varchar) as price
    From {{ source('database_mvp_raw', 'netimoveis') }}
)

select
    description::varchar,
    createdat::varchar,
    portal::varchar,
    price::varchar
from source_data




/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
