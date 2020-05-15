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
#// Server-side file upload handler from wp-plupload or other asynchronous upload methods.
#// 
#// @package WordPress
#// @subpackage Administration
#//
if (php_isset(lambda : PHP_REQUEST["action"])) and "upload-attachment" == PHP_REQUEST["action"]:
    php_define("DOING_AJAX", True)
# end if
if (not php_defined("WP_ADMIN")):
    php_define("WP_ADMIN", True)
# end if
if php_defined("ABSPATH"):
    php_include_file(ABSPATH + "wp-load.php", once=True)
else:
    php_include_file(php_dirname(__DIR__) + "/wp-load.php", once=True)
# end if
php_include_file(ABSPATH + "wp-admin/admin.php", once=True)
php_header("Content-Type: text/plain; charset=" + get_option("blog_charset"))
if (php_isset(lambda : PHP_REQUEST["action"])) and "upload-attachment" == PHP_REQUEST["action"]:
    php_include_file(ABSPATH + "wp-admin/includes/ajax-actions.php", once=False)
    send_nosniff_header()
    nocache_headers()
    wp_ajax_upload_attachment()
    php_print("0")
    php_exit()
# end if
if (not current_user_can("upload_files")):
    wp_die(__("Sorry, you are not allowed to upload files."))
# end if
#// Just fetch the detail form for that attachment.
if (php_isset(lambda : PHP_REQUEST["attachment_id"])) and php_intval(PHP_REQUEST["attachment_id"]) and PHP_REQUEST["fetch"]:
    id = php_intval(PHP_REQUEST["attachment_id"])
    post = get_post(id)
    if "attachment" != post.post_type:
        wp_die(__("Invalid post type."))
    # end if
    if (not current_user_can("edit_post", id)):
        wp_die(__("Sorry, you are not allowed to edit this item."))
    # end if
    for case in Switch(PHP_REQUEST["fetch"]):
        if case(3):
            thumb_url = wp_get_attachment_image_src(id, "thumbnail", True)
            if thumb_url:
                php_print("<img class=\"pinkynail\" src=\"" + esc_url(thumb_url[0]) + "\" alt=\"\" />")
            # end if
            php_print("<a class=\"edit-attachment\" href=\"" + esc_url(get_edit_post_link(id)) + "\" target=\"_blank\">" + _x("Edit", "media item") + "</a>")
            #// Title shouldn't ever be empty, but use filename just in case.
            file = get_attached_file(post.ID)
            title = post.post_title if post.post_title else wp_basename(file)
            php_print("<div class=\"filename new\"><span class=\"title\">" + esc_html(wp_html_excerpt(title, 60, "&hellip;")) + "</span></div>")
            break
        # end if
        if case(2):
            add_filter("attachment_fields_to_edit", "media_single_attachment_fields_to_edit", 10, 2)
            php_print(get_media_item(id, Array({"send": False, "delete": True})))
            break
        # end if
        if case():
            add_filter("attachment_fields_to_edit", "media_post_single_attachment_fields_to_edit", 10, 2)
            php_print(get_media_item(id))
            break
        # end if
    # end for
    php_exit(0)
# end if
check_admin_referer("media-form")
post_id = 0
if (php_isset(lambda : PHP_REQUEST["post_id"])):
    post_id = absint(PHP_REQUEST["post_id"])
    if (not get_post(post_id)) or (not current_user_can("edit_post", post_id)):
        post_id = 0
    # end if
# end if
id = media_handle_upload("async-upload", post_id)
if is_wp_error(id):
    printf("<div class=\"error-div error\">%s <strong>%s</strong><br />%s</div>", php_sprintf("<button type=\"button\" class=\"dismiss button-link\" onclick=\"jQuery(this).parents('div.media-item').slideUp(200, function(){jQuery(this).remove();});\">%s</button>", __("Dismiss")), php_sprintf(__("&#8220;%s&#8221; has failed to upload."), esc_html(PHP_FILES["async-upload"]["name"])), esc_html(id.get_error_message()))
    php_exit(0)
# end if
if PHP_REQUEST["short"]:
    #// Short form response - attachment ID only.
    php_print(id)
else:
    #// Long form response - big chunk of HTML.
    type = PHP_REQUEST["type"]
    #// 
    #// Filters the returned ID of an uploaded attachment.
    #// 
    #// The dynamic portion of the hook name, `$type`, refers to the attachment type,
    #// such as 'image', 'audio', 'video', 'file', etc.
    #// 
    #// @since 2.5.0
    #// 
    #// @param int $id Uploaded attachment ID.
    #//
    php_print(apply_filters(str("async_upload_") + str(type), id))
# end if