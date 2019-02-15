**Проблема и решение:**

Этот скрипт я использовал для некоторых нетривиальных переконфигураций 
большого числа Jenkins джоб в автоматическом режиме. Пусть имеется порядка 1000
CI-джоб с приблизительно похожей конфигурацией и необходимо внести изменения в 
каждую из них. Например, обновить конфигурацию какого-то плагина. Поскольку 
джоб много и их конфигурации однотипны, но не идентичны по структуре, заведомо 
известно, что будут ошибки. Такие ошибки нужно уметь отслеживать, уметь 
проходить процесс по шагам и автоматически, и быть готовым к откатыванию 
конфигурации к исходному состоянию. Этот скрипт решает эти задачи.

**Лицензия**

Все материалы этого репозитория доступны как общественное достояние. Делайте с
этим кодом всё, что хотите.
