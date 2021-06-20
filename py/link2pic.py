import requests; # все-таки будем скачивать пики 
import os; # for work with paths and dirs
import sys;
#будем работать с файлом из рабочей директории проекта
#import ssl

#from urllib3 import disable_warnings, exceptions

# чтобы удалить папку с файлами
# впадлу писать рекурсию 
#import shutil

# корневая папка для скрипта
rootPath = "link2pic"

# путь к файлу с ссылками, которые по ошибке не скачались
errorPath = "error.txt"

# new folder (content)
sourcePath = "source"

# где будут пики
resultPath = "RESULT"

userspath = sourcePath + "\\" + "botUsers\\botUsers.txt"

# путь для файла проверки
########
#сюда запишется инфа - линки из каждого треда, что были скачаны
########
checkPath = resultPath + "\\" + "check.txt"

# путь для файлов скачивания
#filePath = sourcePath + "\\" + resultPath + "\\"

"""
# проксюхи
proxies = {
    'https': 'https://119.81.189.194:80',
}
session = requests.Session()
session.proxies.update(proxies)
"""

# bant, c, e, p, toy, vip, vp, vt, w, wg, wsr
"""
bant = '\\bant.txt'
c = '\\c.txt'
e = '\\e.txt'
out = '\\out.txt'
p = '\\p.txt'
toy = '\\toy.txt'
vip = '\\vip.txt' 
vp = '\\vp.txt'
vt = '\\vt.txt'
w = '\\w.txt'
wg = '\\wg.txt'
wsr = '\\wsr.txt'
"""

# придется из верхнего сделать список, чтобы в цикле насоздавать 
# папочек под каждый тред
threadDirs = ["bant", "c", "e", "out", "p", "toy", "vip", "vp", "vt", "w", "wg", "wsr"]
#str(threadDirs)
#ssl._create_default_https_context = ssl._create_unverified_context
#disable_warnings(exceptions.InsecureRequestWarning)


# основная функция
def main_func(thread, ID, perCount):
    percents = 0
    percentsCounter = 0 ##### Если прога выполняется первый раз, то ExtraCount = 0
    print('Completed: {}%'.format(percents), end='\r')
    picCounter = 0
    gifCounter = 0
    webmCounter = 0
    f = open(sourcePath + "\\" + "botUsers" + "\\" + str(ID) + "\\" + thread + ".txt", "r")    # проваливаемся в директорию сорса для юзера
    line = '00'
    while line:
        line = f.readline();
        if(line == ''):
            break
        line = line.strip('\n')
    
        # скачали пик
        try:
            # r = requests.get(line, verify=False) 
            # r = requests.get(line, proxies=proxies)
            # r = session.get(line)
            r = requests.get(line)
        except requests.exceptions.RequestException as e:
            #except Exception as e:
            print(e)
            print("Ошибка при скачивании пика...! ")
            percentsCounter +=1
            f1 = open(errorPath, "a")
            f1.write(line + "\n")
            f1.write(e)
            f1.close()
        
        # записали его в файл
        # тут мы узнаем расширение (тип) файла (png, jpg - как фото, а gif - как видео)
        # пикаем ласт 3 символа из строки
        type = line[-3:]
        if (type == 'gif'):
            with open((resultPath + "\\" + thread + "\\" + "Gifka" + str(gifCounter) + ".gif") , 'wb') as file: 
                file.write(r.content)
                gifCounter += 1
                
        elif (type == 'ebm'):
            with open((resultPath + "\\" + thread + "\\" + "WebM" + str(webmCounter) + ".webm") , 'wb') as file: 
                file.write(r.content)
                webmCounter += 1
            
        else:
            with open((resultPath + "\\" + thread + "\\" + "Kartinka" + str(picCounter) + "." + type) , 'wb') as file:
                file.write(r.content)
                picCounter += 1
    
        # тут сразу же быстренько вычислили процентики
        ##########
        percentsCounter +=1
        percents = ((percentsCounter*100) / perCount)
        percents = str(round(percents, 3))
        print("\t\t\t\t\t\t\t\t\t\t\t\t", end = '\r') #шобы было покрасивше
        print('Completed: {}%'.format(percents), end='\r')
        ##########
    f.close()
    print("\nDone!")


def counter_func(thread, ID):
    picCounter = 0
    gifCounter = 0
    webmCounter = 0
    f = open(sourcePath + "\\" + "botUsers" + "\\" + str(ID) + "\\" + thread + ".txt")    # проваливаемся в директорию сорса для юзера
    line = '00'
    while line:
        line = f.readline();
        if(line == ''):
            break
        line = line.strip('\n')
        # тут мы узнаем расширение (тип) файла (png, jpg - как фото, а gif - как видео)
        # пикаем ласт 3 символа из строки
        type = line[-3:]
        if (type == 'gif'):
            gifCounter += 1
        elif (type == 'ebm'):
            webmCounter += 1
        else:
            picCounter += 1
    print("Картинок: ", picCounter)
    print("Гифок: ", gifCounter)
    print("Вебмов: ", webmCounter)
    perCount = picCounter + gifCounter + webmCounter
    return perCount


