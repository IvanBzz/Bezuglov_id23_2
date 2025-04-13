import itertools
import subprocess

def generate_passwords(task_id, charset: str, max_length: int, output_file: str = "passwords.txt"):
    """
    Генерирует все возможные комбинации символов из charset с длинами от 1 до max_length
    и записывает их в файл с именем: str(task_id) + output_file.
    """
    filename = str(task_id) + output_file
    with open(filename, "w", encoding="utf-8") as f:
        for length in range(1, max_length + 1):
            for combo in itertools.product(charset, repeat=length):
                password = ''.join(combo)
                f.write(password + '\n')
    print(f"Словарь с вариантами паролей сгенерирован и сохранён в файле: {filename}")
    return filename

class RarCracker:
    def __init__(self, archive_path):
        """
        Инициализация экземпляра: задаётся путь к RAR-архиву и стандартные имена для файлов.
        Словарь для восстановления пароля генерируется автоматически с помощью generate_passwords.
        """
        self.archive_path = archive_path
        charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
        task_id = 1
        max_length = 3
        self.wordlist = generate_passwords(task_id, charset, max_length, output_file="passwords.txt")

    def get_rar_hash(self):
        """
        Извлекает хеш из RAR-архива с помощью утилиты rar2john и записывает результат в файл.
        """

        try:
            process = subprocess.run(
                ['john/run/rar2john', self.archive_path],
                capture_output=True,
                text=True
            )

            if not process.stdout or process.returncode != 0:
                print(f"Ошибка при выполнении rar2john:\n{process.stderr}")
                return False

            with open('hash_result.txt', 'w', encoding='utf-8') as outfile:
                outfile.write(process.stdout)
            result_file='hash_result.txt'
            print(f"Хеш успешно сохранён в файле: {result_file}")
            return True

        except FileNotFoundError:
            print("Утилита rar2john не найдена. Проверьте правильность указанного пути: john/run/rar2john")
            return False

    def perform_cracking(self):
        """
        Читает хеш из файла, подготавливает его для hashcat, запускает процесс восстановления пароля,
        а затем сохраняет найденный пароль.
        """
        try:
            with open('hash_result.txt', 'r', encoding='utf-8') as infile:
                content = infile.read()
                if ':' not in content:
                    print("Неверный формат хеша в файле.")
                    return

                _, extracted_hash = content.split(':', 1)
        except FileNotFoundError:
            print("Файл с хешем не найден. Сначала выполните извлечение хеша.")
            return

        with open('prepared_hash.txt', 'w', encoding='utf-8') as hash_file:
            hash_file.write(extracted_hash.strip())


        command = f"hashcat -m 13000 -a 0 {'prepared_hash.txt'} {self.wordlist} --force".split()
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print("Ошибка при выполнении hashcat:")
            print(e)
            return

        try:
            show_output = subprocess.check_output([
                'hashcat',
                '-m', '13000',
                'prepared_hash.txt',
                '--show'
            ]).decode('utf-8')
        except subprocess.CalledProcessError as e:
            print("Ошибка при вызове hashcat для вывода результата:")
            print(e)
            return

        if ':' not in show_output:
            print("[-] Пароль не удалось восстановить.")
        else:
            _, cracked_password = show_output.strip().split(':', 1)
            cracked_password = cracked_password.strip()
            with open('password_found.txt', 'w', encoding='utf-8') as password_file:
                password_file.write(cracked_password + '\n')
            print(f"[+] Пароль успешно восстановлен и сохранён: {cracked_password}")


if __name__ == '__main__':
    rar_archive = 'locked.rar'
    cracker = RarCracker(rar_archive)
    if cracker.get_rar_hash():
        cracker.perform_cracking()
