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
#// 
#// Upgrader API: Bulk_Plugin_Upgrader_Skin class
#// 
#// @package WordPress
#// @subpackage Upgrader
#// @since 4.6.0
#// 
#// 
#// Bulk Theme Upgrader Skin for WordPress Theme Upgrades.
#// 
#// @since 3.0.0
#// @since 4.6.0 Moved to its own file from wp-admin/includes/class-wp-upgrader-skins.php.
#// 
#// @see Bulk_Upgrader_Skin
#//
class Bulk_Theme_Upgrader_Skin(Bulk_Upgrader_Skin):
    theme_info = Array()
    #// Theme_Upgrader::bulk_upgrade() will fill this in.
    def add_strings(self):
        
        super().add_strings()
        #// translators: 1: Theme name, 2: Number of the theme, 3: Total number of themes being updated.
        self.upgrader.strings["skin_before_update_header"] = __("Updating Theme %1$s (%2$d/%3$d)")
    # end def add_strings
    #// 
    #// @param string $title
    #//
    def before(self, title=""):
        
        super().before(self.theme_info.display("Name"))
    # end def before
    #// 
    #// @param string $title
    #//
    def after(self, title=""):
        
        super().after(self.theme_info.display("Name"))
        self.decrement_update_count("theme")
    # end def after
    #// 
    #//
    def bulk_footer(self):
        
        super().bulk_footer()
        update_actions = Array({"themes_page": php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("themes.php"), __("Return to Themes page")), "updates_page": php_sprintf("<a href=\"%s\" target=\"_parent\">%s</a>", self_admin_url("update-core.php"), __("Return to WordPress Updates page"))})
        if (not current_user_can("switch_themes")) and (not current_user_can("edit_theme_options")):
            update_actions["themes_page"] = None
        # end if
        #// 
        #// Filters the list of action links available following bulk theme updates.
        #// 
        #// @since 3.0.0
        #// 
        #// @param string[] $update_actions Array of theme action links.
        #// @param WP_Theme $theme_info     Theme object for the last-updated theme.
        #//
        update_actions = apply_filters("update_bulk_theme_complete_actions", update_actions, self.theme_info)
        if (not php_empty(lambda : update_actions)):
            self.feedback(php_implode(" | ", update_actions))
        # end if
    # end def bulk_footer
# end class Bulk_Theme_Upgrader_Skin