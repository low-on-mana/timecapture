/* globals django */
if (!$) {
    $ = django.jQuery;
}
$(document).ready(function(){
    console.log($(document).find('title').text());
    $('.special').each(function(){
        var ele_color = $(this).attr('value');
        var ele_li = $(this).parent().parent();
        ele_li.append("<td><div style=\"width:100px;height:20px;background-color:" + ele_color + "\"> </div></td>");
    });
});
