import os

def scrape_alliance_members(html_file_path):
    """
Get a list of alliance members from a webpage of the format https://ts6.x1.asia.travian.com/alliance/*/profile/members (where * points to alliance ID).

I should really be using a DOM parser for this, but oh well.

Parameter(s):
- html_file_path: String path to HTML capture file of webpage

Returns: List of alliance members
    """

    assert os.path.isfile(html_file_path)

    members_set = set()

    with open(html_file_path, "r") as f:
        for line in f.readlines():
            if "<a href=\"/profile/" in line:
                st = line.index("<a href=\"/profile/")
                st = line.index(">", st) + 1
                end = line.index("<", st)
                members_set.add(line[st:end])

    return list(members_set)