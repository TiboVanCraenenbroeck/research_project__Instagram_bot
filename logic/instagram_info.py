# import the modules
from time import sleep
from typing import List
import instagram_explore as ie
from instagramy import InstagramUser, InstagramHashTag
import json
import logging
from datetime import datetime
import sys
import os
import time
import numpy as np

from selenium.webdriver.common.keys import Keys


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)

from logic.browser import Browser
from models.location import Location
from models.post import Post
from models.profile import Profile

class InstagramInfo:
    def get_profile(username: str) -> Profile:
        try:
            profile = InstagramInfo.get_profile_data(username)
            profile.posts = InstagramInfo.get_users_posts(username)
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
                edge_media_to_caption_in: str = ""
                if len(post_data["edge_media_to_caption"]["edges"]) > 0:
                    edge_media_to_caption_in = post_data["edge_media_to_caption"]["edges"][0]["node"]["text"]

                post = Post(id=post_data["id"], shortcode=post_data["shortcode"], url=user_posts_iu[i]["url"], likes=user_posts_iu[i]["likes"], comments=user_posts_iu[i]["comment"], caption=user_posts_iu[i]
                            ["caption"], edge_media_to_caption=edge_media_to_caption_in, is_video=user_posts_iu[i]["is_video"], time_stamp=user_posts_iu[i]["timestamp"])

                if user_posts_iu[i]["location"] is not None:
                    try:
                        post_more_information = ie.media(post.shortcode).data
                        address_json = json.dumps(
                            post_more_information["location"]["address_json"])
                        location = Location(id=post_more_information["location"]["id"], has_public_page=post_more_information["location"]["has_public_page"],
                                            name=post_more_information["location"]["name"], slug=post_more_information["location"]["slug"], address_json=address_json)
                        post.location = location
                    except Exception as e:
                        logging.warning(
                            f"Could not get location from {username} - {e}")
                user_posts.append(post)
            return user_posts
        except Exception as e:
            logging.error(e)
            raise e

    def get_posts_from_hashtag(hashtag: str) -> List[Profile]:
        try:
            posts_tag_in = InstagramHashTag(hashtag)
            posts_tag = posts_tag_in.tag_data["edge_hashtag_to_media"]["edges"]
            list_posts: List[Profile] = []
            for post_tag in posts_tag:
                try:
                    post_tag = post_tag["node"]
                    id: int = post_tag["id"]
                    shortcode: str = post_tag["shortcode"]
                    url: str = f"https://instagram.com/p/{shortcode}"
                    likes: int = post_tag["edge_liked_by"]["count"]
                    comments: int = post_tag["edge_media_to_comment"]["count"]
                    caption: str = post_tag["accessibility_caption"]

                    edge_media_to_caption: str = ""
                    if len(post_tag["edge_media_to_caption"]["edges"]) > 0:
                        edge_media_to_caption = post_tag["edge_media_to_caption"]["edges"][0]["node"]["text"]
                    is_video: bool = post_tag["is_video"]
                    time_stamp: datetime = post_tag["taken_at_timestamp"]
                    found_by_tag: str = posts_tag_in.tagname

                    post_more_information = ie.media(shortcode).data

                    post: Post = Post(id=id, shortcode=shortcode, url=url, likes=likes, comments=comments, caption=caption,
                                      edge_media_to_caption=edge_media_to_caption, is_video=is_video, time_stamp=time_stamp, found_by_tag=found_by_tag)

                    if post_more_information["location"] is not None:
                        address_json = json.dumps(
                            post_more_information["location"]["address_json"])
                        location = Location(id=post_more_information["location"]["id"], has_public_page=post_more_information["location"]["has_public_page"],
                                            name=post_more_information["location"]["name"], slug=post_more_information["location"]["slug"], address_json=address_json)
                        post.location = location

                    # Get userinfo
                    username: str = post_more_information["owner"]["username"]
                    userinfo: Profile = InstagramInfo.get_profile_data(
                        username)
                    userinfo.posts.append(post)
                    list_posts.append(userinfo)
                except Exception as e:
                    logging.warning(
                        f"Could not get location from {post_tag} - {e}")
            return list_posts
        except Exception as e:
            logging.error(e)
            raise e

        except Exception as e:
            logging.error(e)
            raise e

    def get_likers_by_post(post_shortcode: str) -> List[str]:
        driver = Browser(0)
        driver.webdriver.get(f'https://www.instagram.com/p/{post_shortcode}/')
        sleep(np.random.uniform(1, 3))
        userid_element = driver.webdriver.find_elements_by_xpath(
            '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button')[0].click()
        time.sleep(2)

        users = []

        height_xpath: str = "/html/body/div[4]/div/div/div[2]/div/div"
        height = driver.webdriver.find_element_by_xpath(
            height_xpath).value_of_css_property("padding-top")
        sleep(np.random.uniform(1, 3))
        match = False
        while match == False:
            lastHeight = height

            # step 1
            elements = driver.webdriver.find_elements_by_xpath(
                "//*[@id]/div/span/a")

            sleep(np.random.uniform(1, 3))

            # step 2
            for element in elements:
                if element.get_attribute('title') not in users:
                    users.append(element.get_attribute('title'))

            # step 3
            driver.webdriver.execute_script(
                "return arguments[0].scrollIntoView();", elements[-1])
            sleep(np.random.uniform(1, 3))

            # step 4
            height = driver.webdriver.find_element_by_xpath(
                height_xpath).value_of_css_property("padding-top")
            sleep(np.random.uniform(1, 3))
            if lastHeight == height:
                match = True
        driver.close()
        return users
