"""
py-voobly - Python wrapper for Voobly developer kit
Copyright (C) 2011  Ofir Tadmor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
   
import requests 
import urllib
from functools import partial

class InvalidActionParameter(Exception): pass
class InvalidRequest(Exception): pass
class InvalidResult(Exception): pass
class VooblyNotInitiated(Exception): pass
class InvalidVooblyKey(Exception): pass


VOOBLY_API_PATH = r"http://www.voobly.com/api"
MAX_LADDER_LIMIT = 40

class Voobly(object):
    """
    Voobly - a python wrapper for voobly developer api
    Voobly is a community driven which allows you to play old direct 
    play games (like age of empires). Voobly replaces the ZONE service provided by 
    Microsoft, which is not longer available.
    
    The key is available here:
    http://www.voobly.com/pages/view/146/Developer-Membership-Types
    
    Usage:
    
    >>> voobly = Voobly(voobly_developer_api_key) # 32 bytes long key
    >>> voobly_obj.init()
    >>> voobly.find_user('some_user')
    [{'uid': '12345', 'name': 'some_user'}]
    >>> voobly.get_user(12345)
    [{'bmonth': '0', 'display_name': 'some_user', 'uid': '12345', 'name': 'some_user', 'level': '0', 'bday': '0', 'byear': '0', 'imagesmall': '/res/user_img_large.png','sex': '0', 'last_login': '0123456789', 'tid': '', 'nationid': 'il', 'nation':'Israel', 'imagelarge': '/res/user_img_small.png', 'account_created': '0123456789'}]
    >>> voobly.get_ladder(20)
    [{'streak': '0', 'rating': '3359', 'display_name': 'some_user1', 'uid': '12345', 'wins': '682', 'losses': '316', 'rank': '1'}, 
     {'streak': '0', 'rating': '3206', 'display_name': 'some_user2', 'uid': '54321', 'wins': '351', 'losses': '151', 'rank': '2'}, 
     {'streak': '0', 'rating': '3205', 'display_name': 'some_user3', 'uid': '111111', 'wins': '351', 'losses': '152', 'rank': '3'}, 
     ...
     ...
    ]
    >>> voobly.get_ladder(20, start = 1, limit = 2)
    [{'streak': '0', 'rating': '3206', 'display_name': 'some_user2', 'uid': '54321', 'wins': '351', 'losses': '151', 'rank': '2'}, 
     {'streak': '0', 'rating': '3205', 'display_name': 'some_user3', 'uid': '111111', 'wins': '351', 'losses': '152', 'rank': '3'}, 
    ]
    >>> voobly.get_ladder(20, uidlist = [54321, 111111])
    [{'streak': '0', 'rating': '3206', 'display_name': 'some_user2', 'uid': '54321', 'wins': '351', 'losses': '151', 'rank': '2'}, 
     {'streak': '0', 'rating': '3205', 'display_name': 'some_user3', 'uid': '111111', 'wins': '351', 'losses': '152', 'rank': '3'}, 
    ]
    >>> voobly.get_ladder(20, uidst = [111111])
    [{'streak': '0', 'rating': '3205', 'display_name': 'some_user3', 'uid': '111111', 'wins': '351', 'losses': '152', 'rank': '3'}, 
    ]
    >>> voobly.find_users(['some_user1', 'some_user2'])
    [{'name': 'some_user1', 'uid': '12345'},
     {'name': 'some_user2', 'uid': '54321'},
    ]
    >>> voobly.get_lobbies(13)
    [{'lobbyid': '64', 'ladders': ['21', '8', '14', '13'], 'max_players': '1000', 'name': 'Medieval Siege (RM)', 'players_online': '674'}, 
     {'lobbyid': '67', 'ladders': ['21', '8', '14', '13'], 'max_players': '350', 'name': 'Tours (RM)', 'players_online': '2'}, 
     ...
     ...
    ]
    
    """
    def __init__(self, key, voobly_api_path = VOOBLY_API_PATH):
        super(Voobly, self).__init__()
        self.session = requests.session()
        self._key = key
        self._voobly_api_path = voobly_api_path
        
        self.get_user = self._voobly_not_initiated
        self.get_ladder = self._voobly_not_initiated
        self.find_user = self._voobly_not_initiated
        self.find_users = self._voobly_not_initiated
        self.get_lobbies = self._voobly_not_initiated

    def _voobly_not_initiated(self, *args, **kargs):
        raise VooblyNotInitiated()
        
    def init(self):
        if not VooblyActionValidateKey().act(self._voobly_api_path, self._key):
            raise InvalidVooblyKey(self._key)
            
        self.get_user = partial(VooblyActionGetUserInformation().act, self._voobly_api_path, self._key)
        self.get_ladder = partial(VooblyActionGetLadderInformation().act, self._voobly_api_path, self._key)
        self.find_user = partial(VooblyActionFindUser().act, self._voobly_api_path, self._key)
        self.find_users = partial(VooblyActionFindUsers().act, self._voobly_api_path, self._key)
        self.get_lobbies = partial(VooblyActionGetLobbies().act, self._voobly_api_path, self._key)
        

class VooblyAction(object):

    def __init__(self, action_path, allowed_parameters):
        super(VooblyAction, self).__init__()
        self._action_path = action_path
        self._allowed_parameters = allowed_parameters
        
    def act(self, base_url, key, input, parameters):
        if any([p not in self._allowed_parameters for p in parameters]):
            raise InvalidActionParameter("Allowed parameters are %s, got %s" % (self._allowed_parameters, parameters))
        
        requested_url = "%s/%s%s?key=%s%s" % (base_url, self._action_path, input, key, "".join(["&%s=%s" % p for p in parameters.items()]))
        print(requested_url)
        results = requests.get(requested_url)
        #file_obj = urllib.URLopener().open(requested_url)
        #try:
        #    results = self._parse(file_obj.read())
        #finally:
        #    file_obj.close()
        
        return results.content.decode()
        
    def _parse(self, results):
        if '400 Bad Request' in results:
            raise InvalidRequest()

        result_lines = results.splitlines()
        if not result_lines:
            raise InvalidResult('no result data')
            
        header_line = result_lines[0].split(',')
        data_lines = result_lines[1:]
        return [dict(zip(header_line, line.split(","))) for line in data_lines]
        
class VooblyActionValidateKey(VooblyAction):
    def __init__(self):
        super(VooblyActionValidateKey, self).__init__("validate", [])
        
    def act(self, base_url, key):
        return super(VooblyActionValidateKey, self).act(base_url, key, '', {})
        
    def _parse(self, results):
        return 'valid-key' in results
        
        
        
class VooblyActionGetUserInformation(VooblyAction):
    def __init__(self):
        super(VooblyActionGetUserInformation, self).__init__("user", [])
    def act(self, base_url, key, user_id):
        return super(VooblyActionGetUserInformation, self).act(base_url, key, '/%d' % user_id, {})
        
class VooblyActionGetLadderInformation(VooblyAction):
    def __init__(self):
        super(VooblyActionGetLadderInformation, self).__init__("ladder", ["uid", "uidlist", "start", "limit"])
    def act(self, base_url, key, ladder_id, uid = None, uidlist = None, start = None, limit = None):
        if uidlist is not None and uid is not None:
            raise InvalidActionParameter('only one of uid or uidlist parameters should be suplied to ladder, not both.')
        parameters = {}
        if uidlist is not None:
            parameters["uidlist"] = ','.join([str(uid) for uid in uidlist])
        if uid is not None:
            parameters["uid"] = uid
        if start is not None:
            parameters["start"] = start
        if limit is not None:
            parameters["limit"] = limit
            if limit > MAX_LADDER_LIMIT:
                raise InvalidActionParameter('max limit to ladder is %d, but received %d.' % (MAX_LADDER_LIMIT, limit,))
            

        return super(VooblyActionGetLadderInformation, self).act(base_url, key, '/%d' % ladder_id, parameters)

class VooblyActionFindUser(VooblyAction):
    def __init__(self):
        super(VooblyActionFindUser, self).__init__("finduser", [])
    def act(self, base_url, key, user_name):
        return super(VooblyActionFindUser, self).act(base_url, key, '/%s' % user_name, {})

class VooblyActionFindUsers(VooblyAction):
    def __init__(self):
        super(VooblyActionFindUsers, self).__init__("findusers", [])
    def act(self, base_url, key, user_names):
        return super(VooblyActionFindUsers, self).act(base_url, key, '/%s' % ','.join(user_names), {})

class VooblyActionGetLobbies(VooblyAction):
    def __init__(self):
        super(VooblyActionGetLobbies, self).__init__("lobbies", [])
    def act(self, base_url, key, lobby_id):
        return super(VooblyActionGetLobbies, self).act(base_url, key, '/%d' % lobby_id, {})
    def _parse(self, results):
        lobbies = super(VooblyActionGetLobbies, self)._parse(results)
        
        for lobby in lobbies:
            lobby['ladders'] = [ladder for ladder in lobby['ladders'].split('|') if ladder]
            
        return lobbies

