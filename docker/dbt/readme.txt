Criar pasta dbt
pip install dbt
dbt init datawarehouse

cd /Users/resale/.dbt
alterou o profiles.yml ( configurações do Redshift no Secret Manager da Aws )
Altera o arquivo dbt_project.yml ( Nome do projeto, configurar o comportamento Ex: staging:materialized: ephemeral => imprimir na tela  ou  mart:materialized: table => salva na tabela )

Rodar no Redshift pra criar a referencia:
CREATE EXTERNAL SCHEMA glue_data_lake_processed
FROM DATA CATALOG
DATABASE 'database_mvp_processed'
REGION 'us-east-2'
iam_role 'arn:aws:iam::736529293817:role/redshift-IamProductionRedshiftSpectrumRole-LGW3N55ZVXBV';

CREATE EXTERNAL SCHEMA glue_data_lake_raw
FROM DATA CATALOG
DATABASE 'database_mvp_raw'
REGION 'us-east-2'
iam_role 'arn:aws:iam::736529293817:role/redshift-IamProductionRedshiftSpectrumRole-LGW3N55ZVXBV';

Acrescenta o diretorio staging com:
imovel.sql ( Fazer select no bucket)
schema.yml ( acrescenta a configuração do glue, o database e a tabela e o schema)

dbt run

Copiar o profiles.yml para gerar a imagem
cd /Users/resale/.dbt
cp -r profiles.yml /Users/resale/Desktop/Projetos/Data_lake_Enginner/docker/dbt/profiles.yml

export $ENVIRONMENT = production
export $AWS_REGION = us-east-2

Make push-to-ecr