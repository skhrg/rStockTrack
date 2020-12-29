import re
import praw
from yahoo_fin import stock_info as si
import numpy as np
from datetime import date

PATH = "../personal-site/_posts/spacs/"

def save_md(spacs):
    spacs = np.array([[k]+v for k, v in spacs.items()])
    today = str(date.today())
    
    spacs = spacs[spacs[:,0].argsort()]
    header = "--- \n layout: post \n title: Summary for " + today + "\n category: spacs \n--- \n\n# r/SPACs summary for " + today + " \n\nTICKER|[POSTS](../spacs-summary-posts)|[UPVOTES](../spacs-summary-upvotes)|[VALUE](../spacs-summary-value)\n ---|---|---|---\n"
    with open(PATH+today+"-spacs-summary.md", "w") as f:
        f.write(header)
        f.close()
    with open(PATH+today+"-spacs-summary.md", "ab") as f:
        np.savetxt(f, spacs, fmt='%s', delimiter="|")
        f.close()

    spacs = spacs[spacs[:,1].astype(np.int).argsort()[::-1]]
    header = "--- \n layout: post \n title: Summary for " + today + "\n category: spacs \n hidden: true \n--- \n\n# r/SPACs summary for " + today + " \n\n[TICKER](../spacs-summary)|POSTS|[UPVOTES](../spacs-summary-upvotes)|[VALUE](../spacs-summary-value)\n ---|---|---|---\n"
    with open(PATH+today+"-spacs-summary-posts.md", "w") as f:
        f.write(header)
        f.close()
    with open(PATH+today+"-spacs-summary-posts.md", "ab") as f:
        np.savetxt(f, spacs, fmt='%s', delimiter="|")
        f.close()

    spacs = spacs[spacs[:,2].astype(np.int).argsort()[::-1]]
    header = "--- \n layout: post \n title: Summary for " + today + "\n category: spacs \n hidden: true \n--- \n\n# r/SPACs summary for " + today + " \n\n[TICKER](../spacs-summary)|[POSTS](../spacs-summary-posts)|UPVOTES|[VALUE](../spacs-summary-value)\n ---|---|---|---\n"
    with open(PATH+today+"-spacs-summary-upvotes.md", "w") as f:
        f.write(header)
        f.close()
    with open(PATH+today+"-spacs-summary-upvotes.md", "ab") as f:
        np.savetxt(f, spacs, fmt='%s', delimiter="|")
        f.close()

    spacs = spacs[spacs[:,3].astype(np.float).argsort()[::-1]]
    header = "--- \n layout: post \n title: Summary for " + today + "\n category: spacs \n hidden: true \n--- \n\n# r/SPACs summary for " + today + " \n\n[TICKER](../spacs-summary)|[POSTS](../spacs-summary-posts)|[UPVOTES](../spacs-summary-upvotes)|VALUE\n ---|---|---|---\n"
    with open(PATH+today+"-spacs-summary-value.md", "w") as f:
        f.write(header)
        f.close()
    with open(PATH+today+"-spacs-summary-value.md", "ab") as f:
        np.savetxt(f, spacs, fmt='%s', delimiter="|")
        f.close()

def get_spacs(reddit):
    spacs = {}
    not_spacs = []

    for submission in reddit.subreddit("SPACs").top("day", limit=100):
        all_words = submission.title + ' ' + submission.selftext
        all_words = re.sub(r"[^\w]", " ",  all_words)
        all_words = re.findall(r"([A-Z]+[^a-z\W\d])", all_words)
        for word in all_words:
            if word in spacs.keys():
                spacs[word][0] += 1
                spacs[word][1] += submission.score
            else:
                if word in not_spacs:
                    continue
                try:
                    price = si.get_live_price(word)
                    if np.isnan(price):
                        not_spacs.append(word)
                        continue
                    spacs[word] = [0,0,0]
                    spacs[word][0] = 1
                    spacs[word][1] = submission.score
                    spacs[word][2] = price
                except:
                    not_spacs.append(word)
    return spacs

reddit = praw.Reddit(
        client_id="ccIRAkiGGdLWQw",
        client_secret="T7iifHWKy3kgRrPd8Nk2KCCTsKhw7A",
        user_agent="linux:com.saianeesh.spacs:v1.0 (by /u/lordskh)"
        )

spacs = get_spacs(reddit)
save_md(spacs)
