import re
import praw
from yahoo_fin import stock_info as si
import numpy as np
from datetime import date
import argparse

PATH = "../personal-site/_posts/"

def save_md(stocks, sub):
    path = PATH + sub + "/"

    stocks = np.array([[k]+v for k, v in stocks.items()])
    today = str(date.today())
    
    stocks = stocks[stocks[:,0].argsort()]
    header = "--- \n layout: post \n title: Summary for " + today + "\n category: " + sub + " \n--- \n\n# r/" + sub + " summary for " + today + " \n\nTICKER|[POSTS](../" + sub + "-summary-posts)|[UPVOTES](../" + sub + "-summary-upvotes)|[VALUE](../" + sub + "-summary-value)\n ---|---|---|---\n"
    with open(path+today+"-" + sub + "-summary.md", "w") as f:
        f.write(header)
        f.close()
    with open(path+today+"-" + sub + "-summary.md", "ab") as f:
        np.savetxt(f, stocks, fmt='%s', delimiter="|")
        f.close()

    stocks = stocks[stocks[:,1].astype(np.int).argsort()[::-1]]
    header = "--- \n layout: post \n title: Summary for " + today + "\n category: " + sub + " \n hidden: true \n--- \n\n# r/" + sub + " summary for " + today + " \n\n[TICKER](../" + sub + "-summary)|POSTS|[UPVOTES](../" + sub + "-summary-upvotes)|[VALUE](../" + sub + "-summary-value)\n ---|---|---|---\n"
    with open(path+today+"-" + sub + "-summary-posts.md", "w") as f:
        f.write(header)
        f.close()
    with open(path+today+"-" + sub + "-summary-posts.md", "ab") as f:
        np.savetxt(f, stocks, fmt='%s', delimiter="|")
        f.close()

    stocks = stocks[stocks[:,2].astype(np.int).argsort()[::-1]]
    header = "--- \n layout: post \n title: Summary for " + today + "\n category: " + sub + " \n hidden: true \n--- \n\n# r/" + sub + " summary for " + today + " \n\n[TICKER](../" + sub + "-summary)|[POSTS](../" + sub + "-summary-posts)|UPVOTES|[VALUE](../" + sub + "-summary-value)\n ---|---|---|---\n"
    with open(path+today+"-" + sub + "-summary-upvotes.md", "w") as f:
        f.write(header)
        f.close()
    with open(path+today+"-" + sub + "-summary-upvotes.md", "ab") as f:
        np.savetxt(f, stocks, fmt='%s', delimiter="|")
        f.close()

    stocks = stocks[stocks[:,3].astype(np.float).argsort()[::-1]]
    header = "--- \n layout: post \n title: Summary for " + today + "\n category: " + sub + " \n hidden: true \n--- \n\n# r/" + sub + " summary for " + today + " \n\n[TICKER](../" + sub + "-summary)|[POSTS](../" + sub + "-summary-posts)|[UPVOTES](../" + sub + "-summary-upvotes)|VALUE\n ---|---|---|---\n"
    with open(path+today+"-" + sub + "-summary-value.md", "w") as f:
        f.write(header)
        f.close()
    with open(path+today+"-" + sub + "-summary-value.md", "ab") as f:
        np.savetxt(f, stocks, fmt='%s', delimiter="|")
        f.close()

def get_stocks(reddit, sub):
    stocks = {}
    not_stocks = []

    for submission in reddit.subreddit(sub).top("day", limit=100):
        all_words = submission.title + ' ' + submission.selftext
        all_words = re.sub(r"[^\w]", " ",  all_words)
        all_words = re.findall(r"([A-Z]+[^a-z\W\d])", all_words)
        for word in all_words:
            if word in stocks.keys():
                stocks[word][0] += 1
                stocks[word][1] += submission.score
            else:
                if word in not_stocks:
                    continue
                try:
                    price = si.get_live_price(word)
                    if np.isnan(price):
                        not_stocks.append(word)
                        continue
                    stocks[word] = [0,0,0]
                    stocks[word][0] = 1
                    stocks[word][1] = submission.score
                    stocks[word][2] = price
                except:
                    not_stocks.append(word)
    return stocks

parser = argparse.ArgumentParser()
parser.add_argument("subreddit", type = str, help = "subreddit to scrape tickers from")
args = parser.parse_args()
sub = args.subreddit

reddit = praw.Reddit(
        client_id="ccIRAkiGGdLWQw",
        client_secret="T7iifHWKy3kgRrPd8Nk2KCCTsKhw7A",
        user_agent="linux:com.saianeesh.spacs:v1.0 (by /u/lordskh)"
        )

stocks = get_stocks(reddit, sub)
save_md(stocks, sub)
