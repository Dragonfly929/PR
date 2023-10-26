import xml.etree.ElementTree as ET
from player import Player
import player_pb2 as pb
from player_pb2 import Class


class PlayerFactory:
    def to_json(self, players):
        '''
        This function should transform a list of Player objects into a list with dictionaries.
        '''
        player_list = []
        for player in players:
            player_dict = {
                "nickname": player.nickname,
                "email": player.email,
                "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"),
                "xp": player.xp,
                "class": player.cls
            }
            player_list.append(player_dict)
        return player_list

    def from_json(self, list_of_dict):
        '''
        This function should transform a list of dictionaries into a list with Player objects.
        '''
        players = []
        for player_dict in list_of_dict:
            players.append(Player(
                player_dict["nickname"],
                player_dict["email"],
                player_dict["date_of_birth"],
                player_dict["xp"],
                player_dict["class"]
            ))
        return players

    def from_xml(self, xml_string):
        players = []
        root = ET.fromstring(xml_string)
        for player_elem in root.findall('player'):
            player_data = {}
            for elem in player_elem:
                player_data[elem.tag] = elem.text
            player_class = player_data.get("class", "Unknown")
            date_of_birth_str = str(player_data["date_of_birth"])
            players.append(Player(
                player_data["nickname"],
                player_data["email"],
                date_of_birth_str,
                int(player_data["xp"]),
                player_class
            ))
        return players

    def to_xml(self, list_of_players):
        '''
        This function should transform a list with Player objects into an XML string.
        '''
        root = ET.Element('data')
        for player in list_of_players:
            player_elem = ET.SubElement(root, 'player')
            for key, value in player.__dict__.items():
                if key == "date_of_birth":
                    value = value.strftime("%Y-%m-%d")
                if key == "cls":
                    key = "class"
                ET.SubElement(player_elem, key).text = str(value)

        xml_string = ET.tostring(root, encoding="unicode")
        return xml_string

    def from_protobuf(self, binary):
        '''
        Transform a binary protobuf string into a list of Player objects.
        '''
        player_list = pb.PlayersList()
        player_list.ParseFromString(binary)

        result = [Player(
            player.nickname,
            player.email,
            player.date_of_birth,
            player.xp,
            Class.Name(player.cls)
        ) for player in player_list.player]

        return result

    def to_protobuf(self, list_of_players):
        '''
        Transform a list of Player objects into a binary protobuf string.
        '''
        serialized_players = pb.PlayersList()
        for player in list_of_players:
            serialized_player = serialized_players.player.add()
            serialized_player.nickname = player.nickname
            serialized_player.email = player.email
            serialized_player.date_of_birth = player.date_of_birth.strftime("%Y-%m-%d")
            serialized_player.xp = player.xp
            serialized_player.cls = Class.Value(player.cls)

        return serialized_players.SerializeToString()