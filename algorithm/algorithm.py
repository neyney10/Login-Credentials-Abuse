
import math
import logging
import numpy as np
import pandas as pd

######################################################
# Module logger
logger = logging.getLogger('algorithm')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('algorithm.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(sh)
##
logger_res = logging.getLogger('algorithm-results')
logger_res.setLevel(logging.DEBUG)
fh2 = logging.FileHandler('algorithm-results.log')
fh2.setLevel(logging.DEBUG)
fh2.setFormatter(formatter)
logger_res.addHandler(fh2)

######################################################

class Algorithm():
    def __init__(self, data, subsetting_method, features):
        self.data = data
        self.subsetting_method = subsetting_method
        self.benign_fail_succ_ratio = None
        self.features = features

        # logger

    def run(self):
        logger.debug('Starting to subset the data')
        subsets = self.subsetting_method.subset(self.data)
        logger.debug('Finished to subset the data')

        logger.debug('Starting to estimate benign failure ratio')
        (self.benign_fail_succ_ratio, subset_index) = self.__estimate_benign_failure_ratio([subsets[5]])
        logger.debug('Finished to estimate benign failure ratio: '+ str(self.benign_fail_succ_ratio) + ', index: '+str(subset_index))
        subset_index=5
        logger.debug('Starting to calculate p')
        p = self.__calculate_p(self.benign_fail_succ_ratio)
        logger.debug('Finished to calculate p: '+ str(p))

        logger.debug('Starting to calculate features...')
        #debug
        results = np.zeros((len(self.features), len(subsets), 6))
        #debug
        for fi, feature in enumerate(self.features):
            logger.debug('Feature: '+feature.__class__.__name__)

            how_common_in_benign = self.__estimate_how_common_feature_benign(subsets[subset_index], feature) # TODO: dependency inversion of feature.
            logger.debug('How common in benign: '+ str(how_common_in_benign *100)+'%')

            for i, subset in enumerate(subsets):
                logger.debug('Looking at subset index of: '+ str(i))
                subset_at_test = subset
                pre_observation_odds = self.__estimate_pre_observation_odds(subset_at_test, self.benign_fail_succ_ratio, p)
                results[fi,i, 0] = pre_observation_odds # fi=feature index, i=subset index, 0=pre obser index.
                logger.debug('pre_observation_odds: '+ str(pre_observation_odds))

                alpha = self.__calculate_alpha(pre_observation_odds)
                results[fi,i, 1] = alpha # fi=feature index, i=subset index, 1=alpha.
                logger.debug('alpha: '+ str(alpha))

                how_common_feature_subset = self.__how_common_feature_in_subset(subset, feature)
                results[fi,i, 5] = how_common_feature_subset # fi=feature index, 5=subset index, 2=how_common_feature_subset
                likelihood_ratio = self.__calculate_likelihood_ratio(subset_at_test, how_common_in_benign, alpha, how_common_feature_subset)
                results[fi,i, 2] = likelihood_ratio # fi=feature index, i=subset index, 2=likelihood ratio.
                logger.debug('likelihood_ratio: '+ str(likelihood_ratio))
                
                post_observation_odds = self.__calculate_post_observation_odds(likelihood_ratio, pre_observation_odds)
                results[fi,i, 3] = post_observation_odds # fi=feature index, i=subset index, 3=post obser.
                logger.debug('post_observation_odds: '+ str(post_observation_odds))

                results[fi,i, 4] = len(subset_at_test[subset_at_test['IsMal']==1])/len(subset_at_test.index) # fi=feature index, i=subset index, 4=Mal/Total.


        for feature_result in results:
            logger_res.debug(pd.DataFrame(feature_result, columns=['Psi','Alpha','(Phi)-likelihood-ratio','Post-obs-odds','Mal/Total','How_common']))


    def __estimate_benign_failure_ratio(self, auth_subsets): # constant c hat
        min_ratio = 1 # starting with max value.
        susbet_index = -1 # index of the subset that minimizes min_ratio
        for k, subset in enumerate(auth_subsets):
            outcomes = subset.groupby('Outcome')
            # sum login success
            try:
                num_of_succ = len(outcomes.get_group('Success').index)
            except: # failsafe, todo: change
                num_of_succ = 1
            # sum login failure
            try:
                num_of_fail = len(outcomes.get_group('Fail').index)
            except: # failsafe, todo: change
                num_of_fail = 1
            # compute ratio fail/succ
            ratio = num_of_fail/num_of_succ
            # compare with current min_ratio
            min_ratio = min(min_ratio, ratio)
            susbet_index = k if min_ratio == ratio else susbet_index

            # DEBUG
            print(ratio)
        
        return (min_ratio, susbet_index)

    def __calculate_p(self, benign_fail_succ_ratio): # TODO: give meaningful name.
        return benign_fail_succ_ratio/(1+benign_fail_succ_ratio)
        
    def __estimate_how_common_feature_benign(self, benign_subset, feature): 
        featured_benign_subset = feature.filter(benign_subset)
        return len(featured_benign_subset.index)/len(benign_subset.index)

    def __estimate_pre_observation_odds(self, subset, benign_fail_succ_ratio, p):
        # TODO: complete, this is only a template.
        outcomes = subset.groupby('Outcome')
        # sum login success
        try:
            num_of_succ = len(outcomes.get_group('Success').index)
        except: # failsafe, todo: change
            num_of_succ = 1
        # sum login failure
        try:
            num_of_fail = len(outcomes.get_group('Fail').index)
        except: # failsafe, todo: change
            num_of_fail = 1
        # compute ratio fail/succ
        ratio = num_of_fail/num_of_succ

        pre_observation_odds = (ratio*(1/benign_fail_succ_ratio) -1) *p

        return pre_observation_odds
    
    def __calculate_alpha(self, pre_observation_odds): # TODO: give meaningful name.
        return 1/(1+pre_observation_odds)

    def __calculate_likelihood_ratio(self, subset, how_common_in_benign, alpha, how_common_feature_subset):
        if alpha==1:
            return 0
        if how_common_in_benign==0:
            how_common_in_benign = 1/len(subset.index) # failsafe - need to do something better here.

        return (how_common_feature_subset - alpha*how_common_in_benign)/((1-alpha)*how_common_in_benign)

    def __calculate_post_observation_odds(self, likelihood_ratio, pre_observation_odds):
        return likelihood_ratio*pre_observation_odds

    def __how_common_feature_in_subset(self, subset, feature):
        featured_subset = feature.filter(subset)
        how_common_feature_subset = len(featured_subset.index)/len(subset.index)
        return how_common_feature_subset