#!/usr/bin/env python3
"""
Entry point for dir_checker when run as a module with python -m dir_checker
"""

if __name__ == '__main__':
    import sys
    from dir_checker.main import main
    sys.exit(main())
