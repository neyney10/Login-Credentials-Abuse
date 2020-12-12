# Synthetic data generator
## Description
For details about implementation please see the notebook at ["dev-notebook.ipynb"](./dev-notebook.ipynb)
### Users
- username
- correct user password

Every user should have some unique behavior, such as distribution of user-agent string over time.

Amount of users: 20,000. 

#### <b>How credentials are chosen</b>
- User: Uniformly at random.
- Password: By the distribution given with the "counts" column in the data.

### Benign data
- User-agent string
- Credentials for each authentication request
- Authentication request outcome (Success/Failure) - mostly success (99% succ)
- Max-time: 500,000

Amount of benign auth records: 2,000,000

#### <b> How the data is generated </b>
For each user:
- Amount of authentication requests: Binomial(amount/(#users-1), 0.6)+1 (i.e. around 60% of the average amount per user) and more are generated in order to fill the required amount.
- Time: Uniformly at random between \[0,max-time=500,000]
- User-agent strings: 
- Outcome & password:
    - 99% login success - the password that belongs to the user is then attached to the geenrated record.
    - 1% login failure - 90% to simulate typo (40% to replace a char, 25% to add an unwanted char and 25% to remove a char from the correct password) and 10% to simulate forgotten password by choosing another password unofrmly at random from the list.

### Malicious data
- user-agent string
- credentials for each authentication request - randomly select subset of users, and use 100 most common passwords.
- authentication request outcome (Success/Failure) - mostly failure (98% fail)
- Max-time: 350,000

Amount of mal auth records: 400,000

#### <b> How the data is generated </b>
- Fraction of known usernames to the attacker: 20%.
- Time: Uniformly at random between \[0,max-time=350,000]
- User-agent strings: 
- Outcome & password:
    - 2% login success - the password that belongs to the user is then attached to the generated record (regardless if it is the list of 100 most common passwords that is used).
    - 98% login failure - using 100 most common passwords (in the same passwords file as used to generate the users) uniformly at random at a time.

## Problems with the generation
### The benign requests
- The requests of each user spans unifomly over the time span [0, max-time].
- Browser's useragent is random and chosen at uniform and isn't consisent with single browser that the user can update its version (i.e from Chrome 80 to Chrome 81) and therefore the useragent browser version number is increased but the rest stays the same.
### The malicious requests
- The succ/fail to login is determined purely at random and does not take into account the passwords that the attacker is using, hence, the attacker can access an account without even trying to guess the correct password. Similarly the attacker can fail to login and then one of 100 of his passwords will be attached and it will still fail even if its the correct password.
- Does not declare specific time spans of the attack beside the max-time.
- There (frequently) are more than 3 requests for each user, it might be detected by snort brute-force rules, to overcome this, there could be at most 2 requests per user, i.e. the amount of attack traffic is limited, although we can span it across time.

## Data normalization
As the format user-agent strings are of the form (see [IETF document](https://tools.ietf.org/html/rfc7231#section-5.5.3])):
```
[Compatibility, OS+VERSION, ARCH, ENGINE, BROWSER/VERSION]
```
Like:
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36
```
We then have to parse the contents of each user-agent string when we want to see how many records in our data has X, i.e. if we want to know how many records are using the Chrome web browser, than we have to parse all user-agent string each time that we want to know such a thing.

Because of that we normalized the data to [1NF](https://en.wikipedia.org/wiki/Database_normalization) in order to speed up proccessing time, i.e. we splitted each user-agent to multiple columns such as OS, OS-Version, Browser, Browser-Version...
this siginifcantly improved running-time from around 40-min on unnormalized form of data to 10-seconds on normalized form of data. (In simple words, we just parsed the user-agent strings ahead of time instead of parsing it as part of the algorithm).

## Real-life data distribution of features
### Usernames
There are many datasets in the wild of usernames, such as reddit's and twitters.
We have used the dataset of reddit accounts that can be found at Kaggle.com:
https://www.kaggle.com/colinmorris/reddit-usernames

Usernames are different from each service/platform/app as each one has its name restrictions and community.

### Passwords
We wanted to collect a lot of password from every breach/hack that happend recently and create from that a valid password distribution, although we couldn't find some and we had to use datasets of common-passwords, XATO dataset of passwords that collected over the years is preprocesses and updated list of password, although without their distributions, but are sorted by most-common to least-common.
https://xato.net/today-i-am-releasing-ten-million-passwords-b6278bbe7495

Update: the new version is using hacked password used by haveibeenpwned.com website, proccessed and distributed:
https://github.com/robinske/password-data


### Useragents
Using the library "user-agents" of npm (nodeJS) we could extract the distribution of user-agents strings.
https://github.com/intoli/user-agents

See the extraction code here: [link](./app.js)

### Time
We couldn't find any data regarding of how many times each user logins to a service and when (although we can assume that most logins are during work-hours if the its a business application), so we arbitrary uniformly at random spanned the auth records over time units.


