#!coding=utf-8
import json
import math
from recommender_helper import RecommenderHelper
from recommender_db import RecommenderDB
from recommender import recommend
from collections import Counter


class CoefficientFeature:

    recommender_db = RecommenderDB()

    def __init__(self):
        self.imdbid_genre_dict = self.recommender_db.get_imdbid_feature_dict("genre")
        self.imdbid_actor_dict = self.recommender_db.get_imdbid_feature_dict("actor")
        self.imdbid_imdbkeyword_dict = self.recommender_db.get_imdbid_feature_dict("imdbkeyword")
        self.imdbid_wikikeyword_dict = self.recommender_db.get_imdbid_feature_dict("wikikeyword")
        self.imdbid_vioneltheme_dict = self.recommender_db.get_imdbid_feature_dict("vioneltheme")
        self.imdbid_vionelscene_dict = self.recommender_db.get_imdbid_feature_dict("vionelscene")
        self.imdbid_locationcity_dict = self.recommender_db.get_imdbid_feature_dict("locationcity")
        self.imdbid_locationcountry_dict = self.recommender_db.get_imdbid_feature_dict("locationcountry")





    def __getCosSim(self, indict1, indict2):
        
        indict1_keys = indict1.keys()
        indict2_keys = indict2.keys()
        all_keys = list(set(indict1_keys + indict2_keys))
        indict1_keys_vector = [0] * len(all_keys)
        indict2_keys_vector = [0] * len(all_keys)
        
        for index, key in enumerate(all_keys):
            if key in indict1:
                indict1_keys_vector[index] = indict1[key]
            if key in indict2:
                indict2_keys_vector[index] = indict2[key]


        num1 = sum(map(lambda x: indict1_keys_vector[x] * indict2_keys_vector[x], range(0, len(all_keys))))
        tmp1 = math.sqrt(sum([x ** 2 for x in indict1_keys_vector]))
        tmp2 = math.sqrt(sum([x ** 2 for x in indict2_keys_vector]))
        num2 = tmp1 * tmp2  # num2=sqrt(a1^2+a2^2+a3^2) * sqrt(b1^2+b2^2+b3^2)

        if num2 == 0:
            return 0
        else:
            return float(num1) / num2

    def __getAddedSim(self, indict1, indict2, category_parameter):

        indict1_keys = indict1.keys()
        indict2_keys = indict2.keys()
        all_keys = list(set(indict1_keys + indict2_keys))
        key_match_counter = 0
        for key in all_keys:
            if key in indict1_keys and key in indict2:
                key_match_counter += 1

        return category_parameter * key_match_counter


    def getCategoryNumDict(self, director_imdbids_dict, imdbid_category_dict):
        director_category_dict = {}
        for directorid in director_imdbids_dict:
            movie_list = director_imdbids_dict[directorid]
            category_num_dict = {}

            for movieid in movie_list:
                category_list = imdbid_category_dict[movieid]

                for category in category_list:
                    if category not in category_num_dict.keys():
                        category_num_dict[category] = 1
                    else:
                        category_num_dict[category] += 1
            director_category_dict[directorid] = category_num_dict
        return director_category_dict


    def getDirectorSimilarity(self, director_imdbids_path):
        output_path = 'director_coefficient.json'
        director_coefficient_file = open(output_path, 'w')
        with open(director_imdbids_path) as director_imdbids_file:
            director_imdbids_dict = json.loads(director_imdbids_file.readline())

        # category with cosin similarity
        director_genres_dict = self.getCategoryNumDict(director_imdbids_dict, self.imdbid_genre_dict)

        director_vionelscene_dict = self.getCategoryNumDict(director_imdbids_dict, self.imdbid_vionelscene_dict)
        director_locationcity_dict = self.getCategoryNumDict(director_imdbids_dict, self.imdbid_locationcity_dict)
        director_locationcountry_dict = self.getCategoryNumDict(director_imdbids_dict, self.imdbid_locationcountry_dict)

        # category with added similarity
        director_actor_dict = self.getCategoryNumDict(director_imdbids_dict, self.imdbid_actor_dict)
        director_imdbkeyword_dict = self.getCategoryNumDict(director_imdbids_dict, self.imdbid_imdbkeyword_dict)
        director_wikikeyword_dict = self.getCategoryNumDict(director_imdbids_dict, self.imdbid_wikikeyword_dict)
        director_vioneltheme_dict = self.getCategoryNumDict(director_imdbids_dict, self.imdbid_vioneltheme_dict)
        #print director_vioneltheme_dict





        director_director_score_dict = {}
        for index, k1 in enumerate(director_imdbids_dict):
            director_score_dict = {}
            for k2 in director_imdbids_dict:
                

                # score for consin similarity
                genre_score = self.__getCosSim(director_genres_dict[k1], director_genres_dict[k2])
                vionelscene_score = self.__getCosSim(director_vionelscene_dict[k1], director_vionelscene_dict[k2])
                locationcity_score = self.__getCosSim(director_locationcity_dict[k1], director_locationcity_dict[k2])
                locationcountry_score = self.__getCosSim(director_locationcountry_dict[k1], director_locationcountry_dict[k2])

                # score for added similarity
                actor_score = self.__getAddedSim(director_actor_dict[k1], director_actor_dict[k2], 0.1)
                imdbkeyword_score = self.__getAddedSim(director_imdbkeyword_dict[k1], director_imdbkeyword_dict[k2], 0.1)
                wikikeyword_score = self.__getAddedSim(director_wikikeyword_dict[k1], director_wikikeyword_dict[k2], 0.1)
                vioneltheme_score = self.__getAddedSim(director_vioneltheme_dict[k1], director_vioneltheme_dict[k2], 0.1)




                score = genre_score + vionelscene_score + locationcity_score + locationcountry_score + actor_score +imdbkeyword_score + wikikeyword_score + vioneltheme_score

                director_score_dict[k2] = score
                # print actor_score

            director_director_score_dict[k1] = director_score_dict
            print index, 'director processed'

            json.dump({k1: director_score_dict}, director_coefficient_file)
            director_coefficient_file.write('\n')
        
        
        director_coefficient_file.close

        print Counter(director_director_score_dict).most_common(20)

        




cf = CoefficientFeature()
cf.getDirectorSimilarity("director_imdbids.json")
