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
#// The custom background script.
#// 
#// @package WordPress
#// @subpackage Administration
#// 
#// 
#// The custom background class.
#// 
#// @since 3.0.0
#//
class Custom_Background():
    admin_header_callback = Array()
    admin_image_div_callback = Array()
    updated = Array()
    #// 
    #// Constructor - Register administration header callback.
    #// 
    #// @since 3.0.0
    #// @param callable $admin_header_callback
    #// @param callable $admin_image_div_callback Optional custom image div output callback.
    #//
    def __init__(self, admin_header_callback="", admin_image_div_callback=""):
        
        self.admin_header_callback = admin_header_callback
        self.admin_image_div_callback = admin_image_div_callback
        add_action("admin_menu", Array(self, "init"))
        add_action("wp_ajax_custom-background-add", Array(self, "ajax_background_add"))
        #// Unused since 3.5.0.
        add_action("wp_ajax_set-background-image", Array(self, "wp_set_background_image"))
    # end def __init__
    #// 
    #// Set up the hooks for the Custom Background admin page.
    #// 
    #// @since 3.0.0
    #//
    def init(self):
        
        page = add_theme_page(__("Background"), __("Background"), "edit_theme_options", "custom-background", Array(self, "admin_page"))
        if (not page):
            return
        # end if
        add_action(str("load-") + str(page), Array(self, "admin_load"))
        add_action(str("load-") + str(page), Array(self, "take_action"), 49)
        add_action(str("load-") + str(page), Array(self, "handle_upload"), 49)
        if self.admin_header_callback:
            add_action(str("admin_head-") + str(page), self.admin_header_callback, 51)
        # end if
    # end def init
    #// 
    #// Set up the enqueue for the CSS & JavaScript files.
    #// 
    #// @since 3.0.0
    #//
    def admin_load(self):
        
        get_current_screen().add_help_tab(Array({"id": "overview", "title": __("Overview"), "content": "<p>" + __("You can customize the look of your site without touching any of your theme&#8217;s code by using a custom background. Your background can be an image or a color.") + "</p>" + "<p>" + __("To use a background image, simply upload it or choose an image that has already been uploaded to your Media Library by clicking the &#8220;Choose Image&#8221; button. You can display a single instance of your image, or tile it to fill the screen. You can have your background fixed in place, so your site content moves on top of it, or you can have it scroll with your site.") + "</p>" + "<p>" + __("You can also choose a background color by clicking the Select Color button and either typing in a legitimate HTML hex value, e.g. &#8220;#ff0000&#8221; for red, or by choosing a color using the color picker.") + "</p>" + "<p>" + __("Don&#8217;t forget to click on the Save Changes button when you are finished.") + "</p>"}))
        get_current_screen().set_help_sidebar("<p><strong>" + __("For more information:") + "</strong></p>" + "<p>" + __("<a href=\"https://codex.wordpress.org/Appearance_Background_Screen\">Documentation on Custom Background</a>") + "</p>" + "<p>" + __("<a href=\"https://wordpress.org/support/\">Support</a>") + "</p>")
        wp_enqueue_media()
        wp_enqueue_script("custom-background")
        wp_enqueue_style("wp-color-picker")
    # end def admin_load
    #// 
    #// Execute custom background modification.
    #// 
    #// @since 3.0.0
    #//
    def take_action(self):
        
        if php_empty(lambda : PHP_POST):
            return
        # end if
        if (php_isset(lambda : PHP_POST["reset-background"])):
            check_admin_referer("custom-background-reset", "_wpnonce-custom-background-reset")
            remove_theme_mod("background_image")
            remove_theme_mod("background_image_thumb")
            self.updated = True
            return
        # end if
        if (php_isset(lambda : PHP_POST["remove-background"])):
            #// @todo Uploaded files are not removed here.
            check_admin_referer("custom-background-remove", "_wpnonce-custom-background-remove")
            set_theme_mod("background_image", "")
            set_theme_mod("background_image_thumb", "")
            self.updated = True
            wp_safe_redirect(PHP_POST["_wp_http_referer"])
            return
        # end if
        if (php_isset(lambda : PHP_POST["background-preset"])):
            check_admin_referer("custom-background")
            if php_in_array(PHP_POST["background-preset"], Array("default", "fill", "fit", "repeat", "custom"), True):
                preset = PHP_POST["background-preset"]
            else:
                preset = "default"
            # end if
            set_theme_mod("background_preset", preset)
        # end if
        if (php_isset(lambda : PHP_POST["background-position"])):
            check_admin_referer("custom-background")
            position = php_explode(" ", PHP_POST["background-position"])
            if php_in_array(position[0], Array("left", "center", "right"), True):
                position_x = position[0]
            else:
                position_x = "left"
            # end if
            if php_in_array(position[1], Array("top", "center", "bottom"), True):
                position_y = position[1]
            else:
                position_y = "top"
            # end if
            set_theme_mod("background_position_x", position_x)
            set_theme_mod("background_position_y", position_y)
        # end if
        if (php_isset(lambda : PHP_POST["background-size"])):
            check_admin_referer("custom-background")
            if php_in_array(PHP_POST["background-size"], Array("auto", "contain", "cover"), True):
                size = PHP_POST["background-size"]
            else:
                size = "auto"
            # end if
            set_theme_mod("background_size", size)
        # end if
        if (php_isset(lambda : PHP_POST["background-repeat"])):
            check_admin_referer("custom-background")
            repeat = PHP_POST["background-repeat"]
            if "no-repeat" != repeat:
                repeat = "repeat"
            # end if
            set_theme_mod("background_repeat", repeat)
        # end if
        if (php_isset(lambda : PHP_POST["background-attachment"])):
            check_admin_referer("custom-background")
            attachment = PHP_POST["background-attachment"]
            if "fixed" != attachment:
                attachment = "scroll"
            # end if
            set_theme_mod("background_attachment", attachment)
        # end if
        if (php_isset(lambda : PHP_POST["background-color"])):
            check_admin_referer("custom-background")
            color = php_preg_replace("/[^0-9a-fA-F]/", "", PHP_POST["background-color"])
            if php_strlen(color) == 6 or php_strlen(color) == 3:
                set_theme_mod("background_color", color)
            else:
                set_theme_mod("background_color", "")
            # end if
        # end if
        self.updated = True
    # end def take_action
    #// 
    #// Display the custom background page.
    #// 
    #// @since 3.0.0
    #//
    def admin_page(self):
        
        php_print("<div class=\"wrap\" id=\"custom-background\">\n<h1>")
        _e("Custom Background")
        php_print("</h1>\n\n        ")
        if current_user_can("customize"):
            php_print("<div class=\"notice notice-info hide-if-no-customize\">\n    <p>\n           ")
            printf(__("You can now manage and live-preview Custom Backgrounds in the <a href=\"%s\">Customizer</a>."), admin_url("customize.php?autofocus[control]=background_image"))
            php_print(" </p>\n</div>\n      ")
        # end if
        php_print("\n       ")
        if (not php_empty(lambda : self.updated)):
            php_print("<div id=\"message\" class=\"updated\">\n <p>\n           ")
            #// translators: %s: Home URL.
            printf(__("Background updated. <a href=\"%s\">Visit your site</a> to see how it looks."), home_url("/"))
            php_print(" </p>\n</div>\n      ")
        # end if
        php_print("\n<h2>")
        _e("Background Image")
        php_print("""</h2>
        <table class=\"form-table\" role=\"presentation\">
        <tbody>
        <tr>
        <th scope=\"row\">""")
        _e("Preview")
        php_print("</th>\n<td>\n        ")
        if self.admin_image_div_callback:
            php_call_user_func(self.admin_image_div_callback)
        else:
            background_styles = ""
            bgcolor = get_background_color()
            if bgcolor:
                background_styles += "background-color: #" + bgcolor + ";"
            # end if
            background_image_thumb = get_background_image()
            if background_image_thumb:
                background_image_thumb = esc_url(set_url_scheme(get_theme_mod("background_image_thumb", php_str_replace("%", "%%", background_image_thumb))))
                background_position_x = get_theme_mod("background_position_x", get_theme_support("custom-background", "default-position-x"))
                background_position_y = get_theme_mod("background_position_y", get_theme_support("custom-background", "default-position-y"))
                background_size = get_theme_mod("background_size", get_theme_support("custom-background", "default-size"))
                background_repeat = get_theme_mod("background_repeat", get_theme_support("custom-background", "default-repeat"))
                background_attachment = get_theme_mod("background_attachment", get_theme_support("custom-background", "default-attachment"))
                #// Background-image URL must be single quote, see below.
                background_styles += str(" background-image: url('") + str(background_image_thumb) + str("');") + str(" background-size: ") + str(background_size) + str(";") + str(" background-position: ") + str(background_position_x) + str(" ") + str(background_position_y) + str(";") + str(" background-repeat: ") + str(background_repeat) + str(";") + str(" background-attachment: ") + str(background_attachment) + str(";")
            # end if
            php_print(" <div id=\"custom-background-image\" style=\"")
            php_print(background_styles)
            php_print("\">")
            pass
            php_print("         ")
            if background_image_thumb:
                php_print("     <img class=\"custom-background-image\" src=\"")
                php_print(background_image_thumb)
                php_print("\" style=\"visibility:hidden;\" alt=\"\" /><br />\n      <img class=\"custom-background-image\" src=\"")
                php_print(background_image_thumb)
                php_print("\" style=\"visibility:hidden;\" alt=\"\" />\n        ")
            # end if
            php_print(" </div>\n    ")
        # end if
        php_print("""</td>
        </tr>
        """)
        if get_background_image():
            php_print("<tr>\n<th scope=\"row\">")
            _e("Remove Image")
            php_print("""</th>
            <td>
            <form method=\"post\">
            """)
            wp_nonce_field("custom-background-remove", "_wpnonce-custom-background-remove")
            php_print("         ")
            submit_button(__("Remove Background Image"), "", "remove-background", False)
            php_print("<br/>\n          ")
            _e("This will remove the background image. You will not be able to restore any customizations.")
            php_print("""</form>
            </td>
            </tr>
            """)
        # end if
        php_print("\n       ")
        default_image = get_theme_support("custom-background", "default-image")
        php_print("     ")
        if default_image and get_background_image() != default_image:
            php_print("<tr>\n<th scope=\"row\">")
            _e("Restore Original Image")
            php_print("""</th>
            <td>
            <form method=\"post\">
            """)
            wp_nonce_field("custom-background-reset", "_wpnonce-custom-background-reset")
            php_print("         ")
            submit_button(__("Restore Original Image"), "", "reset-background", False)
            php_print("<br/>\n          ")
            _e("This will restore the original background image. You will not be able to restore any customizations.")
            php_print("""</form>
            </td>
            </tr>
            """)
        # end if
        php_print("\n       ")
        if current_user_can("upload_files"):
            php_print("<tr>\n<th scope=\"row\">")
            _e("Select Image")
            php_print("""</th>
            <td><form enctype=\"multipart/form-data\" id=\"upload-form\" class=\"wp-upload-form\" method=\"post\">
            <p>
            <label for=\"upload\">""")
            _e("Choose an image from your computer:")
            php_print("""</label><br />
            <input type=\"file\" id=\"upload\" name=\"import\" />
            <input type=\"hidden\" name=\"action\" value=\"save\" />
            """)
            wp_nonce_field("custom-background-upload", "_wpnonce-custom-background-upload")
            php_print("         ")
            submit_button(__("Upload"), "", "submit", False)
            php_print(" </p>\n  <p>\n       <label for=\"choose-from-library-link\">")
            _e("Or choose an image from your media library:")
            php_print("</label><br />\n     <button id=\"choose-from-library-link\" class=\"button\"\n          data-choose=\"")
            esc_attr_e("Choose a Background Image")
            php_print("\"\n         data-update=\"")
            esc_attr_e("Set as background")
            php_print("\">")
            _e("Choose Image")
            php_print("""</button>
            </p>
            </form>
            </td>
            </tr>
            """)
        # end if
        php_print("""</tbody>
        </table>
        <h2>""")
        _e("Display Options")
        php_print("""</h2>
        <form method=\"post\">
        <table class=\"form-table\" role=\"presentation\">
        <tbody>
        """)
        if get_background_image():
            php_print("<input name=\"background-preset\" type=\"hidden\" value=\"custom\">\n\n          ")
            background_position = php_sprintf("%s %s", get_theme_mod("background_position_x", get_theme_support("custom-background", "default-position-x")), get_theme_mod("background_position_y", get_theme_support("custom-background", "default-position-y")))
            background_position_options = Array(Array({"left top": Array({"label": __("Top Left"), "icon": "dashicons dashicons-arrow-left-alt"})}, {"center top": Array({"label": __("Top"), "icon": "dashicons dashicons-arrow-up-alt"})}, {"right top": Array({"label": __("Top Right"), "icon": "dashicons dashicons-arrow-right-alt"})}), Array({"left center": Array({"label": __("Left"), "icon": "dashicons dashicons-arrow-left-alt"})}, {"center center": Array({"label": __("Center"), "icon": "background-position-center-icon"})}, {"right center": Array({"label": __("Right"), "icon": "dashicons dashicons-arrow-right-alt"})}), Array({"left bottom": Array({"label": __("Bottom Left"), "icon": "dashicons dashicons-arrow-left-alt"})}, {"center bottom": Array({"label": __("Bottom"), "icon": "dashicons dashicons-arrow-down-alt"})}, {"right bottom": Array({"label": __("Bottom Right"), "icon": "dashicons dashicons-arrow-right-alt"})}))
            php_print("<tr>\n<th scope=\"row\">")
            _e("Image Position")
            php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
            _e("Image Position")
            php_print("</span></legend>\n<div class=\"background-position-control\">\n          ")
            for group in background_position_options:
                php_print(" <div class=\"button-group\">\n              ")
                for value,input in group:
                    php_print("     <label>\n           <input class=\"screen-reader-text\" name=\"background-position\" type=\"radio\" value=\"")
                    php_print(esc_attr(value))
                    php_print("\"")
                    checked(value, background_position)
                    php_print(">\n          <span class=\"button display-options position\"><span class=\"")
                    php_print(esc_attr(input["icon"]))
                    php_print("\" aria-hidden=\"true\"></span></span>\n         <span class=\"screen-reader-text\">")
                    php_print(input["label"])
                    php_print("</span>\n        </label>\n  ")
                # end for
                php_print(" </div>\n")
            # end for
            php_print("""</div>
            </fieldset></td>
            </tr>
            <tr>
            <th scope=\"row\"><label for=\"background-size\">""")
            _e("Image Size")
            php_print("</label></th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
            _e("Image Size")
            php_print("</span></legend>\n<select id=\"background-size\" name=\"background-size\">\n<option value=\"auto\"")
            selected("auto", get_theme_mod("background_size", get_theme_support("custom-background", "default-size")))
            php_print(">")
            _ex("Original", "Original Size")
            php_print("</option>\n<option value=\"contain\"")
            selected("contain", get_theme_mod("background_size", get_theme_support("custom-background", "default-size")))
            php_print(">")
            _e("Fit to Screen")
            php_print("</option>\n<option value=\"cover\"")
            selected("cover", get_theme_mod("background_size", get_theme_support("custom-background", "default-size")))
            php_print(">")
            _e("Fill Screen")
            php_print("""</option>
            </select>
            </fieldset></td>
            </tr>
            <tr>
            <th scope=\"row\">""")
            _ex("Repeat", "Background Repeat")
            php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
            _ex("Repeat", "Background Repeat")
            php_print("</span></legend>\n<input name=\"background-repeat\" type=\"hidden\" value=\"no-repeat\">\n<label><input type=\"checkbox\" name=\"background-repeat\" value=\"repeat\"")
            checked("repeat", get_theme_mod("background_repeat", get_theme_support("custom-background", "default-repeat")))
            php_print("> ")
            _e("Repeat Background Image")
            php_print("""</label>
            </fieldset></td>
            </tr>
            <tr>
            <th scope=\"row\">""")
            _ex("Scroll", "Background Scroll")
            php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
            _ex("Scroll", "Background Scroll")
            php_print("</span></legend>\n<input name=\"background-attachment\" type=\"hidden\" value=\"fixed\">\n<label><input name=\"background-attachment\" type=\"checkbox\" value=\"scroll\" ")
            checked("scroll", get_theme_mod("background_attachment", get_theme_support("custom-background", "default-attachment")))
            php_print("> ")
            _e("Scroll with Page")
            php_print("""</label>
            </fieldset></td>
            </tr>
            """)
        # end if
        pass
        php_print("<tr>\n<th scope=\"row\">")
        _e("Background Color")
        php_print("</th>\n<td><fieldset><legend class=\"screen-reader-text\"><span>")
        _e("Background Color")
        php_print("</span></legend>\n       ")
        default_color = ""
        if current_theme_supports("custom-background", "default-color"):
            default_color = " data-default-color=\"#" + esc_attr(get_theme_support("custom-background", "default-color")) + "\""
        # end if
        php_print("<input type=\"text\" name=\"background-color\" id=\"background-color\" value=\"#")
        php_print(esc_attr(get_background_color()))
        php_print("\"")
        php_print(default_color)
        php_print(""">
        </fieldset></td>
        </tr>
        </tbody>
        </table>
        """)
        wp_nonce_field("custom-background")
        php_print("     ")
        submit_button(None, "primary", "save-background-options")
        php_print("""</form>
        </div>
        """)
    # end def admin_page
    #// 
    #// Handle an Image upload for the background image.
    #// 
    #// @since 3.0.0
    #//
    def handle_upload(self):
        
        if php_empty(lambda : PHP_FILES):
            return
        # end if
        check_admin_referer("custom-background-upload", "_wpnonce-custom-background-upload")
        overrides = Array({"test_form": False})
        uploaded_file = PHP_FILES["import"]
        wp_filetype = wp_check_filetype_and_ext(uploaded_file["tmp_name"], uploaded_file["name"])
        if (not wp_match_mime_types("image", wp_filetype["type"])):
            wp_die(__("The uploaded file is not a valid image. Please try again."))
        # end if
        file = wp_handle_upload(uploaded_file, overrides)
        if (php_isset(lambda : file["error"])):
            wp_die(file["error"])
        # end if
        url = file["url"]
        type = file["type"]
        file = file["file"]
        filename = wp_basename(file)
        #// Construct the object array.
        object = Array({"post_title": filename, "post_content": url, "post_mime_type": type, "guid": url, "context": "custom-background"})
        #// Save the data.
        id = wp_insert_attachment(object, file)
        #// Add the metadata.
        wp_update_attachment_metadata(id, wp_generate_attachment_metadata(id, file))
        update_post_meta(id, "_wp_attachment_is_custom_background", get_option("stylesheet"))
        set_theme_mod("background_image", esc_url_raw(url))
        thumbnail = wp_get_attachment_image_src(id, "thumbnail")
        set_theme_mod("background_image_thumb", esc_url_raw(thumbnail[0]))
        #// This action is documented in wp-admin/includes/class-custom-image-header.php
        do_action("wp_create_file_in_uploads", file, id)
        #// For replication.
        self.updated = True
    # end def handle_upload
    #// 
    #// Ajax handler for adding custom background context to an attachment.
    #// 
    #// Triggers when the user adds a new background image from the
    #// Media Manager.
    #// 
    #// @since 4.1.0
    #//
    def ajax_background_add(self):
        
        check_ajax_referer("background-add", "nonce")
        if (not current_user_can("edit_theme_options")):
            wp_send_json_error()
        # end if
        attachment_id = absint(PHP_POST["attachment_id"])
        if attachment_id < 1:
            wp_send_json_error()
        # end if
        update_post_meta(attachment_id, "_wp_attachment_is_custom_background", get_stylesheet())
        wp_send_json_success()
    # end def ajax_background_add
    #// 
    #// @since 3.4.0
    #// @deprecated 3.5.0
    #// 
    #// @param array $form_fields
    #// @return array $form_fields
    #//
    def attachment_fields_to_edit(self, form_fields=None):
        
        return form_fields
    # end def attachment_fields_to_edit
    #// 
    #// @since 3.4.0
    #// @deprecated 3.5.0
    #// 
    #// @param array $tabs
    #// @return array $tabs
    #//
    def filter_upload_tabs(self, tabs=None):
        
        return tabs
    # end def filter_upload_tabs
    #// 
    #// @since 3.4.0
    #// @deprecated 3.5.0
    #//
    def wp_set_background_image(self):
        
        if (not current_user_can("edit_theme_options")) or (not (php_isset(lambda : PHP_POST["attachment_id"]))):
            php_exit(0)
        # end if
        attachment_id = absint(PHP_POST["attachment_id"])
        sizes = php_array_keys(apply_filters("image_size_names_choose", Array({"thumbnail": __("Thumbnail"), "medium": __("Medium"), "large": __("Large"), "full": __("Full Size")})))
        size = "thumbnail"
        if php_in_array(PHP_POST["size"], sizes):
            size = esc_attr(PHP_POST["size"])
        # end if
        update_post_meta(attachment_id, "_wp_attachment_is_custom_background", get_option("stylesheet"))
        url = wp_get_attachment_image_src(attachment_id, size)
        thumbnail = wp_get_attachment_image_src(attachment_id, "thumbnail")
        set_theme_mod("background_image", esc_url_raw(url[0]))
        set_theme_mod("background_image_thumb", esc_url_raw(thumbnail[0]))
        php_exit(0)
    # end def wp_set_background_image
# end class Custom_Background