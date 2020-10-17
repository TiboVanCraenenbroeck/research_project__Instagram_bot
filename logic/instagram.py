# import the modules
from models.profile import Profile
import instagram_explore as ie
import json


import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)


class Instagram:
    def get_profile_data(username: str) -> Profile:
        # search user name
        result = ie.user(username)

        parsed_data = json.dumps(result, indent=4, sort_keys=True)
        test = json.loads(parsed_data)

        # displaying the data
        user_data = test[0]
        # print(user_data)

        profile = Profile(id=user_data["id"], full_name=user_data["full_name"], username=user_data["username"], biography=user_data["biography"], profile_pic_url=user_data["profile_pic_url"], amount_posts=user_data["edge_owner_to_timeline_media"]["count"], amount_followers=user_data["edge_followed_by"]["count"], amount_following=user_data["edge_follow"]["count"],
                          external_url=user_data["external_url"], connected_fb_page=user_data["connected_fb_page"], is_joined_recently=user_data["is_joined_recently"], is_private=user_data["is_private"], is_verified=user_data["is_verified"], is_business_account=user_data["is_business_account"], business_email=user_data["business_email"], business_category_name=user_data["business_category_name"], category_enum=user_data["category_enum"])
        return profile
