import json
from kafka import KafkaConsumer

# Configuration
KAFKA_BROKER = 'localhost:9092'
CONSUMER_GROUP_ID = 'social-media-monitor-group'
TOPICS = ['posts', 'comments', 'emojis']

def create_consumer():
    """Creates a Kafka consumer instance."""
    return KafkaConsumer(
        *TOPICS,
        bootstrap_servers=[KAFKA_BROKER],
        group_id=CONSUMER_GROUP_ID,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def consume_messages():
    """Main function to consume messages from Kafka topics."""
    consumer = None
    try:
        consumer = create_consumer()
        print(f"Consumer started, listening to topics: {TOPICS}")
        print("Press Ctrl+C to exit.")

        for message in consumer:
            topic = message.topic
            data = message.value

            print(f"Received message from topic '{topic}': {json.dumps(data, indent=2)}")

    except KeyboardInterrupt:
        print("\nStopping consumer...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if consumer:
            consumer.close()
        print("Consumer closed.")

if __name__ == '__main__':
    consume_messages()