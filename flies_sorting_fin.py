import inspect
import os
import sys
import copy
import shutil
import datetime

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

#print(get_script_dir())

def ext2dir(filename):
    # взять имя
    # откочерыжить расширение
    # проверить его на правильность
    # выдать расширение из трех первых после точки символов стоит ли?
    # filename.rfind('.', [start],[end])
    print('Проверка расширения у файла: '+filename)
    #stroka=((filename.split('.')[-1])[:3:]) строго три символа отрезать
    ext=(filename.split('.')[-1])
    for simbol in ext:
        if (not simbol.isalnum() and not simbol != ' '):
            print('Корректируем символ '+simbol+' в расширении '+ext)
            ext=ext.replace(simbol,'_')
    return ext

def createdir(path):
    # проверка на уже созданные дирректории
    if os.path.isdir(path)==True:
        print('Пропускаем создание директории - такая дирректория уже есть: ',path)
    else:
        os.makedirs(path)
        print('Создаём директорию: ',path)
    return

def move4copy(pathold, pathnew, action):
    if action == 1:
        shutil.move(pathold, pathnew)
        print('Перенос файла: ОК')        
    else:
        shutil.copyfile(pathold, pathnew)
        print('Копирование файла: ОК')
    return

def fileinfo(path):
    filesize=os.path.getsize(path)
    if filesize < 1024:
        print('Размер:',filesize,'байт')
    elif filesize < 1048576:
        print('Размер:',filesize//1024,'Кб')
    else:
        print('Размер:',filesize//1048576,'Мб')
    print('Дата создания:',\
        datetime.datetime.fromtimestamp(int(os.path.getctime(path))))
    print('Дата последнего открытия:',\
        datetime.datetime.fromtimestamp(int(os.path.getatime(path))))
    print('Дата последнего изменения:',\
        datetime.datetime.fromtimestamp(int(os.path.getmtime(path))))
    return

def userinput():
    fold=''
    user_action=0
    
    try:
        user_action= int(input('Перенос файлов (1) или копирование (0):'))
        if user_action!=1:
            user_action=0
        print('Введите папку для сортированных файлов  (Папка для сортированных\nфайлов по умолчанию SORTED ввденый текст будет переведен в верхний\nрегристр и обрезан до 8 символов):')
        fold= str(input(''))
        if (not fold.isprintable() or fold==''):
            fold='SORTED'
        else:
            fold=(fold.upper()[:8])
        print (fold,':',user_action)
    except ValueError:
        print ('Вы ошиблись. Попробуйте снова.')
        raise SystemExit(1)
    return fold, user_action 
    



folder='SORTED'
useraction=0
#pathnow = str(get_script_dir()) # путь самурая, тьфу путь скрипта
folder, useraction = userinput()
print('Папка:', folder, 'Действие: ',useraction)
gonow=str(input('Вы уверены? (0-Да 1-Нет)'))
if gonow=='1':
    print('Действие отменено')
    raise SystemExit(1)

      
# вытаскиваем список файлов для переноса
for disk, dirs, files in os.walk(get_script_dir()):
    for file in files:
        print(' _______________________________________________________________ ')    
        print('|                                                               |')
        print('|_Выполняем обработку файла_____________________________________|')
        path_old = os.path.join(disk,file) # формирование адреса
        path_dir = os.path.join(disk,folder,ext2dir(file))
        path_new = os.path.join(path_dir,file)
   
        try:
            print('Файл:       ', file)
            print('Путь:       ', path_old)
            print('Новый путь: ', path_new)
            fileinfo(path_old)
            createdir(path_dir)
            move4copy(path_old, path_new, useraction)
            print('-------------------------------------------------------------')
        except IOError as err:
            print("I/O error: {0}".format(err))
        except ValueError:
            print("Ошибка в имени  или пути файла")
        except:
            print("Неожиданная ошибка:", sys.exc_info()[0])
        
