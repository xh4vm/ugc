# Исследование OLAP систем

Было проведено исследование двух OLAP систем Clickhouse и Vertica.
Замеры времени проводились при загрузке тестовых данных разными размерами пачки данных и выборки данных в нескольких разрезах.
В сводной таблице приведены данные о времени выполнения операций: вставка данных при размере пачки 10млн, чтение данных время по самой долгой выборке.

## Сводные данные

| Замер                      | Clickhouse, время выборки | Vertica, время  |
|----------------------------|---------------------------|-----------------|
| Вставка данных             | 0:00:10.657789            | 0:03:29.044678  |
| Чтение данных              | 0:00:06.197345            | 0:00:09.764115  |
| Вставка данных с нагрузкой | 0:00:23.222058            | 0:06:13.940257  |
| Чтение данных с нагрузкой  | 0:00:09.917351            | 0:00:17.715298  |

## Выводы
По результатам исследования в качестве OLAP системы был выбран Clickhouse. 
Результат на чтение данных из ClickHouse выше в 1,79 раза, на чтение данных с нагрузкой в 1,58 раза.
Основные преимущества это скорость выполнения операций, хорошая масштабируемость и это Opensource решение.
 