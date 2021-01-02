from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName('to_parquet') \
    .getOrCreate()

df = spark.read.format('json').load(f's3a://s3-production-mvp-imovel-raw/zapimoveis')
df.write.format('parquet').save(path=f's3a://s3-production-mvp-imovel-processed/zapimoveis', mode='overwrite')
