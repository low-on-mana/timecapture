/* globals mcName, mcColor, mcJobtype, mcColspan */
function pad(n){return n<10 ? '0'+n : n;}
$(document).ready(function(){
    var DAY_START = 9;
    // var DAY_END = 22;
	var mdown = false;
	var draggedStuff = "";
    var selectedTD = [];
    var form = $('form:first');
    $('[data-toggle="tooltip"]').tooltip();
    function showPopover(elem){
        elem.popover('show');
        elem.attr('aria-copy',elem.attr('aria-describedby'));
    }
    function hidePopover(elem){
        elem.popover('hide');
        elem.removeAttr('aria-copy');
    }
    function timesheetEntry(start,colspan,client,jobtype,date,category,description)
    {
        this.start = start;
        this.colspan =  colspan;
        this.client = client;
        this.jobtype = jobtype;
        this.date = date;
        this.category = category;
        this.description = description;
    }

	$('td').hover(function(){
		$(this).toggleClass('highlighted');
	});

	$('td.active2').mousedown(function(){
		mdown = true;
		draggedStuff += " ";
        selectedTD = [];
		if(!$(this).hasClass('dragged') && !$(this).hasClass('oldie')){
			$(this).addClass('dragged');
			draggedStuff += $(this).html();
            selectedTD.push($(this));
		}
		
	});

	$(this).mouseup(function(){
		mdown = false;
		$('#somespan').text(draggedStuff);
        if(selectedTD.length > 0)
        {
            $('.dragged').addClass('oldie');
            $('.dragged').removeClass('dragged');
        
            for(var i = 1; i<selectedTD.length;i++)
            {
                selectedTD[i].remove();
            }    
            selectedTD[0].text('');
            selectedTD[0].attr("colspan",selectedTD.length);
            selectedTD[0].data("container","body");
            selectedTD[0].data("placement","bottom");
            selectedTD[0].data("html","true");
            selectedTD[0].data("trigger","manual");
            selectedTD[0].data("content",$('#popover-form').html());
            selectedTD[0].tooltip({
                    placement : 'top',
                    trigger: 'hover focus',
                    title: function(){ return $(this).closest('td').data('tooltip');},
                    container: selectedTD[0]
                });
            showPopover(selectedTD[0]);
            selectedTD = [];
        }
	});

 	$('td.active2').mousemove(function(){
		if(mdown === true && !$(this).hasClass('dragged') && !$(this).hasClass('oldie') && ($(this).prev().hasClass('dragged') || $(this).next().hasClass('dragged'))){
			$(this).addClass('dragged');
			draggedStuff += $(this).html();
            selectedTD.push($(this));
		}
	});

    $(this).on('click','#popover-button',function(){
        var popId = $(this).closest('.popover').attr('id'); 
        var client_select = $(this).siblings('#select-client');
        var jobtype = $(this).siblings('#select-jobtype').find(':selected');
        var description = $(this).siblings('#input-description');

        if(jobtype.data('ismis') === 'True'){
            client_select.val(mcName);
        }
        var client = client_select.find(':selected');

        $('.oldie').each(function(){
            if( $(this).attr('aria-copy') === popId)
            { 
                $(this).data('tooltip',description.val() === '' ? 'Did you miss something?':description.val());
                hidePopover($(this));
                $(this).css('background-color',client.data('color'));
                if($(this).children('span.client').length === 0) 
                {
                    $(this).append('<span class="client">'+client.text()+'</span><br>');
                    $(this).append('<span class="jobtype">'+jobtype.text()+'</span><br>');
                    $(this).append('<span class="description">'+description.val()+'</span>');
                }
                else
                {
                    $(this).children('span.client').text(client.text());
                    $(this).children('span.jobtype').text(jobtype.text());
                    $(this).children('span.description').text(description.val());
                }
                return;
            }
        });
    });
    
    $(this).on('mousedown','td.oldie',function(){
        var popover_id = $(this).attr('aria-copy');
        if(popover_id === undefined)
        {
            showPopover($(this));
            var div_form_group = $('#'+$(this).attr('aria-copy')).find('div.form-group');
            div_form_group.children('input').val($(this).children('span.description').text());
            div_form_group.children('#select-client').val($(this).children('span.client').text());
            div_form_group.children('#select-jobtype').val($(this).children('span.jobtype').text());

        }
        else
        {
            hidePopover($(this));
        }   
    });

    $('#push-timesheet').click(function(){
         if(!confirm('Are you sure? '))
        {
            return;
        }
         var hrStart = DAY_START;
         var timesheetentries = [];
        $('tr.active3').children('td').each(function(){
                var d = new Date();
                var clientDate = pad(d.getMonth()+1)+'/'+pad(d.getDate())+'/'+d.getFullYear();
                var colspan;
                if($(this).attr('colspan') !== undefined)
                {   
                    colspan =  Number($(this).attr('colspan'));
                }
                else
                {
                    colspan = 1;
                }
                if($(this).hasClass('oldie') && $(this).hasClass('active2') && $(this).children('span.client').text().length > 0 && $(this).children('span.jobtype').text().length > 0 )
                {
                    timesheetentries.push(new timesheetEntry(hrStart,colspan,$(this).children('span.client').text(),$(this).children('span.jobtype').text(),clientDate,'TODAY',$(this).children('span.description').text()));
                }
                hrStart += colspan; 
        });

        $('tr.leave').each(function(){
            if($(this).children('td').children('span').length > 1)
            {
                var clientDate = $(this).data('date');
                timesheetentries.push(new timesheetEntry(DAY_START,mcColspan,mcName,mcJobtype,clientDate,'LEAVE'));
            }
        });
        form.children('input#hinp').attr('value',JSON.stringify(timesheetentries));
        form.submit();
    });

    $('tr.leave').click(function(){
        if($(this).attr("aria-copy") === undefined )
        {
            $(this).data("container","body");
            $(this).data("placement","bottom");
            $(this).data("html","true");
            $(this).data("trigger","manual");
            $(this).data("content",$('#popover-leave-form').html());
            showPopover($(this));
        }
        else
        {
            hidePopover($(this));
        }
    });

    $(this).on('click','#popover-leave-button',function(){
        var popId = $(this).closest('.popover').attr('id'); 
        $('tr.leave').each(function(){
            if($(this).attr('aria-copy') === popId)
            {
                hidePopover($(this));
                $(this).children('td').remove();
                $(this).append('<td style="background-color:'+mcColor+'" colspan="'+mcColspan+'"><span class="client">'+mcName+'</span><br><span class="jobtype">'+mcJobtype+'</span></td>');
                return;
            }
        });
    });

    $(this).on('keyup','input#input-description',function(){
        console.log('firstinvoke');
        var max_length = $(this).attr('maxlength');
        var cur_length = $(this).val().length; 
        $(this).siblings('span#input-length-span').text(max_length-cur_length);
    });

    $(this).on('change','select#select-jobtype',function(){
        var selected_option = $(this).find(':selected');
        if(selected_option.data('ismis') === 'True'){
            $(this).siblings('select#select-client').val(mcName);
        }
    });

});
