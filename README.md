Description now available on Russian only.

## Проблема и решение

Этот скрипт я использовал для некоторых нетривиальных переконфигураций 
большого числа Jenkins джоб в автоматическом режиме. Пусть имеется порядка 1000
CI-джоб с приблизительно похожей конфигурацией и необходимо внести изменения в 
каждую из них. Например, обновить конфигурацию какого-то плагина. Поскольку 
джоб много и их конфигурации однотипны, но не идентичны по структуре, заведомо 
известно, что будут ошибки. Такие ошибки нужно уметь отслеживать, уметь 
проходить процесс по шагам и автоматически, и быть готовым к откатыванию 
конфигурации к исходному состоянию. Этот скрипт решает эти задачи.
	
## Использование

 0. Убедитесь, что у вас установлена библиотека [requests](http://docs.python-requests.org/en/master/)
 1. Откройте и отредактируйте файл `config.py`
 2. Запустите `python reconf.py` (Python 2)
 
## Конфигурация

### Режим ручного управления

В режиме ручного управления перед каждым следующим шагом запрашивается 
подтверждение пользователя. Для продолжения нужно ввести "Y", "y" или 
нажать Enter.

При отключённом режиме ручного управления скрипт будет исполнять 
последовательно шаг за шагом. 
 
Включить режим ручного управления

```
     MANUAL_MODE = True
```

Выключить режим ручного управления

```
     MANUAL_MODE = False
```

### URL со списком CI джоб

С этого адреса будут собраны все джобы, в которые нужно внести изменения.

```
CI_URL_PREFIX = "https://cisrv.yourcompany.com/view/myview/"
```

### Флаг отключения сбора CI-джоб с Jenkins

Установите USE_JOB_LIST = True, чтобы отключить сбор CI-джоб из CI_URL_PREFIX
(предыдущий параметр). Список CI-джоб будет взят из файла

```
USE_JOB_LIST = True
JOB_LIST_FILE = "modify.tx
```

### Имя пользователя

Доменный пользователь из-под которого будут делаться запросы к Jenkins. 
Внутри yourcompany'а любые запросы ко всем серверам Jenkins CI должны 
происходить из-под какого-либо доменного пользователя

```
USERNAME = "valeriy"
```

### Пароль

Пароль доменного пользователя из-под которого будут делаться запросы к Jenkins.

```
PASSWORD = "your_password"
```

### Имя папки с данными

При запуске скрипта будет создана директория в том же месте, где лежит 
скрипт. В неё будут записываться логи, конфигурация CI джоб и вообще любые 
файлы и данные, относящиеся к последнему запуску скрипта. Вы можете 
установить любое статическое имя:

```
     LOCAL_STORAGE_DIR = "process"
```

или генерировать автоматически имя на каждый запуск скрипта отдельно. 
Например, создавать папку, содержащую в имени дату и время запуска:

```     
     LOCAL_STORAGE_DIR = "process-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
```

### Имя файла с логами

Скрипт автоматического переконфигурирования CI джоб достаточно подробно 
логирует действия и ошибки. Вся эта информация записывается в файл. Файл 
всё время дополняется и никогда не удаляется, не переименовывается, не 
заменяется новым. 

```
LOG_FILE_NAME = "log.txt"
```

### Имя директории с оригинальной конфигурацией CI джоб

Перед редактированием кофигурации на Jenkins-серверах скрипт сохраняет 
исходную конфигурацию модифицируемых CI джоб, чтобы позднее можно было её 
восстановить, если что-то пойдёт не так. Исходная конфигурация хранится в
виде XML файлов в директории: LOCAL_STORAGE_DIR/CI_JOBS_CONFIGS_DIR

```
CI_JOBS_CONFIGS_DIR = "jobs"
```

### Имя директории с модифицированной конфигурацией CI джоб

Перед редактированием кофигурации на Jenkins-серверах скрипт вносит 
изменения в исходную конфигурацию CI джоб локально. Модифицированная 
конфигурация хранится в виде XML файлов в директории: LOCAL_STORAGE_DIR/CI_JOBS_RECONFIGS_DIR

```
CI_JOBS_RECONFIGS_DIR = "new_jobs"
```

### Действие

Функция, выполняющая преобразование конфигурации. На вход получает файл.
Возвращает модифицированную XML-конфигурацию как строку.

```
def action(job_config):
    pass
```

## Лицензия

Все материалы этого репозитория доступны как общественное достояние. Делайте с
этим кодом всё, что хотите.
