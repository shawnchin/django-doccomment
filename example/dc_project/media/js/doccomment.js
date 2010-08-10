/* USAGE:
 *
 * To load comments for a document, simply call:
 *    doccomment.init();
 *    doccomment.loadCommentCount(<URL_FOR_AJAX_CALL>);
 *
 * The script will locate doccomment blocks with and append divs to 
 * display comments next to them.
 *
 * Internal parameters can be modified by running init as such:
 *    doccomment.init({'commentDivWidth':50, 'commentClass':'yourOwnClass'})
 *
 * Possible parameters are:
 *  commentDivWidth - width of comment DIV
 *  hoverClass      - CSS class added to content DIV during mouse over
 *  commentClass    - CSS class used to style comment DIVs
 *  contentClass    - CSS class used to style and identify content DIVs
 *  ccountClass     - CSS for SPAN used to display comment count
 *  commentIDPrefix - ID prefix used to identify comment DIVs
 *  contentIDPrefix - ID prefix used to identify content DIVs
 *
 */
var doccomment = function($) {

    /* default parameters */
    var param = {
        commentDivWidth : 35,
        cdivMinHeight   : 25,
        hoverClass   : 'doccomment-hover',
        commentClass : 'doccomment-cdiv',
        contentClass : 'doccomment-block',
        ccountClass  : 'doccomment-ccount',
        hasdivMarker : 'doccomment-hascommentdiv',
        contentIDPrefix : 'DE-',
        commentIDPrefix : 'CB-'
    };

    /* for each content DIV, create an associated comment DIV and append to
     * content DIV. New DIV shall remain hidden until triggered by a hover.
     *
     * Positioning of div will be handled later by alignCommentDiv()
     */
    var createCommentDiv = function () {
        /* look for content classes, and extract the ID to build 
         * the associated Comment DIV
         */
        var rePattern = new RegExp("^" + param.contentIDPrefix + "(\\d+)$");
        $("." + param.contentClass).each(function() {

            /* check if commend div already created */
            if ($(this).hasClass(param.hasdivMarker)) { return; }

            var found = rePattern.exec($(this).attr('id'));
            if (found && found.length == 2) {
                var id = found[1];
                var contentDIV = $(this);
                
                /* create comment DIV */
                var commentDIV = $('<div></div>').hide()
                    .addClass(param.commentClass)
                    .attr('id', param.commentIDPrefix + id)
                    .css('position', 'absolute')
                    .css('cursor', 'pointer')
                    .appendTo(contentDIV);

                /* store reference to comment DIV in contentDIV */
                contentDIV.data('cdiv', commentDIV);
                
                /* add/remove class on mouseover/out */
                contentDIV.hover(
                    function() { $(this).addClass(param.hoverClass); },
                    function() { $(this).removeClass(param.hoverClass); }
                );

            } /* end if */
            $(this).addClass(param.hasdivMarker);

        }); /* ends for each content div */
        
    };

    /* align comment DIV to the left of content DIV
    * making sure the height is the same
    *
    * Expects a reference to the associated comment div to be stored
    * in the content div under .data('cdiv')
    *
    * This function is called at initialisation as well
    * as after a window resize event
    */
    var alignCommentDiv = function () {
        $("." + param.contentClass).each(function() {
            var offset = $(this).offset();
            var height = $(this).css('height');
            if (height < param.cdivMinHeight) { 
                height = param.cdivMinHeight; 
                $(this).css('height', param.cdivMinHeight);
            }

            /* comment div is stored in content.data('cdiv') */
            $(this).data('cdiv')
                .css('top', offset.top)
                .css('left', offset.left - param.commentDivWidth)
                .css('width', param.commentDivWidth)
                .css('height', height);
        })
    };

    /* load comment count and URL using AJAX call */
    var do_loadCommentCount = function(ajax_url) {
        $.ajax({
            url      : ajax_url, 
            dataType : 'json',
            cache    : false,
            success  : function(data) {
                for (i = 0; i < data.elemCount; i++) {
                    updateCommentCount(data.pageElements[i]);
                }
            },
            /* TODO: handle ajax call errors */
        });
    };

    var updateCommentCount = function(elem) {
        var id = elem.id;
        var url = elem.url;
        var ccount = elem.ccount;

        /* locate content div */
        var contentDIV = $('#' + param.contentIDPrefix + id);
        if (!contentDIV) { return; } /* cannot proceed */
        
        /* add SPAN to comment div */
        contentDIV.data('cdiv').html(
            "<span class='"+param.ccountClass+"'><a href='"+ url +"'>"+ ccount +"</a></span>"
        ).click(function() { /* make the whole div clickable */
            location = url;
        });

        /* if ccount = 0, only display during hover, else always display */
        if (ccount != 0) {
            contentDIV.data('cdiv').show();
        } else {
            contentDIV.hover(
                function() { /* mouseover */
                    $(this).data('cdiv').show();
                },
                function() { /* mouseout */
                    $(this).data('cdiv').hide();
                }
            );
        }
    }

    /* public functions */
    return {
        
        init : function(settings) {

            /* allow users to modify params */
            if (settings) {
                for (key in settings) {
                    if (key in param) {
                        param[key] = settings[key];
                    }
                }
            }

            /* create comment DIVs and align them to content */
            createCommentDiv();
            alignCommentDiv();
            
            /* realign DIVs when window is resized */
            $(window).resize(alignCommentDiv);        
        },

        loadCommentCount : function(ajax_url) {
            /* TODO: display spinner */
            do_loadCommentCount(ajax_url);
            /* TODO: hide spinner */
        }

    };
}(jQuery);