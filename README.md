# A tg-Bot for a Lighting Company💡

![Python ver](https://img.shields.io/badge/python-3.8-orange) ![Aiogram 3.x](https://img.shields.io/badge/aiogram-3.8.0-blue) ![Redis ver](https://img.shields.io/badge/Redis-3.0.504-red)

The bot implements a connection to the **```DB```**, working with the **```State Machine```** and **```2 Roles```** of using the bot. As well as **```Сallbacks```**

## Requirements

#### *You can install in requirements.txt file)*
.

***Addition***

library... - a very effective and simple solution when it comes to storing **```passwords, tokens```**, etc. Just install the library and write to the **```.env```** file what we do not want to distribute.
 

 Don't forget to specify the file name in *```.gitignore!!!```*

 ```
 from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv('TOKEN')
PASSWORD = os.getenv('PASSWORD')
```

## 2 Roles

#### Owner-developer

> core > for_devs.py

Standard CRUD work with the database and the state machine is implemented here. To access this block in tg, you will need to pass **```verification```**

![](https://sun9-6.userapi.com/impg/VIoIjHY7hpWellD7HkZouKHbrUS65Z59n7e6-Q/FDNAT6madCw.jpg?size=501x87&quality=96&sign=0af25972eff5d27437b489b57ad97dbd&type=album)

ahah, if you take it into your head to sort out the "'/edit"' blocks, I wish you good luck!😅 I'm facing a circular import problem here

The **<u>full list of commands</u>** for this role is in the file:

> core > commands.py > list [commands_for_devs]


#### Simple User

> core > callbacks > callbacks_main.py

In my opinion, the simplest **```interaction with the interface```** will be communication through buttons. **```Inline-buttons```**. Because they are more beautiful!


* **Search by name** 

    It was cached! 
    
    The project uses aioredis, but uses **```redis```** in the signature. This means that it also **```needs to be installed```**, otherwise nothing will work.


* **Basic branching by catalog**:

    ![](https://sun9-37.userapi.com/impg/0ZAJhud0mlli-SIXyMtcxrleqOcnoOKEb-7CwA/eZ-IUTjsWUc.jpg?size=1100x1400&quality=95&sign=8461a5541a09b36c837a8936cfb32bd4&type=album)

## DataBase: SQLiter

sqlite3 was used in the project. It was implemented through a class in a separate file

> core > SQLite_block.py

![](https://sun9-77.userapi.com/impg/cbRogvq1-0I2t-XOZaCV1USUf3iBkcaHx5aJbA/frjGWUF-t50.jpg?size=666x831&quality=95&sign=e0aa88d9b800d56b50dca222cb6daf4c&type=album)

## Callbacks

All the work is in the folder

> core > callbacks >

* > callbacks_main.py

    In turn, they were combined into one function - it is convenient that such a design is **```registered```** by the dispatcher ***```once```***. Any changes will be processed automatically

* Callback levels indicate branching from the 1st level (category) to the 4th (specific position in the catalog)

    ![](https://sun9-16.userapi.com/impg/6kz1nY-wB5wkW9upzwMkONy1acXWc9-fqxAfUg/mfLfoVcuwS4.jpg?size=188x153&quality=95&sign=7c06fcdf4dc16ab55f09a87b3dd73cfb&type=album)
    *  the 1st level is in the:
        > core > subcore.py > menu()

## Other

* The **```state machine```** and most of the project **```keyboards```** are located here
    > core > callbacks > utils

    ![](https://sun9-60.userapi.com/impg/Dw61Szca0depKs52nCE3opMbmYLng3vFvaLl8Q/QNYvADNOHaQ.jpg?size=187x130&quality=96&sign=645a12d1cb180de1958d6fb518d1bbfa&type=album)



# Thanks for reading!
.

.

.

.
## P.S: Difficulties
*    ####    Here I will highlight the difficult points when reading and understanding the code
    
     *  > core > for_devs.py > '''/search'''

        ### !!! *this has been replaced by redis at the moment* !!!

        It was difficult with the search, because it had to be optimized: Imagine that you enter a common word for a group of products into the query. There are about 1000 of them. The original version, with such a request, would simply spit out 1000 entries without a limit in telegrams. The reaction to such a phenomenon is obvious. I limited the allowed outlier to 10 per message and added the ability to show the rest of the entries at 10 per click. I also really wanted not to load the database. That's why I tried to speed up this operation. The solution was the cache. I was pleasantly surprised by the lru_cache decorator that was already ready for my needs.
        ![](https://sun9-8.userapi.com/impg/ds3zlt6KHS_q_6-VkXxvheoDYH3I6Hd7jvI48A/x3tRlojCWF8.jpg?size=679x240&quality=96&sign=2d149f54486ba33a286df8891a678f3c&type=album)
    
     * > core > callbacks > utils > keyboards.py > get_keyboard_3lvl_branch()

        In this function, it was necessary to conduct the received data through a "filter". An exception would occur if we went beyond the range of values in the loop or caught a KeyError. It's very easy to get confused in moving from a list to a tuple, then to an element, after which you can select a character from a string by index - do you agree?  
