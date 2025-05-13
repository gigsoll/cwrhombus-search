# About

This project is all about finding rhombuses and squares in heap of random points using object oriented programming and things I've learned at Algorithms and Data Structures classes. It uses lists, hash tables, tuples, linked-lists (with custom implementation) and other data structures.

The problem which were solving is

> The file contains coordinates of points. View these points on the screen. Using the points as vertices, construct and display all possibilities of rhombuses that do not have common vertices. It is necessary to construct as many shapes as possible. Highlight the squares in a separate color.

To solve this problem two following solutions were created
- Brute Force (n^4 time and space) – the first solution which come in my mind and I am not proud of it but decidet to keep (also here is some optimization so it isn't that horrible as it could be)
- Vector math approach

## Vector math approach

The main principle of this approach is to utilize vector math and one of the characteristics of rhombuses

> Diagonals of a Rhombus are intercepting at the right angle and are divided to two equal parts 

This algorithm works like this:

1. creates all possible pairs of points
2. sort them from shortest to longest
3. for each point find a center and shoot two vectors in opposite sides and check all the points which are on these vectors
4. If two points from opposite sides have the same distance from center it is a Rhombus
5. After this rhombus is created, its points added to set of unique points

## About UI

UI is done using Qt6 with custom theme (it is the reason why window can not be resized, to preserve beauty of the background). 
UI takes deep inspiration from NieR:Automata GUI, and to achieve this result custom themes for matplotlib and Qt were written.

# So how to install and use?

```
git clone https://github.com/gigsoll/cwrhombus-search/
cd cwrhombus-search
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

I was trying my best while creating this application

# Some screenshots

![](/media/ui1.png)

![](/media/ui2.png)