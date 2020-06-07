import imaplib
import json
import os

import tqdm


class Mail:
    def __init__(self, username, password, host='imap.gmail.com', port=993):
        self.conn = imaplib.IMAP4_SSL(host, port)
        self.conn.login(username, password)

    def select_mailbox(self, mailbox='INBOX'):
        self.conn.select(mailbox)

    def get_emails_nums(self, subject='Daily Coding Problem: Problem', new=True, date_begin=None, date_end=None):
        args = []

        if subject:
            args.append(f'SUBJECT "{subject}"')
        if new:
            args.append(f'UNSEEN')
        if date_begin:
            args.append(f'SINCE "{date_begin}"')
        if date_end:
            args.append(f'BEFORE "{date_end}"')

        typ, msgnums = self.conn.search(None, *args)
        msgnums = msgnums[0].split()
        
        if typ == 'OK':
            print(f'Got {len(msgnums)} messages ID')
            return typ, msgnums

        else:
            print('[WARNING] Something went wrong when searching for e-mails: typ={typ}')
            return typ, msgnums
    
    def get_emails(self, nums, msg_parts='BODY[TEXT]'):
        nums = tuple(nums)

        if not isinstance(nums[0], bytes):
            raise TypeError('numbers should be a list of byte-strings')

        for num in tqdm.tqdm(nums):
            subject = self.conn.fetch(num,
                    "BODY[HEADER]")[1][0][1].decode().split('\r\n')[64].split()
            problem_id = subject[-2]
            problem_diff = subject[-1]

            data = self.conn.fetch(num,
            "BODY[TEXT]")[1][0][1].decode().split('\r\n')

            problem = ''
            for line in data[6:]:
                if line[:3] != '---':
                    line = line.replace('=', '')
                    problem += line + '\n'
                else:
                    break

            recruiter = data[6]

            self._create_folder(id=problem_id, difficulty=problem_diff,
                    problem=problem, recruiter=recruiter)

        return 0

    @staticmethod
    def _create_folder(**params):
        try:
            folder_name = f'{params["difficulty"]} Problem {params["id"]}'
            os.mkdir(folder_name)
            os.chdir(folder_name)

            os.system(f'touch main.py')

            with open('infos.txt', 'w') as fp:
                fp.write(params['problem'])
                fp.write(params['recruiter'])

            os.chdir('../')

        except KeyError as e:
            print(f'A parameter is missing: {e}')
            return 1
        
        except Exception as e:
            print(f'An unexpeted error occured: {e}')
            return 1


def get_data(file_name='infos.json'):
    try:
        with open(file_name) as fp:
            data = json.load(fp)

        username = data['username']
        password = data['password']
        
        return username, password

    except FileNotFoundError as e:
        print(f'Input file "{e.filename}" was not found in current directory: {os.getcwd()}')
        return 1

    except PermissionError as e:
        print(f'Permission denied to read file "{file_name}"')
        return 1

    except json.JSONDecodeError as e:
        print(f'There was an error at ({e.lineno}, {e.colno}) while decoding the file "{file_name}"')
        return 1


if __name__ == '__main__':
    data = get_data()

    os.chdir('Problems')

    mail = Mail(*data)
    mail.select_mailbox()

    _, nums = mail.get_emails_nums()
    mail.get_emails(nums)
