from user_agents import parse
import numpy as np

class DefaultFeature():
    def filter(self, auths):
        # all usernames that start with C15
        return auths[(auths["Username"] > 'C15') & (auths["Username"] < 'C16')]

class UserAgentWindows10Chrome80Feature():
    # Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36
    def filter(self, auths):
        return auths[auths['Useragent'] == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36']

class UserAgentWindows10Firefox57Feature():
    # Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0
    def filter(self, auths):
        return auths[auths['Useragent'] == 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0']

class Top3PasswordFeature():
    def filter(self, auths):
        # add: (auths['Outcome'] == 'Fail') to filter only failures
        return auths[(auths['Outcome'] == 'Fail') & ((auths['Password'] == '123456') | (auths['Password'] == '123456789') | (auths['Password'] == 'qwerty'))]

class Top3BeginAt100PasswordFeature():
    def filter(self, auths): 
        # add: (auths['Outcome'] == 'Fail') to filter only failures
        return auths[(auths['Outcome'] == 'Fail') & ((auths['Password'] == 'q1w2e3r4') | (auths['Password'] == 'michelle') | (auths['Password'] == 'nicole'))]

class UserAgentSafariFeature(): # Browser
    def filter(self, auths):
        return auths[auths['Browser Family'] == 'Safari']

class UserAgentChromeFeature(): # Browser
    def filter(self, auths):
        return auths[auths['Browser Family'] == 'Chrome']

class UserAgentOperaFeature(): # Browser
    def filter(self, auths):
        return auths[auths['Browser Family'] == 'Opera']

class OSFamilyWindowsFeature(): # OS
    def filter(self, auths):
        return auths[auths['OS Family'] == 'Windows']

class OSFamilyMacFeature(): # OS
    def filter(self, auths):
        return auths[auths['OS Family'] == 'Mac OS X']

class Top50PasswordFeature(): # OS
    def filter(self, auths):
        passwords = ["123456","123456789","qwerty","111111","12345678","abc123","1234567","12345","1234567890","123123","0","iloveyou","1234","1q2w3e4r5t","qwertyuiop","123","monkey","123456a","dragon","123321","654321","666666","1qaz2wsx","myspace1","121212","123qwe","a123456","1q2w3e4r","123abc","qwe123","7777777","tinkle","qwerty123","qwerty1","222222","zxcvbnm","987654321","555555","asdfghjkl","112233","1q2w3e","123123123","qazwsx","computer","12345a","princess","159753","1234qwer","michael","iloveyou1"]
        return auths[(auths['Outcome'] == 'Fail') & (np.isin(auths['Password'],passwords))]


class Top100PasswordFeature(): # OS
    def filter(self, auths):
        passwords = ["123456","123456789","qwerty","111111","12345678","abc123","1234567","12345","1234567890","123123","0","iloveyou","1234","1q2w3e4r5t","qwertyuiop","123","monkey","123456a","dragon","123321","654321","666666","1qaz2wsx","myspace1","121212","123qwe","a123456","1q2w3e4r","123abc","qwe123","7777777","tinkle","qwerty123","qwerty1","222222","zxcvbnm","987654321","555555","asdfghjkl","112233","1q2w3e","123123123","qazwsx","computer","12345a","princess","159753","1234qwer","michael","iloveyou1","football","sunshine","789456123","aaaaaa","ashley","11111","princess1","777777","123654","11111111","daniel","999999","asdfgh","888888","football1","abcd1234","love","12qwaszx","love123","monkey1","jordan23","asdf","a12345","123456789a","shadow","azerty","jessica","superman","samsung","asd123","88888888","charlie","baseball","michael1","master","jesus1","babygirl1","qwert","soccer","killer","qwer1234","blink182","789456","jordan","333333","gfhjkm","thomas","Status","131313","q1w2e3r4"]
        return auths[(auths['Outcome'] == 'Fail') & (np.isin(auths['Password'],passwords))]