def reuse_func(thread, ID, perCount):
    infile = -1
    if (os.path.exists(resultPath + "\\" + thread)):
        files = os.listdir(path = resultPath + "\\" + thread)
        infile = (len(files))
    #print(infile)
    if (perCount == infile):
        return 1 # значит, что чел уже скачал полностью этот тред себе в папку
    else: return 0

# тут будет ненужная функция, которая будет "пугать" пользователя
# количеством пиков, что он скачает)
def scary_message(threadDirs, ID):
    # в цикле мы пробежимся по всем файлам
    # подсчитаем кол-во строк, (исключая webm, но включая gif)
    picCounter = 0
    gifCounter = 0
    webmCounter = 0
    for dirs in threadDirs:
        tmpGif = 0
        tmpPic = 0
        tmpWebm = 0
        f = open(sourcePath + "\\" + "botUsers" + "\\" + str(ID) + "\\" + dirs + ".txt")    # проваливаемся в директорию сорса для юзера
        line = '00'
        while line:
            line = f.readline();
            if(line == ''):
                break
            line = line.strip('\n')
            # тут мы узнаем расширение (тип) файла (png, jpg - как фото, а gif - как видео)
            # пикаем ласт 3 символа из строки
            type = line[-3:]
            if (type == 'gif'):
                gifCounter += 1
                tmpGif += 1
            elif (type == 'ebm'):
                webmCounter += 1
                tmpWebm += 1
            else:
                picCounter += 1
                tmpPic += 1
        # выводим кол-во кала в треде
        print(dirs, ":","(", tmpPic, "/", tmpGif, "/", tmpWebm, ")")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Всего...")
    print("Картинок: ", picCounter)
    print("Гифок: ", gifCounter)
    print("Вебмов: ", webmCounter)
    
    
    
def make_dir(thread):
    if (os.path.exists(resultPath + "\\" + thread)):
        pass
    else: os.makedirs(resultPath + "\\" + thread)
        
    
# функция проверяет наличие юзера в листе
def check_user_func(ID):
    # проверка на распакованность файлов из архива
    if (os.path.exists(userspath) == False):
        return 0
    
    # тут проверка на наличие пользователя в базе
    line = '000'
    f = open(userspath,"r")
    while line:
        line = f.readline();
        if(line == ''):
            break
        # тут мы удаляем \n, чтобы не было ошибки при отправке
        line = line.strip('\n')
        #print(line)
        #print("ID =", ID)
        if (line == ID):
            # print("line =", line)
            print ("Да, " + ID + " есть в списке пользователей, все ОК\n")
            f.close()
            return ID
    f.close()
    print("Пользователя ", ID, " нет в списке...")
    #print("line is =", line)
    f.close()
    return 2
          

#NACHALO
tmp = input("Привет! Если хочешь скачать свои пики, то введи мне свой id: ")
#ID = int(tmp)
ID = tmp
print("Твой id: ", ID)
#ID = ID.strip('\n')

# проверка
ID = check_user_func(ID)
if (ID == 2):
    print("перезапустите программу!")
    sys.exit(54)

if (ID == 0):
    print("Ты не распаковал файлы из архива!")
    sys.exit(0)
    
##############
# предалагаем выбор треда для скачивания
# сначала принтим доступные треды
print("Список доступных тредов ")
# выводим шапку
print("      pics / gifs / webms")
scary_message(threadDirs, ID)

thread = input("Введите название треда, из которого вы хотите скачать данные: ")
#### incorrect test
flag = 0
for dirs in threadDirs:
    if (thread == dirs):
        flag = 1

if (flag == 0):
    print("Такого треда нет в списке!...")
    print("перезапустите программу!")
    sys.exit (1488)
####
perCount = counter_func(thread, ID)
reuse = reuse_func(thread, ID, perCount)
if (reuse == 1):
    print("Вы уже скачивали этот тред полностью... выберите другой...")
    print("Перезапустите программу!")
    sys.exit(777)
print("Далее потребуется соединение с интернетом")
print("Вы уверены, что хотите скачать... ")

# эта ф-я ретернет нам кол-во всего там в треде 
# чтобы мы смогли нормально считать проценты
question = input("Введите (y / n)(Да / Нет): ")
# нет... я не шизик...так было нужно
if ((question == 'y') | (question ==  'yes') | (question == 'Yes') | (question == 'да') | (question == 'Да') | (question == 'д') | (question == 'Д')):
    make_dir(thread)
    main_func(thread, ID, perCount)
elif ((question == 'n') | (question ==  'no') | (question == 'No') | (question == 'нет') | (question == 'Нет') | (question == 'н') | (question == 'Н')):
    print("Вы отменили процесс... Можете закрыть программу.")
    sys.exit(5454)
else:
    print("Здесь нет таких вариантов ответа... перезапустите программу, чтобы повторить...")
    sys.exit(34509)


