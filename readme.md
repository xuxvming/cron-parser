## Cron Parser Usage

<br> In the command line, cd to the project folder
<br>
<br> Run the following command to pass the cron expression
<br>

<br>`python main.py '*/15 0 1,15 * 1-5 /user/bin/'`

<br>In the terminal, it will print the parsed cron expression in a dict format
<br>Meanwhile, it will also output a file out.txt
<br>For Example : 
```.text
minute 0 15 30 45
hour 0
day 1 2
month 1 2 3 4 5 6 7 8 9 10 11 12
week 1 2 3 4 5
command /user/bin/
```

* Use cases:
    1. The parser only works for standard cron expression 
    2. Week and Month also support SUN-SAT, JAN-DEC

* It will fail under the following scenarios
    * If the cron expression is not standard (example: `SUN,MON`)
    * If value is given to the wrong place (example: `*/15 JAN 1,15 * 1-5 /user/bin/`)
    * If the expression is incorrect (example: `*/15 0 1,15 * 1- /user/bin/`)
    * If the the increase step is greater than the limit (example: `*/100 0 1,15 * 1- /user/bin/`)
