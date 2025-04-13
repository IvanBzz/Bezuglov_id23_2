import subprocess

class RarCracker:
    def __init__(self, archive_path, wordlist='wordlist.txt'):
        """
        Инициализация экземпляра: задаются путь к RAR-архиву, имя файла словаря и стандартные имена файлов для сохранения хеша и пароля.
        """
        self.archive_path = archive_path
        self.wordlist = wordlist
        self.hash_filename = 'hash_result.txt'
        self.prepared_hash_filename = 'prepared_hash.txt'
        self.password_filename = 'password_found.txt'

    def get_rar_hash(self, result_file=None):
        """
        Извлекает хеш из RAR-архива с помощью утилиты rar2john и записывает результат в файл.
        """
        if result_file is None:
            result_file = self.hash_filename

        try:
            process = subprocess.run(
                ['john/run/rar2john', self.archive_path],
                capture_output=True,
                text=True
            )

            if not process.stdout or process.returncode != 0:
                print(f"Ошибка при выполнении rar2john:\n {process.stderr}")
                return False

            with open(result_file, 'w', encoding='utf-8') as outfile:
                outfile.write(process.stdout)

            print(f"Хеш успешно сохранён в файле: {result_file}")
            return True

        except FileNotFoundError:
            print("Утилита rar2john не найдена. Проверьте правильность указанного пути: john/run/rar2john")
            return False

    def perform_cracking(self):
        """
        Читает хеш из файла, подготавливает его для hashcat и запускает процесс восстановления пароля.
        """
        try:
            with open(self.hash_filename, 'r', encoding='utf-8') as infile:
                content = infile.read()
                if ':' not in content:
                    print("Неверный формат хеша в файле.")
                    return

                _, extracted_hash = content.split(':', 1)
        except FileNotFoundError:
            print("Файл с хешем не найден. Сначала выполните извлечение хеша.")
            return


        with open(self.prepared_hash_filename, 'w', encoding='utf-8') as hash_file:
            hash_file.write(extracted_hash.strip())

        command = f"hashcat -m 13000 -a 0 {self.prepared_hash_filename} {self.wordlist} --force".split()
        subprocess.run(command, check=True)

        try:
            show_output = subprocess.check_output([
                'hashcat',
                '-m', '13000',
                self.prepared_hash_filename,
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
            with open(self.password_filename, 'w', encoding='utf-8') as password_file:
                password_file.write(cracked_password + '\n')
            print(f"[+] Пароль успешно восстановлен и сохранён: {cracked_password}")


if __name__ == '__main__':
    rar_archive = 'locked.rar'
    cracker = RarCracker(rar_archive)
    if cracker.get_rar_hash():
        cracker.perform_cracking()
