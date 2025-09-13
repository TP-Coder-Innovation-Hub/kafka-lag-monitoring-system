import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# Configuration
KAFKA_BROKER = 'localhost:9092'
POST_TOPIC = 'posts'
COMMENT_TOPIC = 'comments'
EMOJI_TOPIC = 'emojis'
producer = None

def init_producer():
    """Initializes the Kafka producer with a retry mechanism."""
    global producer
    print("Connecting to Kafka broker...")
    retries = 5
    while retries > 0:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BROKER],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Successfully connected to Kafka.")
            return
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            retries -= 1
            time.sleep(5)
    raise ConnectionError("Could not connect to Kafka broker after multiple retries.")

def generate_post():
    """Generates a random social media post event."""
    return {
        'post_id': random.randint(1000, 9999),
        'user_id': random.randint(1, 100),
        'content': f"This is a new post at {datetime.now().isoformat()}",
        'timestamp': int(time.time() * 1000)
    }

def generate_comment(post_id):
    """Generates a random social media comment event."""
    return {
        'comment_id': random.randint(20000, 29999),
        'post_id': post_id,
        'user_id': random.randint(1, 100),
        'content': f"A comment on post {post_id} at {datetime.now().isoformat()}",
        'timestamp': int(time.time() * 1000)
    }

def generate_emoji(target_id, target_type):
    """Generates a random emoji reaction event."""
    emojis = ['👍', '❤️', '😂', '😭', '😮']
    return {
        'reaction_id': random.randint(30000, 39999),
        'target_id': target_id,
        'target_type': target_type,
        'user_id': random.randint(1, 100),
        'emoji_type': random.choice(emojis),
        'timestamp': int(time.time() * 1000)
    }

def produce_events():
    """Main function to produce a stream of events."""
    try:
        init_producer()

        print("Starting producer. Press Ctrl+C to exit.")
        while True:
            post = generate_post()
            producer.send(POST_TOPIC, value=post)
            print(f"Produced Post: {json.dumps(post)}")

            comment = generate_comment(post['post_id'])
            producer.send(COMMENT_TOPIC, value=comment)
            print(f"Produced Comment: {json.dumps(comment)}")

            emoji_post = generate_emoji(post['post_id'], 'post')
            producer.send(EMOJI_TOPIC, value=emoji_post)
            print(f"Produced Emoji on Post: {json.dumps(emoji_post)}")

            emoji_comment = generate_emoji(comment['comment_id'], 'comment')
            producer.send(EMOJI_TOPIC, value=emoji_comment)
            print(f"Produced Emoji on Comment: {json.dumps(emoji_comment)}")

            producer.flush()

            time.sleep(random.uniform(0.5, 2.0))
    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        if producer:
            producer.close()
        print("Producer closed.")

if __name__ == '__main__':
    produce_events()