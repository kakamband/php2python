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
#// Feed API: WP_Feed_Cache_Transient class
#// 
#// @package WordPress
#// @subpackage Feed
#// @since 4.7.0
#// 
#// 
#// Core class used to implement feed cache transients.
#// 
#// @since 2.8.0
#//
class WP_Feed_Cache_Transient():
    name = Array()
    mod_name = Array()
    lifetime = 43200
    #// 
    #// Constructor.
    #// 
    #// @since 2.8.0
    #// @since 3.2.0 Updated to use a PHP5 constructor.
    #// 
    #// @param string $location  URL location (scheme is used to determine handler).
    #// @param string $filename  Unique identifier for cache object.
    #// @param string $extension 'spi' or 'spc'.
    #//
    def __init__(self, location=None, filename=None, extension=None):
        
        self.name = "feed_" + filename
        self.mod_name = "feed_mod_" + filename
        lifetime = self.lifetime
        #// 
        #// Filters the transient lifetime of the feed cache.
        #// 
        #// @since 2.8.0
        #// 
        #// @param int    $lifetime Cache duration in seconds. Default is 43200 seconds (12 hours).
        #// @param string $filename Unique identifier for the cache object.
        #//
        self.lifetime = apply_filters("wp_feed_cache_transient_lifetime", lifetime, filename)
    # end def __init__
    #// 
    #// Sets the transient.
    #// 
    #// @since 2.8.0
    #// 
    #// @param SimplePie $data Data to save.
    #// @return true Always true.
    #//
    def save(self, data=None):
        
        if type(data).__name__ == "SimplePie":
            data = data.data
        # end if
        set_transient(self.name, data, self.lifetime)
        set_transient(self.mod_name, time(), self.lifetime)
        return True
    # end def save
    #// 
    #// Gets the transient.
    #// 
    #// @since 2.8.0
    #// 
    #// @return mixed Transient value.
    #//
    def load(self):
        
        return get_transient(self.name)
    # end def load
    #// 
    #// Gets mod transient.
    #// 
    #// @since 2.8.0
    #// 
    #// @return mixed Transient value.
    #//
    def mtime(self):
        
        return get_transient(self.mod_name)
    # end def mtime
    #// 
    #// Sets mod transient.
    #// 
    #// @since 2.8.0
    #// 
    #// @return bool False if value was not set and true if value was set.
    #//
    def touch(self):
        
        return set_transient(self.mod_name, time(), self.lifetime)
    # end def touch
    #// 
    #// Deletes transients.
    #// 
    #// @since 2.8.0
    #// 
    #// @return true Always true.
    #//
    def unlink(self):
        
        delete_transient(self.name)
        delete_transient(self.mod_name)
        return True
    # end def unlink
# end class WP_Feed_Cache_Transient