#!/usr/bin/env python3
# coding: utf-8
if '__PHP2PY_LOADED__' not in globals():
    import cgi
    import os
    import os.path
    import copy
    import sys
    from goto import with_goto
    with open(os.getenv('PHP2PY_COMPAT', 'php_compat.py')) as f:
        exec(compile(f.read(), '<string>', 'exec'))
    # end with
    globals()['__PHP2PY_LOADED__'] = True
# end if
php_print("<div class=\"akismet-box\">\n    ")
Akismet.view("title")
php_print(" ")
Akismet.view("setup")
php_print("""</div>
<br/>
<div class=\"akismet-box\">
""")
Akismet.view("enter")
php_print("</div>")