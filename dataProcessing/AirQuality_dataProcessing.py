from datetime import date
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, LongType, ArrayType
from pyspark.sql.functions import from_json, col, lit
from pyspark.sql.utils import AnalysisException
from pyspark.sql import Row

#blob storage connection
storage_account_name = "deproject2sa"
storage_account_key = "xxxxxx"
container = "data"

spark.conf.set(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", storage_account_key)


# Get the current date
current_date = date.today().strftime("%Y_%m_%d")

folder_path = f"wasbs://data@deproject2sa.blob.core.windows.net/AirQuality/{current_date}"
# Read JSON files into DataFrames
dfs = []
for file in dbutils.fs.ls(folder_path):
    if file.name.endswith(".json"):
        df = spark.read.json(file.path)
        dfs.append(df)
print(len(dfs))


# Iterate through the list of DataFrames and print their schemas
for df in dfs:

    print(f"Schema of DataFrame ", df.select("data.city.name").collect())
    df2 = df.select("data.iaqi")
    df2.printSchema()
    print()


processed_dfs = []

def has_column(df, col):
    try:
        df[col]
        return True
    except AnalysisException:
        return False

for df1 in dfs:
    # Apply your data processing transformations
    '''Faced a problem with the iaqi colums since they are non-common in our json files (so its not possible to create a csv file that contain all data from the json files  with a single structure and to fix that I
       Got the a list of all the iaqi columns 
       Created a function "has_column" to check if a column exist or not
       If iaqi column exist create a df with iaqi column = its value and id column = 1
       If not create a data frame with iaqi column = -99999 and id column = 1
       Then in each case we append the df to a list
       After that we join all the df’s in the list based on id to get the all the iaqi values of our current row
       We then crossJoin it with part1_df which contain the other columns that are always present in our json files, to get a row with all of our desired columns.
       We then append our dataframe that contains all the desired data form the current json file into a list that we are gonna merge later'''

    part1_df = df1.select("data.idx", "data.city.name", "data.city.url", "data.aqi", "data.dominentpol",
                   "data.time.s", "data.time.tz"
                 )
    emp_RDD = spark.sparkContext.emptyRDD()
    columns = StructType([])

    df_list = []
    val = ['co', 'dew', 'h', "no2", "o3", "p", "pm10", "pm25", "so2", "t", "w", "wg"]

    for i in val:
        df2 = spark.createDataFrame(data = emp_RDD, schema = columns)
        if has_column(df1, f"data.iaqi.{i}.v") == True:
            df2 = df1.select(df1.data.iaqi.getItem(i).v.alias(f"{i}"))
            df2 = df2.withColumn("id", lit(1))
            df_list.append(df2)
        else:
            default_data = Row(id=1, i=-99999)
            df2 = spark.createDataFrame([default_data])
            df2 = df2.withColumnRenamed("i", f"{i}")
            df_list.append(df2)

    combined_df = df_list[0] 
    for df in df_list[1:]:
        combined_df = combined_df.join(df, on='id', how='inner')

    processed_df = part1_df.crossJoin(combined_df)
    processed_dfs.append(processed_df)



merged_df = processed_dfs[0]  # Take the first DataFrame
for df in processed_dfs[1:]:
    merged_df = merged_df.union(df)


output_path = f"/mnt/deprojectsagen2/data/AirQuality/{current_date}"
merged_df.coalesce(1).write.csv(output_path, header=True, mode="overwrite")