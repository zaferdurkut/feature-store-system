# Feature Store System Design Documentation

## Introduction
The designed system is tailored to handle the dual demands of real-time and batch processing in a feature engineering service. With the primary goals of high performance, horizontal scalability, and low latency, each component has been carefully selected to fulfill these objectives. This document outlines why each technology was chosen, emphasizing its advantages over alternatives, particularly in the context of big data processing.

![system_design](/resources/documentation/feature_store_system_design.png)

---

## Components Overview

### 1. **Data Producer Services**
   - **Role**: Ingests real-time data into the system.
### 2. **Kafka (Ecommerce Transaction Topic & Dead Letter Topic)**
   - **Why Chosen**: Kafka was selected for its proven ability to handle massive streams of data with high throughput and low latency.
   - **Performance**: Kafka’s distributed, partitioned log system allows it to efficiently manage large volumes of data while maintaining high availability.
   - **Scalability**: Kafka can scale horizontally by adding more brokers to the cluster, distributing data across partitions for load balancing.
   - **Low Latency**: Kafka provides near real-time data streaming, which is crucial for systems requiring immediate data availability.

   **Comparison**:
   - Traditional message brokers like RabbitMQ or ActiveMQ struggle with the scale and performance needed for big data, especially when it comes to handling the throughput Kafka can manage. Kafka's design for distributed data handling makes it a superior choice.

### 3. **Flink (Feature Store Stream Consumer Services)**
   - **Why Chosen**: Flink was chosen for its robust stream processing capabilities, which are essential for real-time feature generation.
   - **Performance**: Flink's event-driven architecture allows for low-latency processing of streaming data, making it ideal for generating real-time features.
   - **Scalability**: Flink can scale horizontally across multiple nodes, ensuring it can handle increasing volumes of data without degradation in performance.
   - **Low Latency**: Flink processes data in-memory with event-time semantics, enabling real-time feature computation with minimal delay.

   **Comparison**:
   - While Apache Spark Streaming offers similar functionalities, Flink outperforms in scenarios requiring low-latency processing and complex event-time processing. Flink's fine-grained state management also makes it more efficient for stream processing tasks.

### 4. **Redis (Stream Cache & Offline Cache)**
   - **Why Chosen**: Redis was selected for its in-memory data storage capabilities, which provide extremely fast read/write operations.
   - **Performance**: Redis's in-memory nature allows for microsecond-level data access times, making it ideal for use cases where latency is critical.
   - **Scalability**: Redis can be sharded across multiple nodes, allowing for horizontal scaling as data volume grows.
   - **Low Latency**: Redis's ability to serve data from memory ensures that features are available to clients with minimal delay.

   **Comparison**:
   - Alternatives like Memcached offer in-memory storage but lack the robustness and feature set of Redis, such as persistence and complex data types. Databases like MongoDB or Cassandra, though scalable, cannot match Redis in terms of pure speed for cache-based storage.

### 5. **Hive (Data Lake)**
   - **Why Chosen**: Hive was chosen for its ability to handle large datasets stored in the Hadoop Distributed File System (HDFS), making it ideal for batch processing in big data environments.
   - **Performance**: Hive leverages the scalability of HDFS, allowing it to efficiently store and process massive datasets.
   - **Scalability**: Hive's underlying HDFS architecture enables it to scale out by adding more data nodes, accommodating increasing storage and processing demands.
   - **Batch Processing**: Hive’s SQL-like querying capability makes it easy to process large datasets, providing a familiar interface for data engineers.

   **Comparison**:
   - Alternatives like traditional RDBMS (e.g., MySQL, PostgreSQL) are not designed to handle the scale that Hive can manage. Data warehouses like Snowflake or Redshift offer similar scalability but with higher costs and more complexity for on-premise setups.

### 6. **Spark (Ecommerce Transaction Batch Process Services)**
   - **Why Chosen**: Apache Spark was selected for its powerful batch processing capabilities, particularly in the context of large-scale data.
   - **Performance**: Spark’s in-memory computation model allows for faster processing of large datasets compared to traditional disk-based processing.
   - **Scalability**: Spark can process data across multiple nodes in a cluster, allowing it to handle increasing data volumes effectively.
   - **Batch Processing**: Spark's ability to handle complex ETL processes with its flexible API makes it the go-to choice for batch feature generation.

   **Comparison**:
   - Hadoop MapReduce, while powerful, is slower due to its disk-based processing. Presto offers similar in-memory processing but lacks the comprehensive ecosystem and support for large-scale ETL tasks that Spark provides.

### 7. **Airflow (Workflow Management Orchestrator)**
   - **Why Chosen**: Airflow was chosen for its robust workflow management capabilities, crucial for orchestrating complex data processing pipelines.
   - **Performance**: Airflow’s scheduling and dependency management ensure that workflows are executed efficiently and reliably.
   - **Scalability**: Airflow’s modular architecture allows it to scale across distributed environments, managing thousands of tasks with ease.
   - **Reliability**: Airflow provides extensive monitoring and retry mechanisms, ensuring that batch jobs are completed successfully, even in case of failure.

   **Comparison**:
   - Alternatives like Luigi or Jenkins do not offer the same level of flexibility and scalability for data pipeline orchestration. Airflow’s DAG-based approach and community support make it the preferred choice for complex workflows.

### 8. **Feature Store API**
   - **Why Chosen**: The Feature Store API was developed to provide a high-performance interface for accessing precomputed features.
   - **Performance**: The API is optimized for low-latency access to in-memory data stored in Redis, ensuring fast response times.
   - **Scalability**: The API is designed to scale horizontally, handling increased load by distributing requests across multiple instances.
   - **Low Latency**: Directly querying Redis ensures that feature access is nearly instantaneous, critical for real-time ML applications.

   **Comparison**:
   - Traditional API frameworks like Flask or Spring Boot are commonly used but may require additional optimization for low-latency, high-throughput requirements. The selected stack is optimized for performance in a high-demand environment.

