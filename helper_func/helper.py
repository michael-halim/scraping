import os
import datetime
import time
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo('Asia/Bangkok')

def replace_text_in_between(text,start,end,replace_with=''):
    idx_start = text.index(start) if start in text else None
    idx_end = text.index(end) + len(end) if end in text else None
    
    if idx_start == None or idx_end == None:
        return text
    return str(text[0:idx_start]) + replace_with + str(text[idx_end:])

def replace_multiple_char(text, char_to_replace):
    for key, value in char_to_replace.items():
        text = text.replace(key, value)

    return text

def replace_multiple_tags(text, start, end, replace_with=''):
    occurences = text.count(start)

    for _ in range(occurences):
        text = replace_text_in_between(text,start,end,replace_with)
    return text

def save_to_file(dest_path, filename, itemList, automatic_overwrite = True, save_mode='w'):
    with open(dest_path + '.txt', save_mode, encoding='utf-8') as file:
        file.write(filename + ' = [')
        for count,product in enumerate(itemList):
            file.write(str(product))

            if count == len(itemList):
                file.write('\n')
            else:
                file.write(',\n')

        file.write(']')
    file.close()


    FILE_NAME = dest_path
    try:
        os.rename(FILE_NAME + '.txt', FILE_NAME + '.py')

    except FileExistsError:
        chc = '1'
        if not automatic_overwrite:
            chc = input('{0}.py Already Exist. Do You Want to Overwrite ? (0/1)'.format(FILE_NAME))
        
        if chc == '1':
            os.remove(FILE_NAME + '.py')
            os.rename(FILE_NAME + '.txt',FILE_NAME + '.py')

    finally:
        print('Saving File Finished\n\n')
        if automatic_overwrite:
            print('File Overwrite Automatically')

def start_timer():
    return time.perf_counter()

def end_timer(start_time, time_log=[], add_time_log=False, message=''):
    total_time = datetime.timedelta(seconds = time.perf_counter() - start_time)
    bracket = '********************************************'
    print(bracket)
    print(message)
    print('--- %s ---' % (total_time))
    print(bracket)

    if add_time_log:
        time_log += [ (message, str(total_time)) ]
        return time_log

    return None

def get_today():
    """Get Today's Date with `YYYY-MM-DD` Format"""
    today = datetime.datetime.now(LOCAL_TZ)
    return datetime.date(today.year, today.month, today.day)

def print_help(var, title='', username='', show_list_more=False, save_log_path='', log_filename = ''):
    """Log to CLI and Save to File \n
    `============================================`\n
    `2023-01-06 14:15:01.963270`\n
    `USERNAME:  TRAIN APRIORI MODEL`\n
    `APRIORI MODEL`\n
    `============================================`
    
    `============================================`\n
    `2023-01-06 14:15:01.923290`\n
    `USERNAME:  TRAIN WEIGHTED MATRIX`\n
    `CBF LOWEST ITEM LIST`\n
    `[ [841, 2.82], [840, 2.95], [2237, 3.03], [834, 3.2], [224, 3.23] ]`\n
    `LENGTH : 5`\n
    `============================================`
    """
    logs = []
    bracket = '============================================'
    time_now = datetime.datetime.now(LOCAL_TZ)
    print(bracket)
    print(time_now)
    print('USERNAME: ', username)

    logs += [bracket, str(time_now), f'USERNAME: {str(username)}']
    
    if isinstance(var, str) and title == '':
        print(var)
        print(bracket)
        logs += [str(var), bracket]
    else:
        print(title)
        modified_var = var
        if not show_list_more and isinstance(var, list):
            modified_var = modified_var[:5] if len(modified_var) > 5 else modified_var

        print(modified_var)
        logs += [str(title), str(modified_var)]

        try:
            print(f'ORIGINAL LENGTH : {len(var)}')
            print(bracket)
            logs += [f'ORIGINAL LENGTH : {str(len(var))}', bracket]
        except TypeError as e:
            print(bracket)
            logs += [bracket]

    logs = '\n'.join(logs)

    if os.environ.get('DEVELOPMENT_MODE') == 'False':
        save_log(logs=logs, save_log_path=save_log_path, log_filename=log_filename)

def save_log(logs, save_log_path, log_filename):
    if not os.path.exists(save_log_path):
        os.makedirs(save_log_path)

    with open(save_log_path + log_filename, 'a') as file:
        file.write(logs)

    file.close()

def show_error_message(err, module_name = ''):
    print('=========================================')
    print(f'## Error While Importing {module_name} ##')
    print('=========================================')
    print(err)
    print('=========================================')