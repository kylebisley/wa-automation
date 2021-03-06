from argparse import ArgumentParser, FileType

parser = ArgumentParser(
        description = 'Client for interacting with the Wild Apricot admin API.')
parser.add_argument(
        '-k',
        '--key',
        help = "Path to file containing the API key, generated in Settings -> Security -> Authorized applications",
        metavar = "<api-key>",
        type = FileType())
parser.add_argument(
        '-a',
        '--account',
        help = 'Wild Apricot account ID. Optional as it can be automatically detected based on your API key.',
        metavar = '<id>',
        type = int)
parser.add_argument(
        '-c',
        '--config',
        dest = 'config_file',
        help = 'Path to configuration file',
        metavar = '<file>')
parser.add_argument(
        '-o',
        action = 'append',
        dest = 'operations',
        help = 'The operation to perform. Can be specified multiple times.',
        metavar = ('<operation>', '<argument>'),
        nargs = '+',
        required = True)

#TODO Add argument parsing for Discourse API

args = parser.parse_args()

if args.key is not None:
    key = args.key.read()
