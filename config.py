import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    THETVDB_API_KEY = os.environ.get('THETVDB_API_KEY')
    THETVDB_API_URL = os.environ.get('THETVDB_API_URL', default = 'https://api.themoviedb.org/4')
    TV_IN = os.path.join(basedir, 'tv_in')
    TV_OUT = os.path.join(basedir, 'tv_out')
    MOVIE_IN = os.path.join(basedir, 'movie_in')
    MOVIE_OUT = os.path.join(basedir, 'movie_out')
    MUSIC_IN = os.path.join(basedir, 'music_in')
    MUSIC_OUT = os.path.join(basedir, 'music_out')



# [group] Show - 01-02 [crc]
        '''^\[(?P<group>.+?)\][ ]?               # group name, captured for [#100]
        (?P<seriesname>.*?)[ ]?[-_][ ]?          # show name, padding, spaces?
        (?P<episodenumberstart>\d+)              # first episode number
        ([-_]\d+)*                               # optional repeating episodes
        [-_](?P<episodenumberend>\d+)            # last episode number
        (?=                                      # Optional group for crc value (non-capturing)
          .*                                     # padding
          \[(?P<crc>.+?)\]                       # CRC value
        )?                                       # End optional crc group
        [^\/]*$''',

        # [group] Show - 01 [crc]
        '''^\[(?P<group>.+?)\][ ]?               # group name, captured for [#100]
        (?P<seriesname>.*)                       # show name
        [ ]?[-_][ ]?                             # padding and seperator
        (?P<episodenumber>\d+)                   # episode number
        (?=                                      # Optional group for crc value (non-capturing)
          .*                                     # padding
          \[(?P<crc>.+?)\]                       # CRC value
        )?                                       # End optional crc group
        [^\/]*$''',

        # foo s01e23 s01e24 s01e25 *
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        [Ss](?P<seasonnumber>[0-9]+)             # s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberstart>[0-9]+)       # first e23
        ([\.\- ]+                                # separator
        [Ss](?P=seasonnumber)                    # s01
        [\.\- ]?                                 # separator
        [Ee][0-9]+)*                             # e24 etc (middle groups)
        ([\.\- ]+                                # separator
        [Ss](?P=seasonnumber)                    # last s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberend>[0-9]+))        # final episode number
        [^\/]*$''',

        # foo.s01e23e24*
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        [Ss](?P<seasonnumber>[0-9]+)             # s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberstart>[0-9]+)       # first e23
        ([\.\- ]?                                # separator
        [Ee][0-9]+)*                             # e24e25 etc
        [\.\- ]?[Ee](?P<episodenumberend>[0-9]+) # final episode num
        [^\/]*$''',

        # foo.1x23 1x24 1x25
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<seasonnumber>[0-9]+)                 # first season number (1)
        [xX](?P<episodenumberstart>[0-9]+)       # first episode (x23)
        ([ \._\-]+                               # separator
        (?P=seasonnumber)                        # more season numbers (1)
        [xX][0-9]+)*                             # more episode numbers (x24)
        ([ \._\-]+                               # separator
        (?P=seasonnumber)                        # last season number (1)
        [xX](?P<episodenumberend>[0-9]+))        # last episode number (x25)
        [^\/]*$''',

        # foo.1x23x24*
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<seasonnumber>[0-9]+)                 # 1
        [xX](?P<episodenumberstart>[0-9]+)       # first x23
        ([xX][0-9]+)*                            # x24x25 etc
        [xX](?P<episodenumberend>[0-9]+)         # final episode num
        [^\/]*$''',

        # foo.s01e23-24*
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        [Ss](?P<seasonnumber>[0-9]+)             # s01
        [\.\- ]?                                 # separator
        [Ee](?P<episodenumberstart>[0-9]+)       # first e23
        (                                        # -24 etc
             [\-]
             [Ee]?[0-9]+
        )*
             [\-]                                # separator
             [Ee]?(?P<episodenumberend>[0-9]+)   # final episode num
        [\.\- ]                                  # must have a separator (prevents s01e01-720p from being 720 episodes)
        [^\/]*$''',

        # foo.1x23-24*
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<seasonnumber>[0-9]+)                 # 1
        [xX](?P<episodenumberstart>[0-9]+)       # first x23
        (                                        # -24 etc
             [\-+][0-9]+
        )*
             [\-+]                               # separator
             (?P<episodenumberend>[0-9]+)        # final episode num
        ([\.\-+ ].*                              # must have a separator (prevents 1x01-720p from being 720 episodes)
        |
        $)''',

        # foo.[1x09-11]*
        '''^(?P<seriesname>.+?)[ \._\-]          # show name and padding
        \[                                       # [
            ?(?P<seasonnumber>[0-9]+)            # season
        [xX]                                     # x
            (?P<episodenumberstart>[0-9]+)       # episode
            ([\-+] [0-9]+)*
        [\-+]                                    # -
            (?P<episodenumberend>[0-9]+)         # episode
        \]                                       # \]
        [^\\/]*$''',

        # foo - [012]
        '''^((?P<seriesname>.+?)[ \._\-])?       # show name and padding
        \[                                       # [ not optional (or too ambigious)
        (?P<episodenumber>[0-9]+)                # episode
        \]                                       # ]
        [^\\/]*$''',
        # foo.s0101, foo.0201
        '''^(?P<seriesname>.+?)[ \._\-]
        [Ss](?P<seasonnumber>[0-9]{2})
        [\.\- ]?
        (?P<episodenumber>[0-9]{2})
        [^0-9]*$''',

        # foo.1x09*
        '''^((?P<seriesname>.+?)[ \._\-])?       # show name and padding
        \[?                                      # [ optional
        (?P<seasonnumber>[0-9]+)                 # season
        [xX]                                     # x
        (?P<episodenumber>[0-9]+)                # episode
        \]?                                      # ] optional
        [^\\/]*$''',

        # foo.s01.e01, foo.s01_e01, "foo.s01 - e01"
        '''^((?P<seriesname>.+?)[ \._\-])?
        \[?
        [Ss](?P<seasonnumber>[0-9]+)[ ]?[\._\- ]?[ ]?
        [Ee]?(?P<episodenumber>[0-9]+)
        \]?
        [^\\/]*$''',

        # foo.2010.01.02.etc
        '''
        ^((?P<seriesname>.+?)[ \._\-])?          # show name
        (?P<year>\d{4})                          # year
        [ \._\-]                                 # separator
        (?P<month>\d{2})                         # month
        [ \._\-]                                 # separator
        (?P<day>\d{2})                           # day
        [^\/]*$''',

        # foo - [01.09]
        '''^((?P<seriesname>.+?))                # show name
        [ \._\-]?                                # padding
        \[                                       # [
        (?P<seasonnumber>[0-9]+?)                # season
        [.]                                      # .
        (?P<episodenumber>[0-9]+?)               # episode
        \]                                       # ]
        [ \._\-]?                                # padding
        [^\\/]*$''',

        # Foo - S2 E 02 - etc
        '''^(?P<seriesname>.+?)[ ]?[ \._\-][ ]?
        [Ss](?P<seasonnumber>[0-9]+)[\.\- ]?
        [Ee]?[ ]?(?P<episodenumber>[0-9]+)
        [^\\/]*$''',

        # Show - Episode 9999 [S 12 - Ep 131] - etc
        '''
        (?P<seriesname>.+)                       # Showname
        [ ]-[ ]                                  # -
        [Ee]pisode[ ]\d+                         # Episode 1234 (ignored)
        [ ]
        \[                                       # [
        [sS][ ]?(?P<seasonnumber>\d+)            # s 12
        ([ ]|[ ]-[ ]|-)                          # space, or -
        ([eE]|[eE]p)[ ]?(?P<episodenumber>\d+)   # e or ep 12
        \]                                       # ]
        .*$                                      # rest of file
        ''',

        # show name 2 of 6 - blah
        '''^(?P<seriesname>.+?)                  # Show name
        [ \._\-]                                 # Padding
        (?P<episodenumber>[0-9]+)                # 2
        of                                       # of
        [ \._\-]?                                # Padding
        \d+                                      # 6
        ([\._ -]|$|[^\\/]*$)                     # More padding, then anything
        ''',

        # Show.Name.Part.1.and.Part.2
        '''^(?i)
        (?P<seriesname>.+?)                        # Show name
        [ \._\-]                                   # Padding
        (?:part|pt)?[\._ -]
        (?P<episodenumberstart>[0-9]+)             # Part 1
        (?:
          [ \._-](?:and|&|to)                        # and
          [ \._-](?:part|pt)?                        # Part 2
          [ \._-](?:[0-9]+))*                        # (middle group, optional, repeating)
        [ \._-](?:and|&|to)                        # and
        [ \._-]?(?:part|pt)?                       # Part 3
        [ \._-](?P<episodenumberend>[0-9]+)        # last episode number, save it
        [\._ -][^\\/]*$                            # More padding, then anything
        ''',

        # Show.Name.Part1
        '''^(?P<seriesname>.+?)                  # Show name\n
        [ \\._\\-]                               # Padding\n
        [Pp]art[ ](?P<episodenumber>[0-9]+)      # Part 1\n
        [\\._ -][^\\/]*$                         # More padding, then anything\n
        ''',

        # show name Season 01 Episode 20
        '''^(?P<seriesname>.+?)[ ]?               # Show name
        [Ss]eason[ ]?(?P<seasonnumber>[0-9]+)[ ]? # Season 1
        [Ee]pisode[ ]?(?P<episodenumber>[0-9]+)   # Episode 20
        [^\\/]*$''',                              # Anything

        # foo.103*
        '''^(?P<seriesname>.+)[ \._\-]
        (?P<seasonnumber>[0-9]{1})
        (?P<episodenumber>[0-9]{2})
        [\._ -][^\\/]*$''',

        # foo.0103*
        '''^(?P<seriesname>.+)[ \._\-]
        (?P<seasonnumber>[0-9]{2})
        (?P<episodenumber>[0-9]{2,3})
        [\._ -][^\\/]*$''',

        # show.name.e123.abc
        '''^(?P<seriesname>.+?)                  # Show name
        [ \._\-]                                 # Padding
        [Ee](?P<episodenumber>[0-9]+)            # E123
        [\._ -][^\\/]*$                          # More padding, then anything
        ''',