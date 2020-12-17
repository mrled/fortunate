# Creating fortune databases from tweets

There are some users whose tweets make excellent fortune databases. Two of my favorites are [@ctrlcreep](https://twitter.com/ctrlcreep) and [@QuietPineTrees](https://twitter.com/QuietPineTrees)

Each of these accounts publishes lots of single-tweet speculative fiction. `tweetfortune.py` collects all tweets which have no pictures or videos, no URLs, are not replies or RTs, and are not part of a tweetstorm.

## Running `tweetfortune.py`

You will need a Twitter "app" (see <http://developer.twitter.com>), which will provide four secrets - consumer key, consumer secret, access key, and access secret.

Run it like so:

```sh
python3 tweetfortune.py --debug \
    TWITTER_USER \
    --consumer-key CONSUMER_KEY \
    --consumer-secret CONSUMER_SECRET \
    --access-key ACCESS_KEY \
    --access-secret ACCESS_SECRET
```

It will then create `TWITTER_USER.DATE.tweets`. To use with `fortune`, make sure to run `strfile TWITTER_USER.DATE.tweets`. Then you can run `fortune TWITTER_USER.DATE.tweets`. Nice.

## Examples

The result is pretty lovely.

```
$ fortune ctrlcreep.20201216.tweets | fold -w 80 -s
AIs are fighting in the cyber-trenches over whether to use emojis or emoticons,
while humans lounge in decadent ignorance—don't you understand, your ability to
process emotive ambiguity makes you a GOD
 - @ctrlcreep on September 26, 2019
   https://twitter.com/ctrlcreep/status/1177091814781833217

$ fortune ctrlcreep.20201216.tweets | fold -w 80 -s
Yes, I use 64 bits to store a bool, but only because my bespoke logic system
acknowledges 2^64 possible truth values
 - @ctrlcreep on May 20, 2019
   https://twitter.com/ctrlcreep/status/1130348752148025344

$ fortune ctrlcreep.20201216.tweets | fold -w 80 -s
Our universe obeys the law of conservation of pain. When you're hurting, take
solace that your agony is another's relief
 - @ctrlcreep on February 20, 2019
   https://twitter.com/ctrlcreep/status/1098033641849012225

$ fortune ctrlcreep.20201216.tweets | fold -w 80 -s
The REAL "cryptocurrency" is buying Christmas presents for your friends, and
thereby investing in their lifelong loyalty as enforced by a distributed social
ledger of perceived gift-debt
 - @ctrlcreep on December 13, 2019
   https://twitter.com/ctrlcreep/status/1205526007341600769

$ fortune QuietPineTrees.20201216.tweets | fold -w 80 -s
Prohibition on leaving Earth was a big time for space flight bootleggers.
Chrome rockets fled the planet on ethanol fuel from hidden stills.
 - @QuietPineTrees on August 14, 2017
   https://twitter.com/QuietPineTrees/status/897165892123062272

$ fortune QuietPineTrees.20201216.tweets | fold -w 80 -s
Element #94.5 Penultimum (Pe)
The epitome of the quantum Zeno effect, this metal must be constantly watched
or will decay instantly to lead.
 - @QuietPineTrees on March 21, 2015
   https://twitter.com/QuietPineTrees/status/579372100869316609

$ fortune QuietPineTrees.20201216.tweets | fold -w 80 -s
In the worst cases, echoes could turn feral, insulting their masters and
publicly shouting their secrets. Heterodyne dialysis was required.
 - @QuietPineTrees on April 04, 2015
   https://twitter.com/QuietPineTrees/status/584460663784898560

$ fortune QuietPineTrees.20201216.tweets | fold -w 80 -s
The admin cast a dubious eye over his résumé. "I'm not sure about these
degrees," she said. "What's cryptomycology, or theoretical anatomy?"
 - @QuietPineTrees on March 16, 2015
   https://twitter.com/QuietPineTrees/status/577590306503282688
```
