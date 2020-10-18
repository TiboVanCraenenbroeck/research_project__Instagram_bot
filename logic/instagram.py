# import the modules
from typing import List
import instagram_explore as ie
from instagramy import InstagramUser
import instagramy
import json
import logging

import sys
# sys.setrecursionlimit(10**6)
import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)

from models.profile import Profile
from models.post import Post

class Instagram:
    def get_profile(username: str) -> Profile:
        try:
            profile = Instagram.get_profile_data(username)
            profile.posts = Instagram.get_users_posts(username)
            return profile
        except Exception as e:
            logging.error(e)
            raise e

    def get_profile_data(username: str) -> Profile:
        try:
            user = InstagramUser(username)
            profile: Profile = Profile(id=user.user_data["id"], username=user.username, full_name=user.fullname, biography=user.biography, profile_pic_url=user.profile_picture_url, number_posts=user.number_of_posts, number_followers=user.number_of_followers, connected_fb_page=user.user_data["connected_fb_page"], website_url=user.website,
                                       is_joined_recently=user.other_info["is_joined_recently"], is_private=user.is_private, is_verified=user.is_verified, is_business_account=user.other_info["is_business_account"], business_email=user.user_data["business_email"], business_category_name=user.user_data["business_category_name"], category_enum=user.user_data["category_enum"])
            return profile
        except Exception as e:
            logging.error(e)
            raise e

    def get_users_posts(username: str) -> List[Post]:
        try:
            user = InstagramUser(username)
            user_posts: List[Post] = []
            user_posts_data = user.user_data["edge_owner_to_timeline_media"]["edges"]
            user_posts_iu = user.posts
            for i, post in enumerate(user_posts_data):
                post_data = post["node"]
                try:
                    edge_media_to_caption_in = post_data["edge_media_to_caption"]["edges"][0]["node"]["text"]
                except:
                    edge_media_to_caption_in = ""
                post = Post(id=post_data["id"], shortcode=post_data["shortcode"], url=user_posts_iu[i]["url"], likes=user_posts_iu[i]["likes"], comments=user_posts_iu[i]["comment"], caption=user_posts_iu[i]
                            ["caption"], edge_media_to_caption=edge_media_to_caption_in, is_video=user_posts_iu[i]["is_video"], location=user_posts_iu[i]["location"], time_stamp=user_posts_iu[i]["timestamp"])
                user_posts.append(post)
            return user_posts
        except Exception as e:
            logging.error(e)
            raise e

    """ def get_profile_data(username: str) -> Profile:
        try:
            result = ie.user(username)

            parsed_data = json.dumps(result, indent=4, sort_keys=True)
            json_data = json.loads(parsed_data)

            user_data = json_data[0]

            profile = Profile(id=user_data["id"], full_name=user_data["full_name"], username=user_data["username"], biography=user_data["biography"], profile_pic_url=user_data["profile_pic_url"], amount_posts=user_data["edge_owner_to_timeline_media"]["count"], amount_followers=user_data["edge_followed_by"]["count"], amount_following=user_data["edge_follow"]["count"],
                              external_url=user_data["external_url"], connected_fb_page=user_data["connected_fb_page"], is_joined_recently=user_data["is_joined_recently"], is_private=user_data["is_private"], is_verified=user_data["is_verified"], is_business_account=user_data["is_business_account"], business_email=user_data["business_email"], business_category_name=user_data["business_category_name"], category_enum=user_data["category_enum"])
            return profile
        except Exception as e:
            logging.error(e)
            raise e

    def get_user_posts(user: Profile) -> Profile:
        try:
            result = ie.user_images(user.username)
            ie.
            parsed_data = json.dumps(result, indent=4, sort_keys=True)
            json_data = json.loads(parsed_data)
            print(json_data)
        except Exception as e:
            logging.error(e)
            raise e """
