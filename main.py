import sys
import os
import shutil
import time

class SyncFolders:
    def __init__(self, changes, status, interval, amount, replica_folder_path, source_folder_path, logs_file_path):
        self.changes = changes
        self.status = status
        self.interval = interval
        self.amount = amount
        self.replica_folder_path = replica_folder_path
        self.source_folder_path = source_folder_path
        self.logs_file_path = logs_file_path
    def logs_write(self, changes, status):
        with open(self.logs_file_path, 'a') as logs_file:
            if status == 'DELETE':
                logs_file.writelines('DELETED ' + '\nDELETED '.join(changes) + '\n')
                print('DELETED ' + '\nDELETED '.join(changes) + '\n')
            elif status == 'COPY':
                logs_file.writelines('COPIED ' + '\nCOPIED '.join(changes) + '\n')
                print('COPIED ' + '\nCOPIED '.join(changes) + '\n')
            elif status == 'CREATE':
                logs_file.writelines('CREATED ' + '\nCREATED '.join(changes) + '\n')
                print('CREATED ' + '\nCREATED '.join(changes) + '\n')
    def start(self, interval, amount):
        try:
            changes_list = []
            for i in range(amount):
                replica_files = os.listdir(self.replica_folder_path)
                source_files = os.listdir(self.source_folder_path)
                # DELETE
                for delete_files in replica_files:
                    file_path = os.path.join(self.replica_folder_path, delete_files)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        changes_list.append(delete_files)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        changes_list.append(delete_files)
                if len(changes_list) > 0:
                    self.logs_write(changes_list, 'DELETE')
                    source_action = 'COPY'
                else:
                    source_action = 'CREATE'
                # COPY
                changes_list.clear()
                for copy_files in source_files:
                    file_path = os.path.join(self.source_folder_path, copy_files)
                    if os.path.isfile(file_path):
                        shutil.copyfile(file_path, (self.replica_folder_path + '/' + copy_files))
                        changes_list.append(copy_files)
                    elif os.path.isdir(file_path):
                        shutil.copytree(file_path, (self.replica_folder_path + '/' + copy_files), dirs_exist_ok=True)
                        changes_list.append(copy_files)
                if len(changes_list) > 0:
                    self.logs_write(changes_list, source_action)
                # Get rid of unnecessary interval
                if len(changes_list) > 0 and i < amount - 1:
                    time.sleep(interval)
                changes_list.clear()
        except FileNotFoundError as error:
            print('An error has occurred. \n', error)
def main():
    interval = int(sys.argv[3]) # interval in seconds
    amount = int(sys.argv[4]) # amount of synchronizations
    source_folder_path = str(sys.argv[1]).strip('\'"') # source folder path
    replica_folder_path = str(sys.argv[2]).strip('\'"') # replica folder path
    logs_file_path = str(sys.argv[5]).strip('\'"') # logs file path

    sync = SyncFolders(None, None, None, None, replica_folder_path, source_folder_path, logs_file_path)
    sync.start(interval, amount)
main()