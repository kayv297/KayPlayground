import docker
import time

def get_container_memory_usage(container_name):
    client = docker.from_env()
    container = client.containers.get(container_name)
    stats = container.stats(stream=False)
    memory_usage = stats['memory_stats']['usage']
    return memory_usage

def log_memory_usage(container_name, log_file):
    while True:
        memory_usage = get_container_memory_usage(container_name)
        with open(log_file, 'a') as f:
            log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Memory Usage: {memory_usage} bytes\n"
            f.write(log_entry)
        time.sleep(120)

if __name__ == "__main__":
    container_name = "my_postgres_container"  # Replace with your container name
    log_file = "memory_usage.log"
    log_memory_usage(container_name, log_file)