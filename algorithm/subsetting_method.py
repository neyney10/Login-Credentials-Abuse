import pandas as pd
from user_agents import parse

class DefaultSubsettingMethod():
    '''
    Subsetting login attempts to bins. by time
    '''
    def __init__(self, number_of_subsets: int) -> None:
        self.number_of_subsets = number_of_subsets

    def subset(self, auths):
        amount_of_auths = len(auths.index)
        # sort:
        auths.sort_values('Time', inplace=True)
        subsets = []
        for i in range(self.number_of_subsets):
            intervalBegin = (i/self.number_of_subsets) *amount_of_auths
            intervalEnd = ((i+1)/self.number_of_subsets) *amount_of_auths
            subsets.append(auths[int(intervalBegin):int(intervalEnd)])
        
        return subsets


class UsernameSubsettingMethod():
    def __init__(self, number_of_subsets: int) -> None:
        self.number_of_subsets = number_of_subsets

    def subset(self, auths):
        auths = auths.sample(frac=1).reset_index(drop=True) # shuffle
        amount_of_auths = len(auths.index)
        subsets = []

        unique_usernames_groups = auths.groupby('Username')
        subset = []
        subset_size = 0
        for username, username_group in unique_usernames_groups:
            subset.append(username_group)
            subset_size = subset_size + len(username_group.index)
            if subset_size > amount_of_auths/self.number_of_subsets:
                subsets.append(pd.concat(subset))
                subset = []
                subset_size = 0
        
        subset_size = len(subset)
        if subset_size > 0:
            subsets.append(pd.concat(subset))

        return subsets


class BrowserFamilySubsettingMethod():
    def __init__(self, number_of_subsets: int) -> None:
        self.number_of_subsets = number_of_subsets

    def subset(self, auths):
        subsets = []
        # aggregate
        agg_browser = ['Yandex Browser','IE','UC Browser','Coc Coc','QQ Browser','Vivaldi','Firefox','Sogou Explorer','Whale','Other','Apple Mail','Iron','Maxthon']
        #auths.loc[auths['Browser Family'].isin(agg_browser),'Browser Family']='Other'

        unique_browser_family_groups = auths.groupby('Browser Family', sort=False)
        for browser_family, browser_family_group in unique_browser_family_groups:
            subsets.append(browser_family_group)
            print(browser_family)

        # DEBUG
        print('#Sets:', len(subsets))
        for i,s in enumerate(subsets):
            print(i, 'Set size:', len(s.index))
        # END DEBUG
        return subsets


class OSFamilySubsettingMethod():
    def __init__(self, number_of_subsets: int) -> None:
        self.number_of_subsets = number_of_subsets

    def subset(self, auths):
        subsets = []
        agg_os = ['Fedora','Other','Ubuntu','Chrome OS','Linux']
        auths.loc[auths['OS Family'].isin(agg_os),'OS Family']='Other'

        unique_os_family_groups = auths.groupby('OS Family', sort=False)
        for os_family, os_family_group in unique_os_family_groups:
            subsets.append(os_family_group)
            print(os_family)

        # DEBUG
        print('#Sets:', len(subsets))
        for i,s in enumerate(subsets):
            print(i, 'Set size:', len(s.index))
        # END DEBUG
        return subsets





