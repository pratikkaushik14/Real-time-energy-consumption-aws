This project is designed to implement a real-time data processing pipeline using Apache Kafka, Apache Spark, AWS S3, and Streamlit. The primary goal is to ingest data streams, process them in real-time, and store the processed data for further analysis.

Components
Data Producer (608_project_producer.ipynb): Responsible for producing and streaming data into the pipeline.
Data Consumer (608_project_consumer.ipynb): Consumes and processes the streamed data for analysis.
Detailed Steps
1. Setting Up the Environment
AWS S3 Configuration:
Both notebooks start by setting up connections to an AWS S3 bucket. This involves configuring access keys and mounting the S3 bucket to a specific path.
2. Data Ingestion and Streaming (Producer Notebook)
Kafka Stream Setup:

The producer notebook includes functions to read data from Kafka streams. It uses Spark to handle the streaming data.
Functions such as processStream and processBatch are defined to handle streaming and batch processing, respectively.
Stream Processing:

processStream: Reads data from a Kafka topic in real-time. It processes the data using Spark and writes the output to S3 in Parquet format.
processBatch: Similar to processStream, but designed for batch processing of data from Kafka.
Code Example:

python
Copy code
def processStream(maxOffsetsPertrigger, startingTime, topic):
    print(f"Starting Bronze Stream...", end='')
    kafka_df = readFromKafkaStream(maxOffsetsPertrigger, startingTime, topic)
    invoices_df = readJsonToDf(kafka_df, schema_dict)
    sQuery = writeStreamDataToS3parquet(invoices_df, mount_path)
    print("Done")
    return sQuery

processStream(maxOffsetsPertrigger=1000, startingTime=1, topic='topic_2')
3. Data Consumption and Analysis (Consumer Notebook)
Data Reading from S3:

The consumer notebook mounts the S3 bucket and reads the processed data stored in Parquet format.
Data Processing:

It applies transformations and analyses on the read data. This might include aggregations, filtering, and other Spark operations to prepare the data for further use.
Visualization and Analysis:

The notebook may include steps for visualizing the processed data or preparing it for machine learning models or other analytical tasks.
4. Example Use Cases
Real-Time Analytics: Creating dashboards that visualize data in real-time.
IoT Data Processing: Processing and analyzing data from IoT devices for monitoring and alerting.
ETL Pipelines: Extracting, transforming, and loading large datasets for big data applications.
Conclusion
This project demonstrates a comprehensive real-time data processing pipeline, leveraging the capabilities of Kafka for data ingestion, Spark for data processing, and AWS S3 for storage. The producer notebook handles data ingestion and initial processing, while the consumer notebook focuses on consuming and further analyzing the processed data. This setup is ideal for applications requiring real-time data analysis and large-scale data processing.


