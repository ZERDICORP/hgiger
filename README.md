# hgiger
#### Application for storing notes.
## What the f*** ? :expressionless:

Calm down, it's only **2972** lines of "Best" Python Code.. :alien:  

But seriously, this is one of my **first** more or less large projects, created a long time ago, at the beginning of my journey (I think it was at the end of **2017**).  

2 more years after the creation of this application, I used it every day, so the database has accumulated 3.5 mb of ~selected shit~ various notes.

**Just today I decided to shed some light on this!**

## How to try it? :man_with_gua_pi_mao:

> It's a python (MY SWEET CANDY AND TERRIBLE DREAM), so there shouldn't be any problems with the installation.

#### Clone the repository
```
$ git clone https://github.com/ZERDICORP/hgiger.git
```

#### We need python 3 & pip
```
$ python -V
Python 3.10.2
$ pip -V
pip 21.0 from /usr/lib/python3.10/site-packages/pip (python 3.10)
```

#### Install dependencies
```
$ cd hgiger/src/
$ pip install -r .deps
```

#### And you can already start this clunker
> Since I am generous, I am ready to share my notes with you.  
> Yes, yes, I loaded my database in this repo.  
> Enjoy! xD
```
$ python main.pyw
```

## Interesting Features :poop:

### 1. Cluster > Cell > Section > Note > Page

This app has 5 levels.  
Below are screenshots so as not to rant.

<details>
  <summary>clusters</summary>
    
  ![image](https://user-images.githubusercontent.com/56264511/161407950-8f6d546c-669b-4a75-b89b-ee0bbeca5a65.png)
</details>

<details>
  <summary>cells</summary>
    
  ![image](https://user-images.githubusercontent.com/56264511/161407992-94236187-a30b-4c5c-8b89-b4afda509570.png)
</details>

<details>
  <summary>sections</summary>
    
  ![image](https://user-images.githubusercontent.com/56264511/161408054-03d08e45-7644-4b7a-b210-788833e156b7.png)
</details>

<details>
  <summary>notes</summary>
    
  ![image](https://user-images.githubusercontent.com/56264511/161408143-445cc9d0-3eac-4a66-9509-9cd7d166822e.png)
</details>

<details>
  <summary>pages</summary>
    
  ![image](https://user-images.githubusercontent.com/56264511/161408187-c5ab9fe3-c732-453e-bb89-07ff253dfd76.png)
</details>

### 2. Tag Finder

To quickly find a particular note, you can use the tag finder.  
To call it, press the key combination `Ctrl + F` (only works when you are in a **cell**).

<details>
  <summary>screenshot</summary>
    
  ![image](https://user-images.githubusercontent.com/56264511/161408265-2ecf1641-ac9f-40e7-afed-26e89527ce30.png)
</details>

### 3. Database backup

This is the funniest part..  
For you to understand, I made a telegram bot located in hgiger itself for backup.  
It starts only when we make a backup, and immediately closes.  
All he does is upload the file to telegram at the specified chat_id.

P.S. that's why I like to clean up my old crafts, lol)

First, go to the _clone menu_ with the key combination `Ctrl + M`.

<details>
  <summary>screenshot</summary>
    
  ![image](https://user-images.githubusercontent.com/56264511/161408435-f479a99f-68fd-4250-a24a-3c2c31256140.png)
</details>

> As you can see, I apparently planned to make alternative ways to clone the database, since I left so much space and even created a whole menu :frog:  

Well, let's choose the first one.

<details>
  <summary>screenshot</summary>
    
  ![image](https://user-images.githubusercontent.com/56264511/161408542-39ff5f6a-5522-4f7b-901c-33444ebb43ef.png)
</details>

Now we click on the button with a strange icon, confirm our desire to make a clone of the database and wait for confirmation.

<details>
  <summary>screenshot</summary>
    
  ![image](https://user-images.githubusercontent.com/56264511/161408577-a625b9b4-a7cc-4731-997b-8dfa99cb58a4.png)
</details>

Magic :hear_no_evil:

Obviously, if you also want to make yourself such a ~fucking~ good backup method, just create a telegram bot and write the token to the `modules/hgigerbot/config.json` file. In addition to the token, you will need to find out your chat_id and also write it to the config.

### 4. Сonsole utility - hggr

Right!  
We have **hgiger** (a full-featured graphical application), and **hggr** (a small console utility for finding and copying notes).  

Since some of my notes were literally code files, sometimes I wanted to copy them quickly.  
I was wildly too lazy to open **hgiger**, which was so slow, so I created it - **hggr**.  

Here is a simple (x1) usage example:
```
$ python hggr.py
[info]:
	hgiger <tag>
	or
	hgiger <tag1> <tag2> ... <tagN>
```
```
$ python hggr.py sort buble
loading: [......................................] |38|
---------------------------------------------
[0]. [algorithms > "Buble Sorting"] {pages=1}
[1]. [tools > "Sorted Dictionary"] {pages=1}
---------------------------------------------
index: 0
[info]: file "bubleSort.py" successfully created :]
```

It's simple (x2) - we enter tags, get a list of matches and select the index of the note we are interested in.  
The principle of copying notes is just as simple (x3): **one page = one file**.
