from celery_worker import celery
import subprocess
import os
import json
import redis


# Публикация событий в Redis
def publish_event(task_id, status, message=None, password=None):
    r = redis.Redis(host='localhost', port=6379, db=0)
    event = {
        "task_id": task_id,
        "status": status,
        "message": message,
        "password": password
    }
    r.publish("task_updates", json.dumps(event))


@celery.task(bind=True)
def crack_rar(self, file_path):
    task_id = self.request.id

    try:
        # Извлечение хеша
        rar2john_path = os.path.join(os.getcwd(), 'john/run/rar2john')
        if not os.path.exists(rar2john_path):
            publish_event(task_id, "error", "rar2john not found")
            return

        result = subprocess.run(
            [rar2john_path, file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            publish_event(task_id, "error", f"rar2john error: {result.stderr}")
            return

        hash_str = result.stdout.split(':', 1)[1].strip() if ':' in result.stdout else result.stdout

        publish_event(task_id, "hash_extracted", "Hash extracted successfully")

        # Подбор пароля
        hash_file = f"rar5_hash_{task_id}.txt"
        with open(hash_file, 'w') as f:
            f.write(hash_str)

        wordlist = "wordlist.txt"
        if not os.path.exists(wordlist):
            publish_event(task_id, "error", "Wordlist not found")
            return

        hc_result = subprocess.run(
            ["hashcat", "-m", "13000", "-a", "0", hash_file, wordlist, "--force"],
            capture_output=True,
            text=True
        )

        if hc_result.returncode != 0:
            publish_event(task_id, "error", f"Hashcat error: {hc_result.stderr}")
            return

        # Проверка результата
        show_result = subprocess.check_output(
            ["hashcat", "-m", "13000", hash_file, "--show"],
            text=True
        )

        if ':' in show_result:
            password = show_result.strip().split(':', 1)[1]
            publish_event(task_id, "success", "Password found", password)
        else:
            publish_event(task_id, "failure", "Password not found")

    except Exception as e:
        publish_event(task_id, "error", str(e))
    finally:
        if os.path.exists(hash_file):
            os.remove(hash_file)