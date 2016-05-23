class Group(object):
    def __repr__(self, *args, **kwargs):
        return "Group {0} owns {1}".format(self.name, self.owns)

    def __init__(self, name, owns):
        self.name = name
        self.owns = owns


class Groups(dict):
    """
    Groups are described by a bipartite graph. With Group vs. Members. A member can be in multiple groups.
    A member can not be a group and a group can not be member of a different group.
    """
    @staticmethod
    def __verify_name(names):
        x = names[0]
        for name in names:
            assert name == x
        return x

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        groups = [group_id for group_id in data.index.get_level_values(level="Group ID").unique()]
        name = {group_id: Groups.__verify_name(data.xs(group_id, level="Group ID")["Group Name"]) for group_id in groups}
        owns = {group_id: list(data.xs(group_id, level="Group ID").index) for group_id in groups}
        self.__name = {group_id: Group(name=name[group_id], owns=owns[group_id]) for group_id in groups}

    def __getitem__(self, item):
        return self.__name[item]

    def items(self):
        return self.__name.items()

    def values(self):
        return self.__name.values()

    def keys(self):
        return self.__name.keys()

    def __iter__(self):
        return self.__name.__iter__()
