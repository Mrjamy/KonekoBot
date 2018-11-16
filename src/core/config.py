import optparse


class Settings:
    __slots__ = ('token', 'pm_help', 'prefix', '_dry_run', 'owner_id', 'dev_ids')

    def __init__(self):
        parser = optparse.OptionParser()

        parser.add_option("-t", "--token", dest="token", default="TOKEN")
        parser.add_option("-p", "--pm-help", dest="pm_help", default=False)
        parser.add_option("-c", "--command-prefix", dest="command_prefix", default="/")
        parser.add_option("-d", "--dry-run", dest="boot_only", default=False)

        (options, args) = parser.parse_args()

        self.token = options.token
        self.pm_help = options.pm_help
        self.prefix = options.command_prefix
        self._dry_run = options.boot_only
        self.owner_id = 180640710217826304
        self.dev_ids = [self.owner_id]

    @property
    def login_credentials(self):
        return self.token