### 9. **Load Balancer**
   - **Why Chosen**: A Load Balancer is essential for distributing incoming API requests across multiple instances, ensuring even load distribution.
   - **Performance**: By preventing any single API instance from becoming a bottleneck, the load balancer ensures consistent performance across the system.
   - **Scalability**: The load balancer allows the system to scale horizontally by adding more API instances as needed.
   - **Low Latency**: Evenly distributed requests ensure that response times remain low, even under high load conditions.

---
### Data Management

#### Schema Design

- **Raw Data Storage**: 
  - **Objective**: Efficiently store and manage raw e-commerce transaction data to support both batch and real-time processing needs.
  - Structured data stored in Hive tables 
  - **Approach**: Hive Data Lake stores raw data in structured tables, enabling SQL-like querying for batch processing tasks. Partitioning by date or category can optimize query performance.### Data Size Management

- **Data Size Measurement**
  - 2,000 rows of data measure approximately 252 KB.
  - Average size per row: ~130 bytes.

- **Estimated Data Size**
  - 100 million rows:
    - Approximately 7300 MB (based on 150 bytes per row).

- **Processed Data (Features) Storage**:
  - **Objective**: Optimize for fast retrieval of processed features to support real-time applications.
  - **Data Structure**:
    - Key-value pairs stored in Redis, where:
      - **Key** examples include:
        - `avg_review:{product_id}`: The average of the last 5 reviews a product has received.
        - `last_purchase_amount:{customer_id}`: The amount a customer paid for their last purchase.
        - `last_review:{customer_id}_{product_id}`: The review rating a customer gave to a product.
        - `revenue_category:{category}`: The revenue obtained from a category for the last 3 orders.
        - `units_sold:{product_id}`: The number of units of a product sold in the last 30 days.
        - `revenue_by_product:{product_id}`: The revenue obtained from a product in the last 30 days.
        - `revenue_by_category:{category}`: The revenue obtained from a category in the last 30 days.
        - `avg_review_rating:{product_id}`: The average of the reviews a product has received in the last 30 days.
      - **Value**: Generally an integer or float, representing metrics like counts, averages, and revenue.
  - **Approach**: Store the processed feature data in Redis as key-value pairs. Redis's in-memory storage ensures microsecond-level retrieval times, making it ideal for real-time applications.
  - Redis is used as the primary database, storing feature data as key-value pairs for fast retrieval.  
  - Redis's in-memory storage and horizontal scaling (via sharding) enable microsecond-level data access, crucial for real-time processing. It also serves as a caching layer to reduce retrieval times further.
  - Cassandra as an Alternative
    - In the context of the system's requirements, Redis was selected over Cassandra primarily due to Redis's exceptional performance in caching operations, which is crucial for achieving low-latency access in the API. Redis provides microsecond-level response times for both read and write operations, making it ideal for scenarios where quick access to data is necessary. This speed is particularly important for serving real-time features and ensuring the API can meet the demands of high-throughput, low-latency environments.
    - While Cassandra is a powerful distributed database that excels in scalability and handling large volumes of data, it introduces more complexity and higher latency compared to Redis. Cassandra's eventual consistency model and the overhead involved in managing distributed writes and reads were not aligned with the immediate speed requirements of the API. Thus, Redis's in-memory storage and simplicity made it the preferred choice for ensuring rapid data retrieval and efficient caching in the system.

#### Optimization Strategies 

- **Data Partitioning**: 
  - **Raw Data**: Partition the raw data based on high cardinality columns such as `TransactionDate`. This improves query performance by reducing the amount of data scanned during operations (could not be developed for the current scenario).
  - **Processed Data**: Use meaningful and unique keys in Redis to avoid collisions and optimize the retrieval of specific features.

- **Indexing**:
  - In raw data storage, consider indexing frequently queried columns like `ProductID`, `Category`, and `TransactionDate` to enhance query performance(could not be developed for the current scenario). 
  - Redis inherently indexes data using its key structure, enabling fast lookups without the need for additional indexing mechanisms.

- **Caching**:
  - Leverage Redis as a cache layer for real-time features. This minimizes the need to query the raw data store repeatedly, reducing latency and improving overall system performance.

#### High Volume Data Performance

- **Scalability**:
  - Redis is horizontally scalable, meaning it can handle large volumes of data by sharding across multiple nodes. This allows for maintaining high performance even as data volume grows.

- **Big Data Handling**:
  - For batch processing of large datasets, Apache Spark is utilized. Its distributed in-memory processing framework enables the efficient handling of terabytes of data, ensuring that even the most resource-intensive ETL tasks are completed in a timely manner.

#### Real-Time and Batch Processing

- **Real-Time Features**:
  - Real-time features such as the average of the last 5 reviews or the amount a customer paid for their last purchase are computed using streaming data from Kafka, processed by Flink, and stored in Redis for fast access.

- **Batch Features**:
  - Batch features like the revenue obtained from a product in the last 30 days are processed in bulk using Apache Spark and stored in Redis. This enables the system to perform complex aggregations over large datasets efficiently.

---
## Conclusion
The combination of these components ensures that the system is not only capable of handling large-scale data processing but also optimized for low-latency feature access. The choices made here are driven by the need to maintain high performance as the system scales, ensuring that both real-time and batch feature engineering tasks are executed efficiently. Each technology was selected based on its strengths in handling big data, providing a reliable and scalable solution for feature store management.
