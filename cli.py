# $ git log -n 2 v3.12.6..v3.12.7 -- Lib/argparse.py
# commit cbea45ad74779c0ffe760bab7f9d5ce149302495
# Author: Miss Islington (bot) <31488909+miss-islington@users.noreply.github.com>
# Date:   Sun Sep 29 11:18:06 2024 +0200

#     [3.12] gh-58573: Fix conflicts between abbreviated long options in the parent parser and subparsers in argparse (GH-124631) (GH-124759)
    
#     Check for ambiguous options if the option is consumed, not when it is
#     parsed.
#     (cherry picked from commit 3f27153e077d7e9448e2f081275931968b40cc74)
    
#     Co-authored-by: Serhiy Storchaka <storchaka@gmail.com>

# commit 5464c8aa9856a65f576f536532ee56310397e109
# Author: Miss Islington (bot) <31488909+miss-islington@users.noreply.github.com>
# Date:   Sun Sep 29 10:40:00 2024 +0200

#     [3.12] gh-116850: Fix argparse for namespaces with not directly writable dict (GH-124667) (GH-124758)
    
#     It now always uses setattr() instead of setting the dict item to modify
#     the namespace. This allows to use a class as a namespace.
#     (cherry picked from commit 95e92ef6c74e973ea13d15180190d0fa2af82fbf)
    
#     Co-authored-by: Serhiy Storchaka <storchaka@gmail.com>


# issue from https://github.com/python/cpython/pull/124631

# fail v3.12.7  https://github.com/python/cpython/commit/cbea45ad74779c0ffe760bab7f9d5ce149302495
argparse = __import__("argparse_cbea45a")
# fail 3.13 (not yet released) https://github.com/python/cpython/commit/6925e5b5c778d0c7deab58c62545b69b4a3d3844
# argparse = __import__("argparse_6925e5b") 


# ok v3.12.7_prev https://github.com/python/cpython/commit/5464c8aa9856a65f576f536532ee56310397e109
#argparse = __import__("argparse_5464c8a")

# ok v3.13.0 
# argparse = __import__("argparse_v3130") 

# fail main 
# argparse = __import__("argparse_main") 

# python (3.12.7 fail, everything else works)
#import argparse

parser = argparse.ArgumentParser()
parser.add_argument("args", nargs=-1, help="extra arguments")
parsed_args, extra = parser.parse_known_args()
print(f":args {parsed_args} :extra {extra}")

