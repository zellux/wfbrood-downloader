#!/usr/bin/env python

import urllib
import re
import sys
import optparse

HELP = """ %prog [-p] url1, url2, url3, ...

    Flash Video Snagger (FLVSnag)

    Tool for downloading files referenced in the source code of some
    video-displaying websites. Simply pass a website URL as the first
    argument and the HTML will be scanned for URLs to .flv files and
    they will be downloaded.

    Note that all given pages are scanned before the first video is
    downloaded.

    FIXME: Downloads may not occur in the order that they are found.

                                              - The Music Guy, 5/5/09
                                                musicguy@...
"""

def main():
    # Create the option parser and parse the options.
    parser = optparse.OptionParser(usage=HELP)
    parser.add_option(
        '-p', '--print',
         action = 'store_true',
         default = False,
         help =
            "Causes the URLs to be printed to stdout (one URL per line) "
            "without actually downloading them. Good for piping."
    )
    parser.add_option(
        '-d', '--dpg',
        action = 'store_true',
        default = False,
        help =
            "TODO: Converts each downloaded file to DPG if dpgconv.py is available "
            "from the PATH."
    )
    parser.add_option(
        '-w', '--wget',
        action = 'store_true',
        default = False,
        help =
            "TODO: Downloads each file using wget instead of using internal "
            "downloader. Only works if wget is available from the PATH."
    )
    ops,args = parser.parse_args()
    if not args:
        parser.print_usage()
        return

    # Create a pattern that matches embedded .flv file URLs.
    urlre = re.compile("http\:\/\/(?<!\?)[a-zA-Z0-9_ \.\/]*\.flv", re.I)

    # Download the given URLs and scan the files for video URLs.
    m = set()
    for u in args:
        # Try to download the pages.
        try:
            f = urllib.urlopen(u)
        except IOError:
            sys.exit('ERROR: Unable to open url "%s".'%u)
        s = f.read()
        f.close()

        # Add any located URLs to the set.
        m = m.union(urlre.findall(s))

        # Delete page to save space.
        del s

    # If the user did not specify to print video URLs, download the videos.
    ops.p = False
    if not ops.p:
        # Print a notice if no URLs are found.
        if not m:
            print "No URLs found."
            return

        # Create a pattern to match video filename
        fnre = re.compile("[a-zA-Z0-9_ \.]*\.flv", re.I)

        # Download each video
        for v in m:
            p = fnre.findall(v)[0]
            print 'Downloading "%s" to "%s"...'%(v,p)
            urllib.urlretrieve(v,p)
            print 'done.'

    # If the user said to print video URLs, just print, don't download.
    else:
        for v in m:
            print v


if __name__ == '__main__':
    main() 
