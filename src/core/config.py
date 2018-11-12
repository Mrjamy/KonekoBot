import optparse

owner_id = 180640710217826304
dev_ids = [owner_id]


def get_args():
    parser = optparse.OptionParser()

    parser.add_option("-t", "--token", dest="token", default="TOKEN")
    parser.add_option("-p", "--pm-help", dest="pm_help", default=False)
    parser.add_option("-c", "--command-prefix", dest="command_prefix", default="/")

    (options, args) = parser.parse_args()
    return options
