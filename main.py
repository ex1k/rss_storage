import feedparser
import sys
import sqlite3 as lite

def read_rss(url, rss_name):
    con = lite.connect('rss.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS '+rss_name+' (title TEXT, date TEXT)')
    rss = feedparser.parse(url)
    for post in rss.entries:
        date_entry = []
        for i in range(0,6):
            if (post.published_parsed[i] < 10):
                date_entry.append("0" + str(post.published_parsed[i]))
            else:
                date_entry.append(str(post.published_parsed[i]))
        date="%s-%s-%s %s:%s:%s" % (date_entry[0], date_entry[1], date_entry[2], date_entry[3], date_entry[4], date_entry[5])
        del date_entry[:]
        con.execute('INSERT INTO '+rss_name+' SELECT "'+post.title+'", "'+date+'" WHERE NOT EXISTS(SELECT 1 FROM '+rss_name+' WHERE title="'+post.title+'" and date="'+date+'")')
    con.commit()

def get_rss(rss_name):
        con = lite.connect('rss.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM "+rss_name+" ORDER BY datetime(date) DESC")
        rows = cur.fetchall()
        for row in rows:
            print "%s %s" % (row[0], row[1])

def main():
    args = sys.argv[1:]
    rss_names = {}
    if not args:
        print 'use: main.py [-refresh] rss_name, [url]'
        sys.exit(1)
    else:
        if (len(args) == 1):
            if (args[0] == "-refresh"):
                for key in rss_names:
                    read_rss(rss_names[key], key)
            else:
                get_rss(args[0])
        if (len(args) == 2):
            rss_names[args[0]] = args[1]
            read_rss(args[1], args[0])

if __name__ == "__main__":
    main()
