import csv
import json
import time
import tweepy
import unicodedata

# You must use Python 2.7.x

# 1 point
def loadKeys(key_file):
    # FTODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>

    # Load keys here and replace the empty strings in the return statement with those keys
    data = json.load(open(key_file))
    return data['api_key'],data['api_secret'],data['token'],data['token_secret']

# 4 points
def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    # Add code here to populate primary_friends
    print "primary_friends:"
    user = api.get_user(root_user)
    friends = user.friends()
    for i in range( min(no_of_friends,user.friends_count) ):
        friend = toAscii(friends[i].screen_name)
        print friend
        primary_friends.append( (root_user, friend) )

    # raw_input("\ndebug\n")
    # print primary_friends
    # raw_input("\ndebug\n")

    return primary_friends

# 4 points
def getNextLevelFriends(api, users_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each user in users_list
    # rtype: list containing entries in the form of a tuple (user, friend)
    next_level_friends = []
    # Add code here to populate next_level_friends
    print "\nnext_level_friends:"
    for link in users_list:
        name = link[1]
        user = api.get_user(name)
        print name
        friends = user.friends()
        for i in range( min(no_of_friends,user.friends_count) ):
            friend = toAscii(friends[i].screen_name)
            next_level_friends.append( (name, friend) )

    # raw_input("\ndebug\n")
    # print next_level_friends
    # raw_input("end")

    return next_level_friends

# 4 points
def getNextLevelFollowers(api, users_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each user in users_list
    # rtype: list containing entries in the form of a tuple (follower, user)
    next_level_followers = []
    # Add code here to populate next_level_followers
    print "\nnext_level_followers:"
    for link in users_list:
        name = link[1]
        print name
        user = api.get_user(name)
        followers = user.followers()
        for i in range( min(no_of_followers, user.followers_count) ):
            follower = toAscii(followers[i].screen_name)
            # print follower
            next_level_followers.append( (follower, name) )

    return next_level_followers

# 3 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    #        NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    #        Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the
    #        Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends.
    all_edges = []
    #Add code here to populate all_edges
    primary_friends = getPrimaryFriends(api, root_user, no_of_neighbours)
    next_level_friends = getNextLevelFriends(api, primary_friends, no_of_neighbours)
    next_level_followers = getNextLevelFollowers(api, primary_friends, no_of_neighbours)

    all_edges = primary_friends + next_level_friends + next_level_followers

    return all_edges


# 2 points
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    with open(output_file, 'w') as out:
        for link in data:
            out.write(link[0] + "," + link[1] + "\n")

def toAscii(uni):
    return unicodedata.normalize('NFKD', uni).encode('ascii','ignore') # change into ascii



"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)

    writeToFile(edges, OUTPUT_FILE_GRAPH)


if __name__ == '__main__':
    testSubmission()

