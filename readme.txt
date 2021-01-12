Criar usuário na Aws com permissão total ( devops )
Criar o projeto no GitHub
	Git Clone
	Git ignore ( add postgres_data, criava para o Airflow quando era local )
	Git Action (Cria uma pasta no projeto chamado .github  => wokflows => deploy.yml (Código de exemplo do git ) )
	Criar as credenciais de ambiente da Aws  no git ( arquivo das credenciais - devops )
	Criar arquivo setup.py ( ele faz subir os arquivos do git para Aws, tem que add quais arquivos vc quer subir )
	Criar o arquivo requirements.txt ( arquivo setup.py vai usar cdk )
	Criar pasta tests ( Para criar testes automatizados para subir o cloudformation para Aws)
Criação arquivos Cloud Formation
Roda o 1 2 3 4 5 6
Airflow
	Export nas variáveis de ambiente (readme)
	Docker tem que está rodando na maquina local
	Make airflow-deploy
	Entrou no airflow e configurou as variaveis de ambiente da aws + as variáveis do banco de dados para o NetImoveis
	Executar as dags

Rodar os crawlers do glue ( RAW )
Entrar no Job do glue e informar qual o diretório temporário s3 (s3://aws-glue-temporary-736529293817-us-east-2)
Roda o Job do glue para converter json para Parquet
Rodar os crawlers do glue ( Processed )

Rodar os scripts sql no redshift para aparecer os schemas dos datasses do glue
DBT
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

    dbt run ( quando for rodar local )

    Copiar o profiles.yml para gerar a imagem
    cd /Users/resale/.dbt
    cp -r profiles.yml /Users/resale/Desktop/Projetos/Data_lake_Enginner/docker/dbt/profiles.yml

    export $ENVIRONMENT = production
    export $AWS_REGION = us-east-2

    Subir o 7.emr
    Make push-to-ecr


API
	Alterar a table do redshift ( criada pelo DBT )
	Subir a lambda para o S3
	roda 0 8.api

9.0 ( Máquina para rodar o dbt )



DMS = monitora o BD
DBT = Pega dados da tabela do glue e cria uma tabela no Redshift



Criação da API
Api Gatewarey - Api Rest
Criar recurso - Ativar CORS
Criar um método GET e vincular a ARN da lambda
Implantar API e crio um novo estágio
Dentro do Get pego a URL de teste