
from structure import Zone, Link
import sys


def extract_info(filepath: str):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            Zones = []
            num = 0
            Links = []
            for line in file:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                part = line.split(":")
                type = part[0].strip()
                if type == "nb_drones":
                    num = int(part[1].strip())
                    continue
                elif type == "link":
                    corredores = part[1].strip()
                    corredores = corredores.split()
                    corredor0 = corredores[0]
                    corredor1 = corredores[1]
                    Links.append(Link(corredor0, corredor1))
                    continue
                else:
                    if "[" in part[1]:
                        data = part[1].split("[")
                        mandatory = data[0].strip()
                        metadata = data[1].strip()
                        metadata = metadata.rstrip("]")
                        coor = mandatory.split()
                    else:
                        data = part[1].strip()
                        coor = data.split()

                    name = part[0].strip()
                    x = int(coor[0])
                    y = int(coor[1])

                    Zones.append(Zone(name, x, y, "normal", None, 1))

        dict_Zones = {
            "Zones": Zones,
            "Links": Links,
            "nb_drones": num
        }

        return dict_Zones

    except Exception as e:
        print(e)


def parse_info(dict_Zones):
    Zones = dict_Zones["Zones"]
    Links = dict_Zones["Links"]
    nb_drones = dict_Zones["nb_drones"]
    valid_zone_names = {zone.name for zone in Zones}
    seen_coordinates = set()
    if nb_drones <= 0:
        raise ValueError("Number of Drones are Invalid")
        exit(1)

    for zone in Zones:
        if zone.x is in seen_coordinates and zone.y is in 

    for link in Links:
        if (link.zone1 not in valid_zone_names or
                link.zone2 not in valid_zone_names):
            raise ValueError("Invalid zone in links")


if __name__ == "__main__":
    print(parse_info(extract_info(sys.argv[1])))
